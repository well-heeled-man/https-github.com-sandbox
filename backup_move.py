#!/usr/bin/env python
'''
This script will VMs from one datacentre to another, VM-by-VM.

USAGE: ./backup_move.py

Scott Harrison (scott.harrison@hpe.com)
'''

import argparse
import subprocess
import sys
import xml.etree.ElementTree as etree

def parse_args():
    '''Parse command line arguments'''

    parser = argparse.ArgumentParser()

    parser.add_argument('--vm',
                        required=True,
                        help="Specify the VM name")

    parser.add_argument('--datastore',
                        required=True,
                        help="Specify the source datastore")

    parser.add_argument('--source_cluster',
                        required=True,
                        help="Specify the source cluster")

    parser.add_argument('--destination_cluster',
                        required=True,
                        help="Specify the destination cluster")

    return parser.parse_args()

class Parameter(object):
    '''Create Parameter dictionary and strip UUIDs'''

    def __init__(self, name):
        self.name = name
        self.value = []

    def __len__(self):
        return len(self.value)

    def __getitem__(self, key):
        return self.value[key]

    def add(self, line):
        '''Strip XML and append to a list'''
        xml = etree.fromstring(line)
        value = etree.tostring(xml, encoding='UTF-8', method='text')
        self.value.append(value)

def enumerate_backups(vm, datastore):
    '''Use svt-backup-show to enumerate backups'''

    command = subprocess.check_output(['svt-backup-show',
                                       '--vm', vm,
                                       '--datastore', datastore,
                                       '--output', 'xml',
                                       '--max-results', '25000'])
    temp = command.splitlines()

    virtual_machine = Parameter('virtual_machine')
    backup = Parameter('backup')
    datastore = Parameter('datastore')

    for line in temp:

        if 'hiveName' in line: virtual_machine.add(line)
        elif 'name'   in line: backup.add(line)
        elif 'dsId'   in line: datastore.add(line)

    return (virtual_machine, backup, datastore)

def move_backup(args):
    '''Calculate backup unique bytes'''

    virtual_machine, backup, datastore = enumerate_backups(args.vm, args.datastore)

    splice = zip(virtual_machine, backup, datastore)
    length = len(splice)

    for index, (virtual_machine,
                backup,
                datastore) in enumerate(splice, start=1):
        try:
            print "* Copying {}({}) backup {} of {}".format(backup, virtual_machine, index, length)

            subprocess.check_output(['svt-backup-copy',
                                     '--vm', virtual_machine,
                                     '--backup', backup,
                                     '--datastore', datastore,
                                     '--src-cluster', args.source_cluster,
									 '--dst-cluster', args.destination_cluster])

        except subprocess.CalledProcessError as error:
            pass

if __name__ == '__main__':

    ARGS = parse_args()

    move_backup(ARGS)
