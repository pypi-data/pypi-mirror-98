import requests as req
from urllib.parse import parse_qs
from covid_cloud.constants import *


def login(email, personal_access_token, 
            auth_params = auth_params,
            search_url='', drs_url=''):
    try: 
        session = req.Session()

        # login at /login/token
        session.get(f'{auth_params["wallet_uri"]}/login/token',
                    params={
                        'token': personal_access_token,
                        "email": email,
                    },
                    allow_redirects=False
                    )
        
        auth_code_res = session.get(f'{auth_params["wallet_uri"]}/oauth/authorize',
                                    params={
                                        'response_type': 'code',
                                        'client_id': auth_params["client_id"],
                                        'redirect_uri': auth_params["redirect_uri"],
                                        'scopes': auth_scopes,
                                        'resource': f'{drs_url},{search_url}'
                                    },
                                    allow_redirects=False)
        auth_code = parse_qs(req.utils.urlparse(auth_code_res.headers['Location']).query)['code'][0]

        auth_token_res = session.post(f'{auth_params["wallet_uri"]}/oauth/token',
                                    data={
                                        'grant_type': 'authorization_code',
                                        'code': auth_code,
                                        'client_id': auth_params["client_id"],
                                        'client_secret': auth_params["client_secret"]
                                    })

        json_res = auth_token_res.json()
        print("Login successful!")

        return json_res
    except:
        raise Exception("Login failed!")

    
