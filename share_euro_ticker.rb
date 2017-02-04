#!/usr/bin/ruby

require 'net/http'
require 'json'

def get_share_price(symbol)
    # Retrieve share price

    resource = 'http://download.finance.yahoo.com/d/quotes.csv' \
               '?s=' + symbol + '&f=sl1d1t1c1ohgv&e=.csv&columns=price'

    request = Net::HTTP.get(URI(resource))

    return request.split(",")[1]

end

def get_exchange_rate()
    # Retrieve exchange rate data

    resource = 'https://api.fixer.io/latest?symbols=USD'

    request = Net::HTTP.get(URI(resource))

    return JSON.parse(request)['rates']['USD']

end

def get_island_fund()
    # Calculate island fund

    symbol = 'YHOO'

    price = get_share_price(symbol).to_f

    euro = get_exchange_rate().to_f

    if ARGV[0]
        number_of_shares = ARGV[0].to_f
        return "Island Fund = €#{((price / euro) * number_of_shares).round(2)}"
    else
        return "Island Fund = €#{(price / euro).round(2)}"
    end

end

puts get_island_fund()
