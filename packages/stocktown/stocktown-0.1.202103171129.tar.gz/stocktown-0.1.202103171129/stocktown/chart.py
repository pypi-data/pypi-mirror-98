# encoding: utf-8

__version__ = "0.1.0"
import requests
import re
from IPython.display import display, HTML, Image
from .caches import default_cache


def query_eastmoney_id(symbol, market=None):
    sugg = "http://searchapi.eastmoney.com/api/suggest/get?&input={}&type=14&token=D43BF722C8E33BDC906FB84D85E326E8&count=6".format(
        symbol)

    if market == "US":
        sugg += "&markettype=7"
    elif market == "HK":
        sugg += "&markettype=5"

    r = requests.get(sugg)
    j = r.json()

    if not j['QuotationCodeTable']['Data']:
        return symbol

    for item in j['QuotationCodeTable']['Data']:
        if item['Code'] == symbol:
            mkt = item['MktNum']
            return "{}.{}".format(mkt, symbol)
    return symbol


def eastmoney_image(symbol, market=None, show=True):
    item_id = query_eastmoney_id(symbol, market)

    image = "http://webquoteklinepic.eastmoney.com/GetPic.aspx?token=44c9d251add88e27b65ed86506f6e5da&nid={}&type=&unitWidth=-6&ef=&formula=RSI&imageType=KXL&_=1614437126202".format(
        item_id)
    i = Image(url=image)
    if show:
        display(i)
    return i


def init_stockchart():
    url = "https://stockcharts.com/h-sc/ui"
    body = {'nIndicators': '3',
            'nOverlays': '3',
            'nMaxOverlays': '3',
            'nMaxIndicators': '3',
            'predefChanged': 'false',
            'isPermanentId': 'false',
            'setPermanentId': 'false',
            'defaultChart': 'true',
            'chartId': '',
            'style': '',
            'dataTotalDays': '0',
            'inputsymbol': 'TSLA',
            'originalsymbol': 'TSLA',
            'inputperiod': 'D',
            'originalperiod': 'D',
            'currentSetting': '0|||',
            'curCustomSetting': '0|||',
            'customSettingsCount': '0',
            'curChartList': '',
            'curChartListName': '',
            'curChartName': '',
            'curChartNameIndex': '0',
            'isDeveloper': 'false',
            'companyname': 'Tesla+Inc.',
            'ipaddress': '149.129.97.51',
            'chartcode': '',
            'skinColorPageBg': 'ffffff',
            'skinColorGridBg': 'ffffff',
            'skinColorGridBgStripe': '',
            'skinColorBorder': 'C7C7C7',
            'skinColorText': '000000',
            'skinColorCandles': '000000',
            'chartString': 's=TSLA&p=D&b=5&g=0&id=0&r=1615646364094',
            'symbol': 'TSLA',
            'period': 'D',
            'period2': 'D',
            'dataRange': 'fill',
            'bar': '5',
            'gap': '0',
            'bars-fill': '',
            'years': '0',
            'months': '6',
            'days': '0',
            'bars-predef': '',
            'start': '',
            'end': '',
            'bars-userdef': '',
            'symStyle': 'type="candle"',
            'renkoUnit': 'atr',
            'renkoBoxSize': '14',
            'renkoPriceField': 'close',
            'kagiUnit': 'atr',
            'kagiReversal': '14',
            'kagiPriceField': 'hilo',
            'chartSize': '700',
            'customWidth': '700',
            'customHeight': '530',
            'chartSkin': 'default',
            'symUpColor': '1',
            'symDownColor': '2',
            'legend': 'DEFAULT',
            'showVolume': 'overlay',
            'dataLog': 'true',
            'solidCandles': 'true',
            'dataSignalV': 'sig',
            'antiAliasOn': 'true',
            'axisLabels': 'true',
            'overType_': 'B',
            'overArgs_': '',
            'overType_0': 'SMA',
            'overArgs_0': '50',
            'overType_1': 'SMA',
            'overArgs_1': '200',
            'overType_2': 'B',
            'overArgs_2': '',
            'indType_': 'B',
            'indArgs_': '',
            'indLoc_': 'below',
            'indType_0': 'RSI',
            'indArgs_0': '14',
            'indLoc_0': 'above',
            'indType_1': 'MACD',
            'indArgs_1': '12,26,9',
            'indLoc_1': 'below',
            'indType_2': 'B',
            'indArgs_2': '',
            'indLoc_2': 'below',
            'syncHeight': ''}
    r = requests.post(url, headers={
        "referrer": "https://stockcharts.com/h-sc/ui",
        "user-agent": "mori",
    }, data=body)
    m = re.findall(r'&id=(\w+)&r=', r.text)
    if m:
        return m[-1]
    return ''


