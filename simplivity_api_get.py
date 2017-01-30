#!/usr/bin/env python

'''
Basic REST API Query Client.

USAGE: ./api_get.py -ovc <ovc> --username <username> --password <password>
'''

import argparse
import base64
import requests
import json
import getpass

# Disable SSL warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def parse_args():
    '''Parse command line arguments'''

    parser = argparse.ArgumentParser()

    parser.add_argument('--ovc',
                        required=True,
                        help="Specify the OVC to connect to")

    parser.add_argument('--username',
                        required=True,
                        help="Specify the username")

    parser.add_argument('--password',
                        required=False,
                        help="Specify the password")

    args = parser.parse_args()

    if not args.password:

        args.password = getpass.getpass(("Please enter the Password for {}: "
                                         .format(args.username)))
    return args

def get_token(args):
    '''Retrieve access token'''

    resource = ('https://{}/api/oauth/token'
                .format(args.ovc))

    headers = {'Accept': 'application/json',
               'Authorization': ('Basic {}'
                                 .format(base64.b64encode('simplivity:')))}

    creds = {'grant_type': 'password',
             'username': args.username,
             'password': args.password}

    request = requests.post(url=resource,
                            headers=headers,
                            data=creds,
                            verify=False)
    token = request.json()
    token = 'Bearer {}'.format(token["access_token"])

    return token

def get_data(args, token, api_call):
    '''Retrieve VM data'''

    headers = {'Accept': 'application/json',
               'Authorization': token}

    resource = 'https://{}/api/{}'.format(args.ovc, api_call)

    request = requests.get(url=resource,
                           headers=headers,
                           verify=False)
    data = request.json()

    return data

def main():
    '''Main'''

    args = parse_args()

    token = get_token(args)

    api_calls = [
        'virtual_machines',
        'hosts',
        'datastores',
        'backups',
        'policies',
        ]

    for api_call in api_calls:

        with open(api_call + '_api.json', 'w+') as output:

            data = get_data(args, token, api_call)
            data = json.dumps(data, sort_keys=True, indent=4)

            output.write(data)

if __name__ == '__main__':

    main()
