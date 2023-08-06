"""SNaP OneDrive Report Aggregator

# Resources
1. Docs: https://docs.microsoft.com/en-us/onedrive/developer/rest-api/
getting-started/msa-oauth?view=odsp-graph-online

# Minor to-do's
- Verified exists: If need get code and user pastes, does script correctly run
  all the way through without any intermediate error and need to re-run a
  second time? When I was developing, I had to run twice in a row one time.
- Alternative to have user paste this into browser and copy/paste the token?
- how make code and token last longer?:
  - https://docs.microsoft.com/en-us/onedrive/developer/rest-api/getting-started/graph-oauth?view=odsp-graph-online#step-3-get-a-new-access-token-or-refresh-token
  - can update token max life via powershell only
"""
import base64
# import json
import os
import re

import requests
import urllib.parse as urlparse
from urllib.parse import parse_qs
from typing import Dict, List


# Variables
ROOT_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), '..')
CODE_FILE_PATH = os.path.join(ROOT_DIR, 'code.env')
TOKEN_FILE_PATH = os.path.join(ROOT_DIR, 'token.env')
CONFIG = {
    'redirect_uri': 'https://login.live.com/oauth20_desktop.srf',
    'client_id': os.getenv('ATTEMPT2_APP_ID'),
    'client_secret': os.getenv('n/a', 'wCv35Dzw5AFgOMbE._CJ-EO-4C1-jfFVJH'),
    'api_base_url': 'https://api.onedrive.com/v1.0/',
    'scopes': ['Files.ReadWrite.All'],
    'fetch_headers': {
        'Host': 'graph.microsoft.com',
        'Authorization': 'Bearer {}'
    }
}

# Update config
client_id = CONFIG['client_id']
scope = CONFIG['scopes'][0]
redirect_uri = CONFIG['redirect_uri']
auth_url_base = \
    'https://login.microsoftonline.com/common/oauth2/v2.0/authorize'
fetch_url_base = 'https://graph.microsoft.com/v1.0/'
auth_url = f'{auth_url_base}?client_id={client_id}' \
           f'&scope={scope}&response_type=code&redirect_uri={redirect_uri}'
code_token_headers = {
    'client_id': CONFIG['client_id'],
    'redirect_uri': CONFIG['redirect_uri'],
    'code': None,
    'grant_type': 'authorization_code'
}

CONFIG['auth_url'] = auth_url
CONFIG['code_token_url'] = auth_url
CONFIG['code_token_headers'] = code_token_headers


def get_code(auth_url: str) -> str:
    """Get code"""
    # 1. Auth: Get code
    # - https://docs.microsoft.com/en-us/onedrive/developer/rest-api/getting-started/graph-oauth?view=odsp-graph-online#step-1-get-an-authorization-code
    msg = '2. In "step 1", you should either be asked to ' \
          'log in or auto-logged-in. After that, you should be redirected to ' \
          'a new blank page, and the URL in the address bar should look ' \
          'similar to this: \nhttps://login.live.com/oauth20_desktop.srf?' \
          'code=M.R3_BL2.64370af9-d97a-0e5c-89f8-458184fe1ba8&lc=1033\n\n' \
          'Copy and paste that entire URL here: '
    print('1. Open URL in browser to get auth code: \n', auth_url, '\n')
    url = input(msg)
    parsed = urlparse.urlparse(url)
    code = parse_qs(parsed.query)['code'][0]
    if not code:
        raise RuntimeError('No code found. Url was: ', url)
    return code


def get_token(headers: Dict) -> str:
    """Get token"""
    # 2. redeem token from code
    # - https://docs.microsoft.com/en-us/onedrive/developer/rest-api/getting-started/graph-oauth?view=odsp-graph-online#step-2-redeem-the-code-for-access-tokens
    response: Dict = requests.post(
        'https://login.microsoftonline.com/common/oauth2/v2.0/token',
        data=headers).json()
    return response['access_token']


