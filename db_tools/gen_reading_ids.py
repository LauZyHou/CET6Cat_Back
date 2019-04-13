"""
测试了enread网站的readingURL,并非是连续的,有很多资源已经被删掉
所以不能指定一个id区间取爬取,这个文件的作用就是爬取list页上的URL将其暂存下来
以供gen_reading.py脚本去爬取这些URL对应页面上的文章资源
"""
import requests
import re
from bs4 import BeautifulSoup
import time
import random

"""
http://www.enread.com/essays/list_1.html
目标:爬取reading的list页中展示的reading的URL(实际上只要爬取最后面的id)
"""

# 暂存至此文件
FILE_STORAGE = "./reading_list"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36',
    # 'Cookie': 'srcurl=687474703a2f2f7777772e656e726561642e636f6d2f6573736179732f3130363736352e68746d6c; PHPSESSID=jg8klv0im6l3h521ae8kakhcp7; bdshare_firstime=1555119695040; Hm_lvt_8e0a0ac35ad5727d6e32afe2a02616e9=1555119695; __51cke__=; Hm_lpvt_8e0a0ac35ad5727d6e32afe2a02616e9=1555120274; __tins__1636281=%7B%22sid%22%3A%201555119695506%2C%20%22vd%22%3A%203%2C%20%22expires%22%3A%201555122074380%7D; __51laig__=3; yunsuo_session_verify=28500dbd09d2fb191e59abf222e654dd; security_session_mid_verify=a7a08bcb36730dd0e356f7496a9415a1',
    'Referer': 'http://www.enread.com/essays/106765.html?security_verify_data=313336362c373638',
    'Upgrade-Insecure-Requests': '1',
    'Connection': 'keep - alive'
}
proxies = {
    'https:': 'https://112.85.128.211:9999'
}

# url+page+".html"
url = "http://www.enread.com/essays/list_"
page = 1

max_cnt = 4  # 一个页面的最大尝试次数
a_lst = None  # 存获取到的a标签列表
cookies = None

while (not a_lst) and max_cnt > 0:
    response = requests.get(url + str(page) + ".html", headers=headers, proxies=proxies, cookies=cookies)
    cookies = requests.utils.dict_from_cookiejar(response.cookies)
    soup = BeautifulSoup(response.text, 'lxml')
    a_lst = soup.select('.node-list > .title > h2 > a')
    max_cnt -= 1
    time.sleep(random.uniform(0.5, 1.5))
if (not a_lst) or len(a_lst) == 0:
    print("获取失败")
else:
    for a in a_lst:
        print(str(a))
