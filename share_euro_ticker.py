#!/usr/bin/env python3

'''
Calculate share price and convert to Euros.
'''

import argparse
import requests

def parse_args():
    '''Parse command line arguments'''

    parser = argparse.ArgumentParser()

    parser.add_argument('--symbol',
                        required=True,
                        help="Specify symbol")

    parser.add_argument('--shares',
                        required=False,
                        help="Specify number of shares")

    return parser.parse_args()

def get_share_price(symbol):
    '''Retrieve share price'''

    resource = ('http://download.finance.yahoo.com/d/quotes.csv'
                '?s=' + symbol +'&f=sl1d1t1c1ohgv&e=.csv&columns=price')

    request = requests.get(url=resource)

    return request.text.split(",")[1]

def get_exchange_rate():
    '''Retrieve exchange rate'''

    resource = 'https://api.fixer.io/latest?symbols=USD'

    request = requests.get(url=resource)

    return request.json()['rates']['USD']

def get_island_fund():
    '''Calculate island fund'''

    args = parse_args()

    price = float(get_share_price(args.symbol))

    euro = float(get_exchange_rate())

    if args.shares:
        shares = float(args.shares)
        return 'Island Fund = €{:.2f}'.format((price / euro) * shares)
    else:
        return 'Island Fund = €{:.2f}'.format(price / euro)

print(get_island_fund())