def stockcharts(symbol, show=True):
    from IPython.display import display, HTML, Image
    import requests
    from base64 import b64encode
    keyk = "stockchart_ind"

    ind = default_cache.get(keyk)
    if not ind:
        ind = init_stockchart()
        default_cache.set(keyk, ind)

    image = "https://stockcharts.com/c-sc/sc?s={}&p=D&yr=0&mn=4&dy=0&i={}&r=1615222632271".format(
        symbol, ind)
    r = requests.get(image, headers={"user-agent": "google", "referer": ""})
    i = Image(url="data:image/png;base64," +
              b64encode(r.content).decode("utf-8"))
    if show:
        display(i)
    return i


def show(symbol, style=2):
    if symbol and not symbol.isdigit() and style==2:
        stockcharts(symbol)
        return
    eastmoney_image(symbol)


def tradingview(symbols=None, width="1300px", height="800px"):
    from IPython.display import display, HTML
    from datetime import datetime

    import json
    if not symbols:
        return

    display(HTML(
        """<script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>"""))
    dom_id = "tradingview_%s" % datetime.today().strftime("%s")

    info = {
        "autosize": True,
        "symbol": "AAPL",
        "interval": "D",
        "timezone": "Asia/Shanghai",
        "theme": "light",
        "style": "1",
        "locale": "zh_CN",
        "toolbar_bg": "#f1f3f6",
        "enable_publishing": True,
        "withdateranges": True,
        "hide_side_toolbar": False,
        "allow_symbol_change": True,
        "watchlist": [x for x in symbols],
        "studies": [
                  "RSI@tv-basicstudies"
        ],
        "show_popup_button": True,
        "popup_width": "1000",
        "popup_height": "650",
        "container_id": dom_id
    }

    content = """
        <div class="tradingview-widget-container">
          <div id="{dom}" style="width: {width}; height: {height}"></div>
          
          <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
          <script type="text/javascript">
          new TradingView.widget({config});
          </script>
        </div>""".format(dom=dom_id, config=json.dumps(info, indent=4), width=width, height=height)
    display(HTML(content))


def tradingview_url(symbols=None):
    if not symbols:
        return []

    params = {'frameElementId': 'tradingview_29191',
                'symbol': 'AAPL',
                'interval': 'D',
                'hidesidetoolbar': '0',
                'symboledit': '1',
                'saveimage': '1',
                'toolbarbg': 'f1f3f6',
                'watchlist': 'NPO\x1fCVS\x1fJPM',
                'studies': 'RSI@tv-basicstudies',
                'theme': 'light',
                'style': '1',
                'timezone': 'Asia/Shanghai',
                'withdateranges': '1',
                'studies_overrides': '{}',
                'overrides': '{}',
                'enabled_features': '[]',
                'disabled_features': '[]',
                'enablepublishing': 'true',
        'locale': 'zh_CN'
    }

    params['symbol'] = symbols[0]
    params['watchlist'] = "\x1f".join(symbols)
    pr = requests.Request('get', url="https://www.tradingview.com/widgetembed/", params=params).prepare()
    url1 = "https://www.tradingview.com" + pr.path_url
    url2 = "https://wallstreetcn.com/c/chart?symbol={}&interval=1D&description=%E4%B8%8A%E8%AF%81%E6%8C%87%E6%95%B0".format(symbols[0])
    result = [
        url1, url2
    ]
    return result