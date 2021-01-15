from ruamel.yaml import YAML
from urlextract import URLExtract
import urllib
import re
import os
import requests     #需要安装

import re
from collections import OrderedDict

"""
This script tries to detect keywords in the tool urls. 
"""

yaml = YAML()
yaml_recipe = YAML(typ="rt")  # pylint: disable=invalid-name
with open('../annotations.yaml', 'r') as read_file:
    file_annotations = yaml.load(read_file)

tools = {}

def getdate(url, headers, i):
    try:
        res = requests.get(url=url, headers=headers, timeout=15, allow_redirects=False)
        response = res.text
        if ('doi' in response) or ('pmid' in response.lower()) or ('cite' in response.lower()) or ('citation' in response.lower()):
            print(url)
    except :
        print("网络出现问题-----------%d" % i)
    return url_again

### Annotate bioconductor package
for key in file_annotations:
    tool = file_annotations[key]
    url = tool['home_url']
    url_again = []  # 请求超时或网络问题的链接放到里面，等之前循环一遍后，再次请求一遍

    headers = {
        'Accept': 'text/html',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Cookie': '_octo=GH1.1.2133912576.1600409893; logged_in=no; _ga=GA1.2.1831073498.1600409904; _gh_sess=hS4oMIaMHraJqN9wO6%2BFR0jF0JyPa%2FhotPo0Ujeq5%2BSDuYXAX0Libfa%2BUO%2Bj41BH9NWg1n057KA6LJao9Rtnv6W5C9Nqn2fgJoPDMPXooa8ZSqCtA1sb2LDTCqaezWGf8pz0%2Bmf01pWVrGrgyobbSVHhDT315UDAGl6NJT%2BueaLb%2Fpp%2FCfJ%2B5tSfZsJG8iE%2F6QpAMOGp8088eAd0KNas7fmFwyHcaJd9zJ%2BKjOagBLqqcf%2FfH0MZpuFQeL2yp2oqJlgSfhdmbdrJ83C%2ByvO0Kw%3D%3D--A3%2BF80BsJEuy4LO3--U5vLDuNGDSwCKWHRI9b8GA%3D%3D; tz=Asia%2FShanghai',
        'Host': 'github.com',
        'Referer': 'https://github.com/samtools/samtools',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }
    identifiers = []
    if 'no_doi' not in tool and ('identifiers' not in tool or len(tool['identifiers']) == 0):
        identifiers = []
        getdate(url, headers, 1)