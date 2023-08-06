import requests


#get current price
def get_price(api_key, currency, id):
    r = requests.get(f"https://api.nomics.com/v1/currencies/ticker?key={api_key}&ids={id}&interval=1d,30d&convert={currency}&per-page=100&page=1")
    crypto = r.json()
    price = crypto[0]['price']
    return price

#get the full name
def get_name(api_key, id):
    r = requests.get(f"https://api.nomics.com/v1/currencies/ticker?key={api_key}&ids={id}&interval=1d,30d&convert=USD&per-page=100&page=1")
    crypto = r.json()
    name = crypto[0]['name']
    return name

#see when the price was the highest
def get_high(api_key, currency, id):
    r = requests.get(f"https://api.nomics.com/v1/currencies/ticker?key={api_key}&ids={id}&interval=1d,30d&convert={currency}&per-page=100&page=1")
    crypto = r.json()
    high = crypto[0]['high']
    return high

#get the logo url
def get_logo(api_key, id):
    r = requests.get(f"https://api.nomics.com/v1/currencies/ticker?key={api_key}&ids={id}&interval=1d,30d&convert=USD&per-page=100&page=1")
    crypto = r.json()
    logo = crypto[0]['logo']
    return logo

#get the circulating supply
def get_circulating_supply(api_key, id):
    r = requests.get(f"https://api.nomics.com/v1/currencies/ticker?key={api_key}&ids={id}&interval=1d,30d&convert=USD&per-page=100&page=1")
    crypto = r.json()
    circulating_supply = crypto[0]['circulating_supply']
    return circulating_supply

#get the rank
def get_rank(api_key, id):
    r = requests.get(f"https://api.nomics.com/v1/currencies/ticker?key={api_key}&ids={id}&interval=1d,30d&convert=USD&per-page=100&page=1")
    crypto = r.json()
    rank = crypto[0]['rank']
    return rank

#get the market cap
def get_market_cap(api_key, id):
    r = requests.get(f"https://api.nomics.com/v1/currencies/ticker?key={api_key}&ids={id}&interval=1d,30d&convert=USD&per-page=100&page=1")
    crypto = r.json()
    market_cap = crypto[0]['market_cap']
    return market_cap
