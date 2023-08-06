# encoding: utf-8
from setuptools import setup
from datetime import datetime

t = datetime.today()
NAME = "stocktown"
DESCRIPTION = ""
URL = ""
EMAIL = ""

VERSION = "0.1.{}".format(t.strftime("%Y%m%d%H%M"))
AUTHOR = 'Sikoo Lee'

REQUIRES = [
    "cacheout",
    "pandas",
    "requests",
    "seaborn",
    "mplfinance",
    "pandas_datareader",
    "plotly",
]

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=DESCRIPTION,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    packages=[NAME],
    package_data={'': ['LICENSE', 'NOTICE']},
    package_dir={NAME: NAME},
    include_package_data=True,
    python_requires=">3.5, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*",
    install_requires=REQUIRES,
    license=DESCRIPTION,
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
    # cmdclass={'test': PyTest},
    # tests_require=test_requirements,
    # extras_require={
    #     'security': ['pyOpenSSL >= 0.14', 'cryptography>=1.3.4'],
    #     'socks': ['PySocks>=1.5.6, !=1.5.7'],
    #     'socks:sys_platform == "win32" and python_version == "2.7"': ['win_inet_pton'],
    # },
    project_urls={
        'Documentation': 'https://stocktown.readthedocs.io',
        'Source': 'https://github.com/zhangheli/stocktown',
    },
)
