# encoding: utf-8
import time
import pandas as pd
import requests
import re
import json
import numpy as np
from .caches import default_cache
from .enums import Period
from .scorer import up_trend_ma
from .client import sess, headers
from .filters import scan_from_xueqiu



def get_bar(symbol, bars=284, period=None, cache=default_cache):
    """
    @param period Period.DAY
    @return
    """
    key = symbol
    if period is None:
        period = Period.DAY

    if cache.has(key) and cache.get(key) is not None:
        return cache.get(key)

    tts = int(time.time() * 1000)
    url1 = "https://stock.xueqiu.com/v5/stock/chart/kline.json?symbol={}&begin={}&period={}&type=before&count={}&indicator=kline,pe,pb,ps,pcf,market_capital,agt,ggt,balance,rsi".format(
        symbol.upper(), tts, period, -bars)
    r = sess.get(url1, headers=headers)
    rj = r.json()
    d = rj['data']
    if 'column' not in d:
        return None

    df = pd.DataFrame(columns=d['column'], data=d['item'])
    if df.empty:
        return df

    df['date'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.index = df['date']

    cache.set(key, df, ttl=40000)
    return df


def get_symbols(market="US", limit=300, cache=default_cache):
    if cache.has(market):
        return cache.get(market)

    if market == "CN":
        return scan_from_xueqiu(market, limit)

    url1 = "https://xueqiu.com/service/screener/screen?category={}&indcode=&order_by=symbol&order=desc&page=1&size={}&only_count=0&current=1_370500&pct=&mc=10_2196554480640&amount=10000000_12764323155.69&_=1613632436617".format(
        market, limit)
    r = sess.get(url1, headers=headers)
    info = r.json()
    d = info['data']
    items = d['list']
    cache.set(market, items, ttl=10000)
    return items


def get_ind_category(market):
    key = "xueqiu:categories_{}".format(market)
    content = default_cache.get(key)
    if content:
        return content 

    url = "https://xueqiu.com/service/screener/industries?category={}&_=1615879508304".format(market)
    r = sess.get(url, headers=headers)
    rj = r.json()
    categories = dict()
    if rj and rj['data']['industries']:
        for x in rj['data']['industries']:
            categories[x['encode']] = x['name']
            default_cache.set(key, categories, ttl=86400)

    return categories


def get_china_symbols_us_market():
    """
    """
    url1 = 'https://xueqiu.com/service/v5/stock/screener/quote/list?page=1&size=600&order=desc&orderby=percent&order_by=percent&market=US&type=us_china&_=1613792930558'
    r = sess.get(url1, headers={"user-agent": "maro"})
    info = r.json()
    d = info['data']
    items = d['list']
    return items


def get_base_info(symbol, cache=default_cache):
    key = "ext_{}".format(symbol)
    if cache.has(key):
        try:
            str_data = cache.get(key)
            return json.loads(data)
        except:
            pass

    r = sess.get("https://xueqiu.com/s/{}".format(symbol),
                 headers={"user-agent": "maro"})
    data = [x for x in r.text.split("\n") if "high52w\"" in x]
    if data:
        data = "".join(data)
    if "quote:" in data:
        data = data.replace('    quote: ', '')[:-1]

    cache.set(key, data, ttl=40000)
    try:
        return json.loads(data)
    except Exception:
        pass
    return data


def get_symbol_score(symbol, df, market="US", extra=None, is_debug=1):
    if len(df) < 3:
        return

    d3, d2, d1 = df.iloc[-3], df.iloc[-2], df.iloc[-1]

    score = 0
    rules = []

    item = dict(
        symbol=symbol,
        score=0,
        priceUp=0,
        volumeUp=0,
        market=market,
        ma5Count=0,
        high52w=0,
        volumeBurst=0,
        name="",
    )

    for _p, x in enumerate(df['percent'][::-1]):
        if x < 0:
            break 
        score = 10
        if _p >= 10:
            score = 2
        item['score'] += score
        item['priceUp'] += score

    sub1 = df[-10:]
    # 阳线加分
    for o1, c1, h1, l1 in list(zip(
        sub1['open'], sub1['close'], sub1['high'], sub1['low']
    ))[::-1]:
        if o1 >= c1:
            break 
        item['score'] += 2
        item['priceUp'] += 2

        # 实体阳线+3
        if (h1 - c1) < 0.2 * h1 - l1:
            item['score'] += 3
            item['priceUp'] += 3


    if df['volume'][-10:].min() >= 300000:
        # 必须基础量够高才能计算爆量

        for vv in df['volume'].pct_change()[::-1][:10]:
            if vv < 0:
                break
            score = 5
            if vv > 50:
                score = 50
                item['volumeBurst'] += score
            elif vv > 30:
                score = 30
                item['volumeBurst'] += score
            elif vv > 20:
                score = 20
                item['volumeBurst'] += score
            elif vv > 10:
                score = 10
                item['volumeBurst'] += score
                
            item['score'] += score
            item['volumeUp'] += score
            rules.append("volume continue up")


    for c1, mean1 in list(zip(df['close'], df['close'].rolling(5).mean()))[::-1]:
        if mean1 is np.nan or mean1 > c1:
            break 
        item['score'] += 2
        item['ma5Count'] += 2

    rsi_score = len(df['rsi1'][-10:][df.rsi1 > 50]) * 5
    item['score'] += rsi_score
        

    if item['score'] >= 20:
        # data = [x for x in r.text.split("\n") if "high52w\"" in x]
        data = get_base_info(symbol)
        if data and 'high52w' in data:
            section_high = df[-5:]['high'].max()
            w52high = data['high52w']
            if df.iloc[-1]['high'] == w52high:
                item['high52w'] = 15
                item['score'] += 15
            elif section_high >= w52high and section_high * 0.95 <= w52high:
                item['high52w'] = 15
                item['score'] += 15
            
            
        if data and 'name' in data:
            item['name'] = data['name']

    ic_info = get_ind_category(market)
    for keyk in ["pettm", "current", "tr", "pct120", "mc", "indcode"]:
        if extra is not None and keyk in extra:
            item[keyk] = extra[keyk]

            if keyk == "mc":
                item[keyk] = "{:.3f}".format(extra[keyk]/100000000)
            if keyk == "indcode" and ic_info:
                item[keyk] = ic_info.get(item[keyk], "-")
        

    dd = pd.DataFrame([item], index=[symbol])
    dd.index = dd['symbol']
    if extra is not None and not dd['name'][0]:
        dd['name'] = extra['name']
    
    up_score = up_trend_ma(df)
    if up_score > 0 and item['priceUp'] < up_score:
        pup = item['priceUp'] 
        item['score'] = item['score'] - pup + up_score
        item['priceUp'] = pup

    if item['score'] > 100 and is_debug is not None:
        pd.set_option("display.width", 2000)
        print(dd)

    return dd


def scan_list(market, limit=2000):
    items = get_symbols(market, limit)
    result = pd.DataFrame()
    for row in items:
        bars = get_bar(row['symbol'])
        r = get_symbol_score(row['symbol'], bars, market, extra=row)
        if r is not None:
            result = result.append(r)
    return result


def scan_us_list(limit=2000):
    return scan_list("US", limit)


def scan_hk_list(limit=2000):
    return scan_list("HK", limit)


def scan_cn_list(limit=2000):
    return scan_list("CN", limit)

