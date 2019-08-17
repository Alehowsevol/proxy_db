import re
import scrapy

from base64 import b64decode

from ..items import ProxyDbItem

from scrapy.utils.response import open_in_browser
class Proxy(scrapy.Spider):
    name = "proxy"
    start_urls = ['http://proxydb.net/']

    def parse(self, response):
        nnum = re.search(r'data-\w*nnum\w="(\d+)"', response.text)
        nnum = int(nnum.group(1)) if nnum else 0
        for tr in response.xpath('//tbody/tr'):
            script = tr.xpath('.//script/text()').extract_first('')

            first_part_ip = re.findall(
                r"var[a-z\s]+=\s+'(.+?)'", script)[0][::-1]
            second_part_ip = re.findall(
                r"var yxy .+? atob\('(.+?)'", script)[0]
            for i in set(re.findall(r'\\x[0-9A-Fa-f]{2}', second_part_ip)):
                second_part_ip = second_part_ip.replace(
                    i, chr(int(i.replace('\\', '0'), 16)))
            ip = first_part_ip + b64decode(second_part_ip).decode('utf-8')

            port = re.findall(r"var[\s/*]+pp = (.+?);", script)[0]
            port = int(re.search(r'\d+', port).group()) + nnum
            yield ProxyDbItem(ip_address=ip,
                              port=port)
        open_in_browser(response)