def download_files(headers: Dict):
    """Download files"""
    # 3. fetch resources
    # - https://docs.microsoft.com/en-us/onedrive/developer/rest-api/api/drive_sharedwithme?view=odsp-graph-online
    # 1. List root files
    # endpoint = 'me/drive/sharedWithMe'
    endpoint = 'me/drive/root/children'
    fetch_url = fetch_url_base + endpoint
    root_items: Dict = requests.get(fetch_url, headers=headers).json()
    if 'error' in root_items.keys():
        raise RuntimeError(root_items)
    root_objs: List[Dict] = root_items['value']
    root_objs: Dict = {
        val['name']: val
        for val in root_objs
    }
    snap_folders = {
        k: v
        for k, v in root_objs.items()
        if re.match('SNAP_TAM_[0-9]{3}', k)
    }
    # Try 1: list & dl (fail)
    # 2. List SNAP folder contents
    # https://docs.microsoft.com/en-us/onedrive/developer/rest-api/api/driveitem_list_children?view=odsp-graph-online
    # snap_folder_contents: Dict = {}
    # endpoint = 'me/drive/items'
    # fetch_url_prefix = fetch_url_base + endpoint
    # for k, v in snap_folders.items():
    #     fetch_url = fetch_url_prefix + '/{}/children'.format(v['id'])
    #     children = requests.get(fetch_url, headers=headers).json()
    #     snap_folder_contents[k] = children
    # 3. Dl files

    # Try 2: straight dl (fail)
    # endpoint = 'me/drive/items/'
    # fetch_url_prefix = fetch_url_base + endpoint
    # for k, v in snap_folders.items():
    #     fetch_url = fetch_url_prefix + '/{}/content'.format(v['id'])
    #     response = requests.get(fetch_url, headers=headers).json()

    # print('Fetch: ' + fetch_url + '\n')
    # pprint(json.dumps(response))

    # Try 3.5: base 64
    # {'error': {'code': 'invalidRequest', 'message': 'Invalid shares key.'
    # for k, v in snap_folders.items():
    #     weburl = v['remoteItem']['webUrl']
    #     ascii_url = weburl.encode('ascii')
    #     base64_url = base64.b64encode(ascii_url)
    #     base64_url = base64_url[0:-1]
    #     # cant replace bytes w/ str:
    #     # encoded_url = base64_url.replace('/', '_').replace('+', '-')
    #     encoded_url = str(base64_url)[2:-1]
    #     fetch_url = fetch_url_prefix + '/{}' \
    #         .format(encoded_url)

    # Try 3: Shares endpoint
    # GET /shares/{shareIdOrUrl}/driveItem?$expand=children
    # - id: {'error': {'code': 'invalidRequest', 'message': 'Bad Argument',
    # 'innerError': ...
    # - remoteItem.id: {'error': {'code': 'invalidRequest', 'message':
    # 'Bad Argument', 'innerError': ...
    # - remoteItem.webUrl: {'error': {'code': 'BadRequest', 'message':
    # "Resource not found for the segment '1drv.ms'.", 'innerError': ...
    # - webUrl: {'error': {'code': 'BadRequest', 'message':
    # "Resource not found for the segment '1drv.ms'.", 'innerError': ...
    # ...
    # 1drv.ms is from webUrls, e.g. https://1drv.ms/u/s!ANBLWsRA6bDCvEk
    snap_folder_contents: Dict = {}
    endpoint = 'shares'
    fetch_url_prefix = fetch_url_base + endpoint
    for k, v in snap_folders.items():
        # fetch_url = fetch_url_prefix + '/{}/driveItem?$expand=children' \
        fetch_url = fetch_url_prefix + '/{}' \
            .format(v['remoteItem']['id'])
            # .format(v['remoteItem']['webUrl'])
        children = requests.get(fetch_url, headers=headers).json()
        snap_folder_contents[k] = children

    print()


def run(config=CONFIG):
    """Run"""
    try:
        headers = config['fetch_headers']
        with open(TOKEN_FILE_PATH, 'r') as file:
            token = file.read()
        headers['Authorization'] = headers['Authorization'].format(token)
        download_files(headers)
    except (RuntimeError, FileNotFoundError):
        # 1. code
        code = get_code(config['auth_url'])
        with open(CODE_FILE_PATH, 'w') as file:
            file.write(code)
        headers = config['code_token_headers']
        headers['code'] = code
        # 2. token
        token = get_token(headers)
        with open(TOKEN_FILE_PATH, 'w') as file:
            file.write(token)
        headers = config['fetch_headers']
        # headers['Authorization'] = headers['Authorization'].format(token)
        headers['Authorization'] = 'Bearer ' + token
        # 3. download
        download_files(headers)


if __name__ == '__main__':
    run()
