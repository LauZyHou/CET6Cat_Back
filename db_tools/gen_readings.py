"""爬取网络上的英文文章,保存到数据库"""
import sys
import os
import requests
import re
from bs4 import BeautifulSoup
import time
import random

# 将当前文件所在目录设置到django环境下
pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(pwd + "../")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CET6Cat.settings")

# 初始化django环境
import django

django.setup()
# 导入django内部的model必须在初始化django之后,不能放在最上边
from readings.models import Reading

"""
www.enread.com
目标：爬取该网站上的英文文章
"""

# 请求头和代理池,请求不到了就更新一下Cookie和Referer和代理
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36',
    'Cookie': 'srcurl=687474703a2f2f7777772e656e726561642e636f6d2f6573736179732f3130363736352e68746d6c; PHPSESSID=jg8klv0im6l3h521ae8kakhcp7; bdshare_firstime=1555119695040; Hm_lvt_8e0a0ac35ad5727d6e32afe2a02616e9=1555119695; __51cke__=; Hm_lpvt_8e0a0ac35ad5727d6e32afe2a02616e9=1555120274; __tins__1636281=%7B%22sid%22%3A%201555119695506%2C%20%22vd%22%3A%203%2C%20%22expires%22%3A%201555122074380%7D; __51laig__=3; yunsuo_session_verify=28500dbd09d2fb191e59abf222e654dd; security_session_mid_verify=a7a08bcb36730dd0e356f7496a9415a1',
    'Referer': 'http://www.enread.com/essays/106765.html?security_verify_data=313336362c373638',
    'Upgrade-Insecure-Requests': '1',
    'Connection': 'keep - alive'
}
proxies = {
    # 'http': 'http://110.52.235.61:9999',
    'https:': 'https://219.138.47.221:9999'
}

url = "http://www.enread.com/essays/106765.html"
article = head = None
max_cnt = 4  # 一个页面的最大尝试次数

# 网站做了保护,请求为空就再请求几次试试
while (not head or not article) and max_cnt > 0:
    response = requests.get(url, headers=headers, proxies=proxies)
    soup = BeautifulSoup(response.text, 'lxml')
    head = soup.select(
        '#wenzhangziti > table > tbody > tr:nth-of-type(1) > td > table > tbody > tr:nth-of-type(1) > td > div > font')
    article = soup.select('#dede_content > div')
    max_cnt -= 1
    time.sleep(random.uniform(0.5, 1.5))
if (not head) or len(head) == 0:
    print("获取失败")
else:
    # 处理标题
    head = re.sub(r'</{0,1}\w.*?>', "", str(head[0]))
    print(head)
    # 获取文章'.html'前的几位数字作为文件名
    fname = re.sub(r'(.html)|(http:.*/)', "", url)
    with open("../media/readings/" + fname, 'w', encoding='utf8') as f:
        # 处理文章的逐段内容,并写入文件
        for d in article:
            # 匹配HTML标签并替换空串以将其删除
            d = re.sub(r'(<a href="#_w_\d+">\d+</a>)|(</{0,1}\w.*?>)', "", str(d))
            # 去除首尾空白(因为可能有大量空白)
            d = d.strip()
            if len(d) > 0:
                f.write(d)
                f.write("\n\n")
    # 持久化到数据库
    reading = Reading()
    reading.name = head[:30]
    reading.content = "readings/" + fname
    reading.source_id = 4
    reading.save()

"""
用下面的小片段测试正则匹配
It was pretty <a href="http://dict.qsbdc.com/devastating" target="_blank">6<strong class="arc_point">devastating<sup class="circle"><a href="#_w_5">5 because other children constantly ma</div><a href="#_w_1">1</a>
"""
