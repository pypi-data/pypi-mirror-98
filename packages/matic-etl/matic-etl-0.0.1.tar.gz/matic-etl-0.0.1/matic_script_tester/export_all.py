# %%
# Append parent package (DEV)
import os, sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))


# %%
import logging


# %%
from ethereumetl.cli import (
    get_block_range_for_timestamps,
    extract_field,
    export_blocks_and_transactions,
    export_receipts_and_logs,
    extract_contracts,
    extract_tokens,
    extract_token_transfers,
    export_geth_traces,
    extract_geth_traces,
)
import os


# %%
from datetime import datetime, timedelta, timezone
from tempfile import TemporaryDirectory
from typing import List, Union, Iterator


# %%
from utils.commons import timestamp_chunk
from utils.google_cloud_storage_hook import SimpleGoogleCloudStorageHook
from utils.task_manager import TaskManager, TaskIDs

# %%
import httplib2
import google.auth
import google_auth_httplib2
import google.oauth2.service_account
from google.api_core.exceptions import GoogleAPICallError, AlreadyExists, RetryError
from googleapiclient.errors import HttpError


# %%
provider_uris = [
    "https://rpc-mainnet.maticvigil.com/v1/927c67086ea722f1b98b3ec14b174ce140d3a84e",
    "https://rpc-mainnet.maticvigil.com/v1/5dc314d2597052c4d1e00370733d762e5fcd3334",
    "https://rpc-mainnet.maticvigil.com/v1/908b40606eada9119d934ae2809b566b87f61cd7",
    "https://rpc-mainnet.maticvigil.com/v1/058a788a199c0017ce46b3900ddd801c6412372b",
    "https://rpc-mainnet.maticvigil.com/v1/3c91e94ed992e48ae091ed12d1d821f2fbdc0b43",
    "https://rpc-mainnet.maticvigil.com/v1/f9c8eaeeb3c203c8fab2a978c41300b68421dccc",
    "https://rpc-mainnet.maticvigil.com/v1/9c92c43ed76d0d0589914fab726015e08d2defb7",
    "https://rpc-mainnet.maticvigil.com/v1/a2e04be7c65204ab96046fb9a84e36b112ef082e",
    "https://rpc-mainnet.maticvigil.com/v1/287560478b0282eee31a95f3e7da08efdf7571ef",
    "https://rpc-mainnet.maticvigil.com/v1/dcca6097dd8fecd19ee7c07acf8e38b7f5c12809",

]

provider_uris_archival = [
    "https://rpc-mainnet.maticvigil.com/v1/927c67086ea722f1b98b3ec14b174ce140d3a84e",
    "https://rpc-mainnet.maticvigil.com/v1/5dc314d2597052c4d1e00370733d762e5fcd3334",
    "https://rpc-mainnet.maticvigil.com/v1/908b40606eada9119d934ae2809b566b87f61cd7",
    "https://rpc-mainnet.maticvigil.com/v1/058a788a199c0017ce46b3900ddd801c6412372b",
    "https://rpc-mainnet.maticvigil.com/v1/3c91e94ed992e48ae091ed12d1d821f2fbdc0b43",
    "https://rpc-mainnet.maticvigil.com/v1/f9c8eaeeb3c203c8fab2a978c41300b68421dccc",
    "https://rpc-mainnet.maticvigil.com/v1/9c92c43ed76d0d0589914fab726015e08d2defb7",
    "https://rpc-mainnet.maticvigil.com/v1/a2e04be7c65204ab96046fb9a84e36b112ef082e",
    "https://rpc-mainnet.maticvigil.com/v1/287560478b0282eee31a95f3e7da08efdf7571ef",
    "https://rpc-mainnet.maticvigil.com/v1/dcca6097dd8fecd19ee7c07acf8e38b7f5c12809",
]

export_max_workers = min(10,len(provider_uris) - 1)
export_batch_size = 10
output_bucket = "nftbank-matic-network"

# %%
CREDENTIALS = f".cred/pipeline-executor.contxtsio-nftbank.credentials"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = CREDENTIALS
SCOPE = ('https://www.googleapis.com/auth/cloud-platform',
        # 'https://www.googleapis.com/auth/bigquery',
        # 'https://www.googleapis.com/auth/drive'
        )
credentials, _ = google.auth.default(scopes=SCOPE)

cloud_storage_hook = SimpleGoogleCloudStorageHook(credentials=credentials, project_id="contxtsio-nftbank")

# %%
task_manager = TaskManager(mongodb_connection_uri="mongodb+srv://masterContxtsio:Contxtsio!23@cluster0.7qjx5.mongodb.net/admin?retryWrites=true&w=majority",
                           min_timestamp=datetime(2020, 5, 30, 16, 0, 0, 0, tzinfo=timezone.utc))
task_manager.initialize_db(TaskIDs['ALL'], "raw")

# %%
# Export
def export_path(directory, start_timestamp):
    return "export/raw/{directory}/block_date={block_date}/block_hour={block_hour}/".format(
        directory=directory,
        block_date=start_timestamp.strftime("%Y-%m-%d"),
        block_hour=start_timestamp.strftime("%H"),
    )

def copy_to_export_path(file_path, export_path):
    logging.info('Calling copy_to_export_path({}, {})'.format(file_path, export_path))
    filename = os.path.basename(file_path)

    cloud_storage_hook.upload_to_gcs(
        gcs_hook=cloud_storage_hook,
        bucket=output_bucket,
        object=export_path + filename,
        filename=file_path)

