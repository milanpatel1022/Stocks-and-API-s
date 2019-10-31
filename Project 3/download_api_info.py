#Milan Patel 47449770

import json
import urllib.parse
import urllib.request

#no api key required to use IEX
BASE_IEX_URL = 'https://api.iextrading.com/1.0'


def info_to_download(num_days: int) -> str:
    ''' According to number of days stock info is wanted, provide query parameter that will download sufficient amount of data'''
    #if user wants data for 10 days, download 1 months worth of data and get the last 10 days
    #if user wants data for 40 days, download 3 months worth of data and get the last 40 days
    #if user wants data for 300 days, download 1 year worth of data and get the last 300 days
    #so on and so forth
    if num_days < 30:
        info = '3m'
    elif num_days < 60:
        info = '6m'
    elif num_days < 150:
        info = '1y'
    elif num_days < 300:
        info = '2y'
    elif num_days < 1000:
        info = '5y'
    return info
    

def build_search_url(stock: str, info: str) -> str:
    '''Build url to get all pricing and volume info on stocks'''
    return BASE_IEX_URL + (f'/stock/{stock}/chart/{info}')


def try_url(url: str) -> bool:
    '''checks to see if the stock symbol is valid by checking if url opens'''
    response = None
    try:
        response = urllib.request.urlopen(url)
        return True
    except:
        print('Invalid stock symbol')
        return False
    finally:
        if response != None:
            response.close()


def get_company_name(stock: str) -> str:
    '''Build url to get the company name of stock'''
    url = BASE_IEX_URL + (f'/stock/{stock}/company')
    response = urllib.request.urlopen(url)
    json_text = response.read().decode(encoding = 'utf-8')
    response.close()
    return json.loads(json_text)['companyName']


def get_total_existing_shares(stock: str) -> str:
    '''Build url to get the total number of shares of the stock exist'''
    url = BASE_IEX_URL + (f'/stock/{stock}/stats')
    response = urllib.request.urlopen(url)
    json_text = response.read().decode(encoding = 'utf-8')
    response.close()
    return json.loads(json_text)['sharesOutstanding']
        

def stock_info(url: str) -> dict:
    '''Obtains pricing/volume info on stock from url in json format'''
    response = urllib.request.urlopen(url)
    json_text = response.read().decode(encoding = 'utf-8')
    response.close()
    return json.loads(json_text)

