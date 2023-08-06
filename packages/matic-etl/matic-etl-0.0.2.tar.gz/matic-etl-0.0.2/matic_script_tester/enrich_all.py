#%%
from google.cloud import bigquery
import json

# %% For local
import google.auth
import os
HOME = os.getcwd()
CLIENT_ID = 'contxtsio-nftbank'
CREDENTIALS = f"./.cred/pipeline-executor.contxtsio-nftbank.credentials"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = CREDENTIALS

SCOPE = ('https://www.googleapis.com/auth/bigquery',
         'https://www.googleapis.com/auth/cloud-platform',
         'https://www.googleapis.com/auth/drive')
credentials, _ = google.auth.default(scopes=SCOPE)

bq_client = bigquery.Client(CLIENT_ID, credentials=credentials)

# %%
def load_table(data_name):
    schema_dicts = json.load(open(f"./schema/raw/{data_name}.json", "r+"))
    schema = [bigquery.SchemaField.from_api_repr(schema_dict) for schema_dict in schema_dicts]

    # Load bq data
    job_config = bigquery.LoadJobConfig()
    hive_partitioning = bigquery.external_config.HivePartitioningOptions()
    hive_partitioning.mode = "CUSTOM"
    hive_partitioning.source_uri_prefix = f"gs://nftbank-matic-network/export/raw/{data_name}/{{block_date:DATE}}/{{block_hour:STRING}}/"  #path to hive partition data
    job_config.hive_partitioning = hive_partitioning

    job_config.source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
    job_config.create_disposition = bigquery.CreateDisposition.CREATE_IF_NEEDED
    job_config.write_disposition = bigquery.WriteDisposition.WRITE_APPEND
    job_config.schema = schema
    # job_config.time_partitioning = bigquery.TimePartitioning(type_=bigquery.TimePartitioningType().DAY, field='block_date')
    job_config.autodetect = True

    # # full
    # uri = "gs://nftbank-metadata/discord/users/*.jsonl"  #path to data

    # incr
    uri = f"gs://nftbank-matic-network/export/raw/{data_name}/*.json"  #path to data

    load_job = bq_client.load_table_from_uri(uri,
                                        f"contxtsio-nftbank.matic_staging_area.raw_{data_name}",
                                        job_config=job_config)  # API request

    load_job.result()  # Waits for table load to complete.


# %%
load_table('blocks')
load_table('transactions')
load_table('logs')
load_table('receipts')
