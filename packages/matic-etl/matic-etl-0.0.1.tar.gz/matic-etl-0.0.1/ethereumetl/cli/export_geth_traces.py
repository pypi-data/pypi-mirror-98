# MIT License
#
# Copyright (c) 2018 Evgeniy Filatov, evgeniyfilatov@gmail.com
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import click

from ethereumetl.jobs.export_geth_traces_job import ExportGethTracesJob
from ethereumetl.jobs.exporters.geth_traces_item_exporter import geth_traces_item_exporter
from blockchainetl.logging_utils import logging_basic_config
from ethereumetl.providers.auto import get_provider_from_uri
from ethereumetl.providers.auto import get_revolving_provider_from_uris
from ethereumetl.thread_local_proxy import ThreadLocalProxy
from ethereumetl.rate_limit_proxy import RateLimitingProxy

logging_basic_config()


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('-s', '--start-block', default=0, show_default=True, type=int, help='Start block')
@click.option('-e', '--end-block', required=True, type=int, help='End block')
@click.option('-b', '--batch-size', default=100, show_default=True, type=int, help='The number of blocks to process at a time.')
@click.option('-o', '--output', default='-', show_default=True, type=str,
              help='The output file for geth traces. If not specified stdout is used.')
@click.option('-w', '--max-workers', default=5, show_default=True, type=int, help='The maximum number of workers.')
@click.option('-p', '--provider-uri', required=True, type=str,
              help='The URI of the web3 provider e.g. '
                   'file://$HOME/Library/Ethereum/geth.ipc or http://localhost:8545/')
@click.option('-t', '--timeout', default=60, show_default=True, type=int, help='IPC or HTTP request timeout.')
@click.option('-r', '--rate-limit', default=None, show_default=True, type=int,
              help='Maximum requests per second for provider in case it has rate limiting')
@click.option('-v', '--revolving', default=False, show_default=True, type=bool,
              help='Enable endpoint revolving')
def export_geth_traces(start_block, end_block, batch_size, output, max_workers,
                       provider_uri, rate_limit, timeout=60, revolving=False):
    """Exports traces from geth node."""
    if revolving:
        api = ThreadLocalProxy(lambda: get_revolving_provider_from_uris(provider_uri, timeout=timeout, batch=True))
    else:
        api = ThreadLocalProxy(lambda: get_provider_from_uri(provider_uri, timeout=timeout, batch=True))

    job = ExportGethTracesJob(
        start_block=start_block,
        end_block=end_block,
        batch_size=batch_size,
        batch_web3_provider=RateLimitingProxy(api, rate_limit),
        max_workers=max_workers,
        item_exporter=geth_traces_item_exporter(output))

    job.run()
