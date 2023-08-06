# encoding: utf-8
import time
from cacheout import Cache

default_cache = Cache(maxsize=25000, ttl=86400, timer=time.time)