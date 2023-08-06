# encoding: utf-8
import requests
import json
import pandas as pd
from .language import tv_languages
from .client import sess, headers


def get_columns():
    return [
        "logoid",
        "name",
        "close",
        "change",
        "change_abs",
        "Recommend.All",
        "volume",
        "market_cap_basic",
        "price_earnings_ttm",
        "earnings_per_share_basic_ttm",
        "number_of_employees",
        "sector",
        "description",
        "name",
        "type",
        "subtype",
        "update_mode",
        "pricescale",
        "minmov",
        "fractional",
        "minmove2",
        "RSI",
        "RSI7"
    ]


def make_query(start, limit, columns=None):
    if columns is None:
        columns = get_columns()
    # "Recommend.All" -0.1 ~ 0.1 中立， 0.1~0.5 买入, 0.5~1 强烈买入
    # Candle.Marubozu.White,Candle.SpinningTop.Black,Candle.EveningStar,Candle.LongShadow.Lower,Candle.LongShadow.Upper,Candle.Hammer,Candle.Doji.Dragonfly,Candle.AbandonedBaby.Bearish,Candle.Harami.Bearish,Candle.Engulfing.Bearish,Candle.Kicking.Bearish,Candle.TriStar.Bearish,Candle.AbandonedBaby.Bullish,Candle.Harami.Bullish,Candle.Engulfing.Bullish,Candle.Kicking.Bullish,Candle.TriStar.Bullish,Candle.SpinningTop.White,Candle.3WhiteSoldiers,Candle.ShootingStar,Candle.Doji.Gravestone,Candle.MorningStar,Candle.Doji,Candle.Marubozu.Black,Candle.InvertedHammer,Candle.HangingMan

    query = {
        "filter": [
            {
                "left": "market_cap_basic",
                "operation": "nempty"
            },
            {
                "left": "type",
                "operation": "in_range",
                "right": [
                    "stock",
                    "dr",
                    "fund"
                ]
            },
            {
                "left": "subtype",
                "operation": "in_range",
                "right": [
                    "common",
                    "",
                    "etf",
                    "unit",
                    "mutual",
                    "money",
                    "reit",
                    "trust"
                ]
            },
            {
                "left": "exchange",
                "operation": "in_range",
                "right": [
                    "NYSE",
                    "NASDAQ",
                    "AMEX"
                ]
            },
            {
                "left": "price_earnings_ttm",
                "operation": "less",
                "right": 80
            },
            {
                "left": "RSI",
                "operation": "less",
                "right": 65
            },
            {
                "left": "RSI",
                "operation": "greater",
                "right": 45
            },
            {
                "left": "RSI7",
                "operation": "greater",
                "right": 50
            }, {"left": "SMA10", "operation": "egreater", "right": "SMA20"}

            # , {"left":"SMA10","operation":"crosses_above","right":"SMA20"}

            # , {
            #     "left": "Candle.Marubozu.White,Candle.SpinningTop.Black,Candle.EveningStar,Candle.LongShadow.Lower,Candle.LongShadow.Upper,Candle.Hammer,Candle.Doji.Dragonfly,Candle.AbandonedBaby.Bearish,Candle.Harami.Bearish,Candle.Engulfing.Bearish,Candle.Kicking.Bearish,Candle.TriStar.Bearish,Candle.AbandonedBaby.Bullish,Candle.Harami.Bullish,Candle.Engulfing.Bullish,Candle.Kicking.Bullish,Candle.TriStar.Bullish,Candle.SpinningTop.White,Candle.3WhiteSoldiers,Candle.ShootingStar,Candle.Doji.Gravestone,Candle.MorningStar,Candle.Doji,Candle.Marubozu.Black,Candle.InvertedHammer,Candle.HangingMan",
            #     "operation": "equal",
            #     "right": 1
            # }
        ],
        "filter2": {
            "operator": "and",
            "operands": [
                {
                    "operation": {
                        "operator": "or",
                        "operands": [
                            {
                                "expression": {
                                    "left": "Recommend.All",
                                    "operation": "in_range",
                                    "right": [
                                        -0.1,
                                        0.1
                                    ]
                                }
                            },
                            {
                                "expression": {
                                    "left": "Recommend.All",
                                    "operation": "in_range",
                                    "right": [
                                        0.1,
                                        0.5
                                    ]
                                }
                            },
                            {
                                "expression": {
                                    "left": "Recommend.All",
                                    "operation": "in_range",
                                    "right": [
                                        0.5,
                                        1
                                    ]
                                }
                            }
                        ]
                    }
                }
            ]
        },
        "options": {
            "lang": "zh"
        },
        "symbols": {
            "query": {
                "types": []
            },
            "tickers": []
        },
        "columns": columns,
        "sort": {
            "sortBy": "market_cap_basic",
            "sortOrder": "desc"
        },
        "range": [
            start,
            limit
        ]
    }
    return query


def scan_from_tradingview(market, start=0, limit=2000, query=None):
    m = {
        "US": "america",
        "HK": "hongkong",
        "CN": "china"
    }
    if market not in m:
        return

    url = "https://scanner.tradingview.com/{}/scan".format(m[market])

    columns = get_columns()
    if query is None:
        query = make_query(start, limit, columns)

    r = requests.post(url, data=json.dumps(query), headers={
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "referrer": "https://cn.tradingview.com/",
    })

    if r.status_code == 200:
        rj = r.json()
        if rj['data']:
            # from language import tv_languages
            zh = tv_languages['zh']

            result = []
            for x in r.json()['data']:
                s, d = x['s'], x['d']
                d1 = [zh[x] if x in zh else x for x in d]
                result.append(d1)

            df = pd.DataFrame(result, columns=columns)
            return df
    return pd.DataFrame([], columns=columns)


def scan_from_xueqiu(market="CN", limit=3000):
    url1 = ""

    pct_limit = [-5, 200]
    params = {
        'category': market,
        'exchange': 'sh_sz',
        'areacode': '',
        'indcode': '',
        'order_by': 'symbol',
        'order': 'desc',
        'page': '1',
        'size': limit,
        'only_count': '0',
        'current': '',
        'pct': '{}_{}'.format(pct_limit[0], pct_limit[1]),
        'pct5': '{}_{}'.format(pct_limit[0], 1000),
        'pettm': '0_100',  # 市盈率
        'mc': '1000000000_2546262692688',
        'amount': '50000000_8102580631',
        'pct120': '5_1603.05',  # 120天涨跌
        'tr': '0_5',  # 换手率 turnover
        '_': '1615741315407'
    }
    if market == "CN":
        params['exchange'] = "sh_sz"
    elif market == "HK":
        pass

    url1 = "https://xueqiu.com/service/screener/screen"
    r = sess.get(url1, params=params, headers=headers)

    info = r.json()
    d = info['data']
    items = d['list']
    return items
