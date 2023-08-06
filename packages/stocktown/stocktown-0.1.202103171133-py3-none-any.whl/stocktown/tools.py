# encoding: utf-8

from IPython.display import display
from .stock import get_bar, get_symbol_score
from .chart import show
import re

def analysis(symbol):
    symbol = symbol.upper()
    bars = get_bar(symbol)
    info = get_symbol_score(symbol, bars)
    display(info)
    if re.match(r'(SH|SZ)+\d{6}', symbol):
        symbol = symbol[2:]
    show(symbol)