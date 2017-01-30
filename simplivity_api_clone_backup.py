#!/usr/bin/python

'''
Basic REST API Clone Client.

USAGE: ./rest_clone_backup.py --ovc <ovc>
                              --username <user>
                              --password <pass>
                              --vm <vm_name>
                              --task backup|clone
                              --number <number>
'''

import argparse
import base64
import requests
import json
import random
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

    parser.add_argument('--vm',
                        required=True,
                        help="Specify the VM name")

    parser.add_argument('--task',
                        required=True,
                        choices=['backup', 'clone'],
                        help="Specify the task to perform")

    parser.add_argument('--number',
                        required=True,
                        type=int,
                        help="Specify number of tasks")

    args = parser.parse_args()

    if not args.password:

        args.password = getpass.getpass(("Please enter the Password for {}: "
                                         .format(args.username)))
    return args

def token_get(args):
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

    return 'Bearer {}'.format(token["access_token"])

def vm_get(args, token):
    '''Retrieve VM data'''

    resource = ('https://{}/api/virtual_machines?show_optional_fields='
                'false&name={}'.format(args.ovc, args.vm))

    headers = {'Accept': 'application/json',
               'Authorization': token}

    request = requests.get(url=resource,
                           headers=headers,
                           verify=False)

    vm_data = request.json()

    return vm_data['virtual_machines'][0]

def vm_post(token, resource, data):
    '''Get VM data'''

    headers = {'Accept': 'application/json',
               'Content-Type': 'application/vnd.simplivity.v1+json',
               'Authorization': token}

    request = requests.post(url=resource,
                            headers=headers,
                            json=data,
                            verify=False)
    return request.json()

def vm_clone(args, token, vm_data, name):
    '''Clone VM'''

    resource = ('https://{}/api/virtual_machines/{}/clone'
                .format(args.ovc, vm_data['id']))

    data = {'app_consistent': 'false',
            'virtual_machine_name': name}

    return vm_post(token, resource, data)

def vm_backup(args, token, vm_data, name):
    '''Backup VM'''

    resource = ('https://{}/api/virtual_machines/{}/backup'
                .format(args.ovc, vm_data['id']))

    data = {'app_consistent': 'false',
            'backup_name': name,
            'destination_id': vm_data['omnistack_cluster_id'],
            'retention': 1}

    return vm_post(token, resource, data)

def main():
    '''Main'''

    args = parse_args()

    token = token_get(args)

    vm_data = vm_get(args, token)

    for dummy in xrange(args.number):

        name = '{}-{}'.format(args.vm,
                              str(random.randint(0, 99999)).zfill(5))

        if args.task == 'clone':
            task = vm_clone(args, token, vm_data, name)
        if args.task == 'backup':
            task = vm_backup(args, token, vm_data, name)

        print json.dumps(task, sort_keys=True, indent=4)

if __name__ == '__main__':

    main()
