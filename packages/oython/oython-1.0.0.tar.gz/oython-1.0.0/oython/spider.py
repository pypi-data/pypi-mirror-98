import requests
import urllib.request
import urllib.parse
from lxml import etree

def translate(content):
    url = "http://fanyi.youdao.com/translate?doctype=json&type=AUTO&i="+content
    r = requests.get(url)
    result = r.json()
    return result["translateResult"][0][0]["tgt"]

def find_baike(content):
    url = 'https://baike.baidu.com/item/' + urllib.parse.quote(content)
    headers = { 
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36' 
    }
    request = urllib.request.Request(url=url, headers=headers, method='GET')
    response = urllib.request.urlopen(request)
    txt = response.read().decode('utf-8')
    html = etree.HTML(txt)
    senlist = html.xpath('//div[contains(@class,"lemma-summary") or contains(@class,"lemmaWgt-lemmaSummary")]//text()') 
    sen_list_after_filter = [item.strip('\r') for item in senlist]
    return ''.join(sen_list_after_filter)
    
