import click
import urllib3
import threading
import os
from typing import Optional
from covid_cloud.constants import *
from requests.exceptions import HTTPError
from covid_cloud.client.utils import get_drs_client
import gzip
import re
import io
import pandas as pd

#since our downloads are multi-threaded, we use a lock to avoid race conditions
output_lock = threading.Lock()


def handle_file_response(download_file,data):
    #decode if fasta
    if re.search(r'\.fa',download_file):
        data = data.decode('utf-8')
        
    return data


def file_to_dataframe(download_file,data):
    #turn into dataframe for FASTA/FASTQ files, otherwise just return raw data
    if re.search(r'\.fa',download_file):
        data = data.split('\n',maxsplit=1)

        meta = data[0]
        sequence = data[1].replace('\n','') #remove newlines
        
        return pd.DataFrame({
            "meta": [meta],
            "sequence": [sequence]
            })
    
    return data


def is_drs_url(url):
    return url[:3] == 'drs'


def download_file(drs_url, url, output_dir, oauth_token: Optional[str] = None, out: Optional[list] = None):
    drs_client = get_drs_client(drs_url, oauth_token)

    http = urllib3.PoolManager()
    chunk_size = 1024
    download_url = url
    download_file = ""
    signed_access_ids = ['az-blobstore-signed']
    
    object_id = url.split('/')[-1]
    if is_drs_url(url):
        # parse the drs url to the resource url
        try:
            object_info = drs_client.get_object_info(object_id)
        except HTTPError as e:
            click.echo(e)
            if '404' in str(e.response):
                click.secho("There was an error getting object info from the DRS Client", fg='red')
            return
        except Exception as e:
            print(e)
            return

        if "access_methods" in object_info.keys():
            for access_method in object_info["access_methods"][0]:
                if access_method.get('access_id', None):
                    if access_method['access_id'] in signed_access_ids:
                        click.echo("found signed access_id @ access_method level")
                        try:
                            object_access = drs_client.get_object_access(object_id, access_method['access_id'])
                        except HTTPError as e:
                            click.echo(e)
                            return
                        download_url = object_access['url']
                        break

                # if we have an https, use that
                if access_method['type'] == 'https':
                    download_url = access_method['access_url']['url']
                    download_file = download_url.split('/')[-1]
                    break
        else:
            return  # next page token, just return
    
    try:
        download_stream = http.request('GET', download_url, preload_content=False)
    except:
        click.secho("There was an error downloading " + download_url, fg='red')
        return

    data = handle_file_response(download_file,download_stream.read())
    
    if out is not None: 
        output_lock.acquire()
        out = out.append(file_to_dataframe(download_file,data))
        output_lock.release()

    else:
        with open(f"{output_dir}/{download_file}", 'wb+') as dest:
            while True:
                data = download_stream.read(chunk_size)
                if not data:
                    break
                dest.write(data)


def download_files(drs_url, urls, output_dir=downloads_directory, oauth_token: Optional[str] = None, out=None):
    download_threads = []
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for url in urls:
        download = threading.Thread(target=download_file(drs_url, url, output_dir, oauth_token, out), name=url)
        download.daemon = True
        download_threads.append(download)
        download.start()

    for thread in download_threads:
        thread.join()

    if out is None:
        click.secho("Download Complete into " + output_dir, fg='green')