#!/usr/bin/env python
'''
This script uses the ESXi utility vscsiStats.
It collects disk statistics for all VMDKs attached to all VMs.
The data is output a series of GZIP'ed files.
These need additional processing to be useful.

USAGE: ./getVscsiStats.py -i <interval> -s <samples>

It requires get_vscsis_stats_processor.sh to process the data. It is currently a WIP and
allcode is being ported to Python in a single script.

For any issues, contact Scott Harrison (scott.harrison@simplivity.com).
'''

import argparse
import gzip
import socket
import subprocess
import sys
import threading
import time

def parse_cli_args():
    '''Parse command line args'''

    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--interval',
                        required=True,
                        type=int,
                        help='Collection Interval in Seconds')

    parser.add_argument('-s', '--samples',
                        required=True,
                        type=int,
                        help='Total number of Samples')

    args = parser.parse_args()

    return args

def collect_process():
    '''Collect and process data, outputting the result to text file'''

    data = subprocess.check_output(["vscsiStats", "-p", "all", "-c"])
    data = data.splitlines(True)

    subprocess.check_output(["vscsiStats", "-r"])

    file_name = "vscsiStats_{}_{}.gz".format(socket.gethostname(),str(int(time.time())))

    exclude = ('min', 'max', 'mean', 'count', 'Frequency')

    with gzip.GzipFile(file_name, "w") as output:
        for line in data:
            if not any(word in line for word in exclude):
                output.write(line)

def runtime(args):
    '''Run the collection'''

    with open("vscsiStatsConfig.txt", "w") as config:
        config.write(subprocess.check_output(["vscsiStats", "-l"]))

    subprocess.check_output(["vscsiStats", "-x"])
    subprocess.check_output(["vscsiStats", "-s"])

    for _ in xrange(args.samples):
        time.sleep(args.interval)
        thread_collect_process = threading.Thread(target=collect_process())
        thread_collect_process.start()

    subprocess.check_output(["vscsiStats", "-x"])

def main():
    '''Main'''

    args = parse_cli_args()

    duration = round((float(args.samples) * float(args.interval) / 3600), 4)

    print 'This will collect data for {} hours'.format(duration)

    enter = raw_input("Press ENTER to start or any other key to exit: ")

    if enter == '':
        runtime(args)
    else:
        print "Aborting collection."
        sys.exit()

if __name__ == '__main__':

    main()
