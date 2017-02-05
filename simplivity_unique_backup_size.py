#!/usr/bin/env python
'''
This script will calculate the unique bytes associated with backups.

USAGE: ./calculateUniquebackupSize.py
USAGE: ./calculateUniquebackupSize.py '<datacenterName>'

For any issues, contact Scott Harrison (scott.harrison@simplivity.com).
'''
# pylint: disable=multiple-statements

import subprocess
import sys
import xml.etree.ElementTree as etree

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
        uuid = etree.tostring(xml, encoding='UTF-8', method='text')
        self.value.append(uuid)

def enumerate_backups():
    '''Use svt-backup-show to enumerate backups'''

    try:

        datacenter = sys.argv[1]
        command = subprocess.check_output(['svt-backup-show', '--output', 'xml',
                                           '--max-results', '25000',
                                           '--datacenter', datacenter])
    except IndexError:

        command = subprocess.check_output(['svt-backup-show', '--output', 'xml',
                                           '--max-results', '25000'])
    temp = command.splitlines()

    virtual_machine = Parameter('virtual_machine')
    backup = Parameter('backup')
    datastore = Parameter('datastore')
    datacenter = Parameter('datacenter')

    for line in temp:

        if 'hiveId' in line: virtual_machine.add(line)
        elif 'id'   in line: backup.add(line)
        elif 'dsId' in line: datastore.add(line)
        elif 'dcId' in line: datacenter.add(line)

    return (virtual_machine, backup, datastore, datacenter)

def calculate_unique_size():
    '''Calculate backup unique bytes'''

    virtual_machine, backup, datastore, datacenter = enumerate_backups()

    splice = zip(virtual_machine, backup, datastore, datacenter)
    length = len(splice)

    for index, (virtual_machine,
                backup,
                datastore,
                datacenter) in enumerate(splice, start=1):
        try:
            subprocess.check_output(['svt-backup-size-calculate', '--force',
                                     '--vm', virtual_machine,
                                     '--backup', backup,
                                     '--datastore', datastore,
                                     '--datacenter', datacenter])

        except subprocess.CalledProcessError as error:

            print "Command: {}".format(str(error.cmd))
            print "Returned with error code: {}".format(error.returncode)

        print "* Calculating {} of {}".format(index, length)

def main():
    '''Main'''

    calculate_unique_size()

if __name__ == '__main__':

    main()