def copy_from_export_path(export_path, file_path):
    logging.info('Calling copy_from_export_path({}, {})'.format(export_path, file_path))
    filename = os.path.basename(file_path)

    cloud_storage_hook.download_from_gcs(gcs_hook=cloud_storage_hook, bucket=output_bucket, object=export_path + filename, filename=file_path)


# %%
storage_client = cloud_storage_hook.get_conn()

# %%
def add_provider_uri_fallback_loop(python_callable, provider_uris):
    """Tries each provider uri in provider_uris until the command succeeds"""

    def python_callable_with_fallback(**kwargs):
        for index, provider_uri in enumerate(provider_uris):
            kwargs['provider_uri'] = provider_uri
            try:
                ret = python_callable(**kwargs)
                break
            except Exception as e:
                if index < (len(provider_uris) - 1):
                    logging.exception('An exception occurred. Trying another uri')
                else:
                    raise e

        return ret

    return python_callable_with_fallback

# %%
##########################################
### EXTRANCTIONS
##########################################

# %%
def _get_block_range(provider_uri, start_timestamp, end_timestamp, **kwargs):
    with TemporaryDirectory() as tempdir:
        logging.info('Calling get_block_range_for_timestamps ({}, {})'.format(start_timestamp, end_timestamp))
        get_block_range_for_timestamps.callback(
            provider_uri=provider_uri,
            start_timestamp=start_timestamp,
            end_timestamp=end_timestamp,
            output=os.path.join(tempdir, "blocks_meta.txt")
        )

        with open(os.path.join(tempdir, "blocks_meta.txt")) as block_range_file:
            block_range = block_range_file.read()
            start_block, end_block = block_range.split(",")

    return int(start_block), int(end_block)


# %%
def _export_blocks_and_transactions_command(start_timestamp, start_block, end_block, provider_uri, **kwargs):
    with TemporaryDirectory() as tempdir:
        logging.info('Calling export_blocks_and_transactions ({}, {})'.format(start_block, end_block))

        export_blocks_and_transactions.callback(
            start_block=start_block,
            end_block=end_block,
            batch_size=export_batch_size,
            provider_uri=provider_uri,
            rate_limit=200,
            max_workers=export_max_workers,
            blocks_output=os.path.join(tempdir, "blocks.json"),
            transactions_output=os.path.join(tempdir, "transactions.json"),
            revolving=True,
        )

        copy_to_export_path(
                os.path.join(tempdir, "blocks.json"), export_path("blocks", start_timestamp)
        )

        copy_to_export_path(
            os.path.join(tempdir, "transactions.json"), export_path("transactions", start_timestamp)
        )


# %%
def _export_receipts_and_logs_command(start_timestamp, provider_uri, **kwargs):
    with TemporaryDirectory() as tempdir:
        copy_from_export_path(
            export_path("transactions", start_timestamp), os.path.join(tempdir, "transactions.json")
        )

        logging.info('Calling extract_field')
        extract_field.callback(
            input=os.path.join(tempdir, "transactions.json"),
            output=os.path.join(tempdir, "transaction_hashes.txt"),
            field="hash",
        )

        logging.info('Calling export_receipts_and_logs')
        export_receipts_and_logs.callback(
            batch_size=export_batch_size,
            transaction_hashes=os.path.join(tempdir, "transaction_hashes.txt"),
            provider_uri=provider_uri,
            rate_limit=200,
            max_workers=export_max_workers,
            receipts_output=os.path.join(tempdir, "receipts.json"),
            logs_output=os.path.join(tempdir, "logs.json"),
            revolving=True,
        )

        copy_to_export_path(
            os.path.join(tempdir, "receipts.json"), export_path("receipts", start_timestamp)
        )
        copy_to_export_path(
            os.path.join(tempdir, "logs.json"), export_path("logs", start_timestamp)
        )


# %%
def extract_token_transfers_command(execution_date, **kwargs):
    with TemporaryDirectory() as tempdir:
        copy_from_export_path(
            export_path("logs", execution_date), os.path.join(tempdir, "logs.json")
        )

        logging.info('Calling extract_token_transfers(..., {}, ..., {})'.format(
            export_batch_size, export_max_workers
        ))
        extract_token_transfers.callback(
            logs=os.path.join(tempdir, "logs.json"),
            batch_size=export_batch_size,
            output=os.path.join(tempdir, "token_transfers.json"),
            max_workers=export_max_workers,
        )

        copy_to_export_path(
            os.path.join(tempdir, "token_transfers.json"),
            export_path("token_transfers", execution_date),
        )

# %%
##########################################
### Get target ranges
##########################################
for task in task_manager.get_todos(TaskIDs["ALL"], "raw"):
    start_timestamp = task['start_timestamp']
    end_timestamp = task['end_timestamp']
    print(start_timestamp, end_timestamp)

    task_manager.task_started(TaskIDs["ALL"], "raw", start_timestamp, end_timestamp)

    ##########################################
    ### Get start / end block number
    ##########################################
    get_block_range = add_provider_uri_fallback_loop(_get_block_range, provider_uris)
    start_block, end_block = get_block_range(**{
        "start_timestamp": start_timestamp.timestamp(),
        "end_timestamp": end_timestamp.timestamp()
    })

    ##########################################
    ### Export blocks and transactions
    ##########################################
    _export_blocks_and_transactions_command(start_timestamp=start_timestamp,
                                            start_block=start_block,
                                            end_block=end_block,
                                            provider_uri=provider_uris)


    ##########################################
    ### Export receipts and logs
    ##########################################
    _export_receipts_and_logs_command(start_timestamp=start_timestamp,
                                    provider_uri=provider_uris)

    task_manager.task_finished(TaskIDs["ALL"], "raw", start_timestamp, end_timestamp)
