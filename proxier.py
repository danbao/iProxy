import requests
from lxml import html
from requests import RequestException


class Proxier(object):
    addrList = []

    def crawl(self):
        ips = []
        ports = []
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'
        }
        for i in xrange(1):
            url = "http://www.xicidaili.com/nn/" + str(i + 1)
            resp = requests.get(url, headers=headers)
            page = html.fromstring(resp.content)
            ips.extend(page.xpath("//table/tr[position()>1]/td[3]/text()"))
            ports.extend(page.xpath("//table/tr[position()>1]/td[4]/text()"))
        return ips, ports

    def check(self, addr):
        proxies = {
            'http': 'http://' + addr['IP'] + ':' + addr['Port']
        }
        try:
            resp = requests.get("http://www.baidu.com", proxies=proxies, timeout=3)
            if resp.status_code == 200:
                self.addrList.append(addr)
                return True
            else:
                return False
        except RequestException:
            return False

    def get(self):
        return self.addrList
