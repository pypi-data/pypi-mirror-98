# !/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import re
import sys
from constants import PYTHON_VERISON


if PYTHON_VERISON[0] == 2:
    reload(sys)
    sys.setdefaultencoding('utf-8')
else:
    pass


class SpiderBase(object):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36"}


class HuangliSpider(SpiderBase):
    api_url = "https://nongli.911cha.com/"

    def get_current_calender(self):
        html = requests.get(self.api_url, headers=self.headers).text
        html = str(html)
        re_pattern = "今日.*?年柱.*?<br />(.*?)</td>.*?月柱.*?<br />(.*?)</td>.*?日柱.*?<br />(.*?)</td>.*?时柱.*?<br />(.*?)</td>"
        r = re.search(re_pattern, html.encode("utf-8"))

        return r.group(1), r.group(2), r.group(3), r.group(4)


def main():
    year, month, day, time = HuangliSpider().get_current_calender()
    print("{} {} {} {}".format(year, month, day, time))




if __name__ == '__main__':
    main()


