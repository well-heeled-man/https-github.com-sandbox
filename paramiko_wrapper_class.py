#!/usr/bin/python

'''
Basic SSH and SFTP client.
'''
# pylint: disable=line-too-long

import paramiko
import time

class ClientConnect(object):
    '''Instantiate a connection class'''

    def __init__(self, connection_string, ssh=None, sftp=None):
        '''Instantiate a connection instance, with parameters'''

        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(hostname=connection_string[0],
                            username=connection_string[1],
                            password=connection_string[2],
                            timeout=30, compress=True)
        if ssh:

            self.ssh = self.client.invoke_shell()
            self.buffer = '65536'

            data = self.ssh.recv(self.buffer)
            del data

        if sftp:

            self.sftp = self.client.open_sftp()

    @staticmethod
    def sftp_progress(transferred, total):
        '''Print transfer progress'''

        transferred = ClientConnect.human_readable(transferred)
        total = ClientConnect.human_readable(total)
        print "{}* {}  of {}{}".format('\r', transferred, total, 5*' '),

    @staticmethod
    def human_readable(byte_value):
        '''Convert byte value to human readable value'''

        value = float(byte_value)

        kilobyte = value / 1000
        megabyte = value / 1000**2
        gigabyte = value / 1000**3
        terabyte = value / 1000**4

        if kilobyte < 1:
            return "{} B".format(byte_value)
        elif megabyte < 1:
            return "{:.2f} KB".format(kilobyte)
        elif gigabyte < 1:
            return "{:.2f} MB".format(megabyte)
        elif terabyte < 1:
            return "{:.2f} GB".format(gigabyte)
        else:
            return "{:.2f} TB".format(terabyte)

    def run_command(self, command):
        '''Run command via SSH'''

        self.ssh.sendall('{}{}'.format(command, '\n'))
        time.sleep(5)

        data = []
        while self.ssh.recv_ready():
            data += self.ssh.recv(self.buffer)

        return data

    def file_get(self, remote_file, local_file):
        '''GET remote file via SFTP'''

        self.sftp.get(remote_file, local_file, callback=self.sftp_progress)

    def file_put(self, local_file, remote_file):
        '''PUT local file via SFTP'''

        self.sftp.put(local_file, remote_file, callback=self.sftp_progress)

    def file_change_permissions(self, remote_file, permissions):
        '''Change permissions on file via SFTP'''

        self.sftp.chmod(remote_file, permissions)

    def close_client(self):
        '''Close connection instance'''

        self.client.close()

def main():
    '''Main'''

    connection_string = ['127.0.0.1', '<username>', '<password>']

    connection = ClientConnect(connection_string, ssh=True, sftp=True)

    commands = ['ifconfig', 'hostname', 'whoami']

    with open('output.txt', 'w') as output:

        for command in commands:
            data = connection.run_command(command)
            print ''.join(data)
            output.write(''.join(data))

    connection.file_put('output.txt', '<destination>/output.txt')

    connection.file_change_permissions('<destination>/output.txt', 777)

    connection.close_client()

if __name__ == '__main__':

    main()
