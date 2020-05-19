import os
import time
import json
import requests

from selenium import webdriver
from tenacity import retry, wait_exponential, wait_fixed, stop_after_attempt

import pandas as pd
from io import BytesIO
from xlrd import XLRDError


CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
CHROME_PATH = os.path.join(CURRENT_PATH, '../drivers/chromedriver.exe')
DATA_PATH = os.path.join(CURRENT_PATH, '../data/')
CACHED_HEADERS = os.path.join(DATA_PATH, 'cached_headers.json')


if not os.path.exists(CHROME_PATH):
    raise Exception('Require selenium chromedriver')


def get_cookie_text(br):
    cookies = br.get_cookies()
    _extract = lambda c: '{}={}'.format(c['name'], c['value'])
    cookie_text = '; '.join([_extract(c) for c in cookies])
    return cookie_text


def compose_headers(cookie_text):
    return {'Cookie': cookie_text}


def get_new_headers():
    br = webdriver.Chrome(CHROME_PATH)
    br.get('http://www.macmap.org/')
    time.sleep(5)

    standby_url = ('http://www.macmap.org/QuickSearch/CompareTariffs/'
                   'CompareTariffs.aspx?subsite=open_access')
    br.get(standby_url)
    time.sleep(5)

    headers = compose_headers(get_cookie_text(br))
    br.quit()
    return headers


def save_cached_headers(headers):
    with open(CACHED_HEADERS, 'w') as f:
        f.write(json.dumps(headers))


def fetch_tariff_excel_response(product, country_iso, headers):
    url = ('http://www.macmap.org/QuickSearch/CompareTariffs/'
           'CompareTariffsResults.aspx?'
           'download=1&contenttype=application/msexcel'
           '&product={}&country={}&isimporter=0').format(product,
                                                         country_iso)
    res = requests.get(url, headers=headers)
    return res


def check_headers_available(headers):
    product = '854239'
    country_iso = '490'
    res = fetch_tariff_excel_response(product, country_iso, headers)
    df = pd.read_excel(BytesIO(res.content))
    try:
        assert len(df) > 0
        return True
    except:
        return False


@retry(stop=stop_after_attempt(10),
       wait=wait_fixed(10) + wait_exponential(multiplier=1, max=20))
def reload_available_headers():
    headers = get_new_headers()
    headers_is_available = check_headers_available(headers)
    if headers_is_available:
        return headers
    else:
        raise


def get_decent_headers():
    try:
        with open(CACHED_HEADERS, 'r') as f:
            headers = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        headers = reload_available_headers()
        save_cached_headers(headers)
    return headers


def save_origin_excel(res, product, country_iso):
    product = product.zfill(6)
    country_iso = country_iso.zfill(3)

    folder = 'exporter-view/{}/{}'.format(product[:2], country_iso)
    excel = 'tariff-{}-export-{}.xlsx'.format(country_iso, product)

    folder_path = os.path.join(DATA_PATH, folder)
    excel_path = os.path.join(folder_path, excel)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    with open(excel_path, 'wb') as f:
        f.write(res.content)


@retry(stop=stop_after_attempt(10))
def download_tariff_excel(product, country_iso, headers):
    res_is_available = False
    while not res_is_available:
        try:
            res = fetch_tariff_excel_response(product, country_iso, headers)

            # check res.content available or not
            df = pd.read_excel(BytesIO(res.content))
            res_is_available = True
        except XLRDError:
            headers = reload_available_headers()
            save_cached_headers(headers)

    save_origin_excel(res, product, country_iso)
