from covid_cloud.client import *
from covid_cloud import constants
from pandas import DataFrame
from getpass import getpass
import json


class COVIDCloud:
    def __init__(self, email=None, personal_access_token=None, search_url=None, drs_url=None, auth_params = auth_params):
        self.email = email
        self.personal_access_token = personal_access_token
        self.search_url = search_url
        self.drs_url = drs_url
        self.auth_params = auth_params
        self.oauth_token = None

    def login(self, email=None, personal_access_token=None):
        
        #if the user did not provide a PAT or email, get that from input
        if not (personal_access_token or self.personal_access_token):
            personal_access_token = getpass("Enter your Personal Access Token (PAT): ")
        
        if not (email or self.email):
            email = input("Enter your Email: ")

        self.oauth_token = login(email=email if email else self.email,
                                 personal_access_token= personal_access_token if personal_access_token else self.personal_access_token,
                                 search_url=self.search_url,
                                 drs_url=self.drs_url)['access_token']

    def query(self, q, download=False, use_json=False, raw=False):
        return json.loads(query(self.search_url, q, download, use_json, raw, self.oauth_token))

    def list_tables(self):
        return json.loads(get_tables(self.search_url, self.oauth_token))

    def get_table(self, table_name):
        return json.loads(get_table(self.search_url, table_name, self.oauth_token))

    def load(self, urls, output_dir=downloads_directory):
        download_content = []
        download_files(self.drs_url, urls, output_dir, self.oauth_token, download_content)
        return download_content

    def download(self, urls, output_dir=downloads_directory):
        return download_files(self.drs_url, urls, output_dir, self.oauth_token)
