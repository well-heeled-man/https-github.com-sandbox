#!/usr/bin/python3

'''
Simple byte converter for reuse elsewhere.
'''

import sys

def get_human_readable(byte_value):
    ''' Convert byte value to human readable value '''

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

def main():
    ''' Main '''

    try:
        byte_value = sys.argv[1]
    except IndexError:
        byte_value = input('Please enter the size in bytes: ')

    try:
        print(get_human_readable(byte_value))
    except ValueError:
        print('Please enter a numerical value!')

if __name__ == '__main__':

    main()
