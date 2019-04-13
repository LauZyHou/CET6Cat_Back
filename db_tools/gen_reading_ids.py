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
import json

"""
http://www.enread.com/essays/list_1.html
目标:爬取reading的list页中展示的reading的URL(实际上只要爬取最后面的id)
"""

# 暂存至此文件
FILE_STORAGE = "./reading_list"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36',
    'Cookie': 'Hm_lvt_8e0a0ac35ad5727d6e32afe2a02616e9=1555125825,1555139354; __51cke__=; yunsuo_session_verify=47caaea7006b66b3027c74b4aff09465; srcurl=687474703a2f2f7777772e656e726561642e636f6d2f6573736179732f6c6973745f322e68746d6c; security_session_mid_verify=0fb499be8d029a761e051487fdd708f1; Hm_lpvt_8e0a0ac35ad5727d6e32afe2a02616e9=1555140172; __tins__1636281=%7B%22sid%22%3A%201555139354228%2C%20%22vd%22%3A%204%2C%20%22expires%22%3A%201555141971944%7D; __51laig__=4',
    # 'Referer': 'http://www.enread.com/essays/106765.html?security_verify_data=313336362c373638',
    # 'Upgrade-Insecure-Requests': '1',
    # 'Connection': 'keep - alive'
}
proxies = {
    'https:': 'https://112.85.128.211:9999'
}

# url+page+".html"
url = "http://www.enread.com/essays/list_"
page = 4

max_cnt = 3  # 一个页面的最大尝试次数
a_lst = None  # 存获取到的a标签列表
cookies = None

if __name__ == '__main__':
    while (not a_lst) and max_cnt > 0:
        response = requests.get(url + str(page) + ".html", headers=headers, proxies=proxies, cookies=cookies)
        soup = BeautifulSoup(response.text, 'lxml')
        # a_lst = soup.select('div.node-list > div.title > h2 > a')
        a_lst = soup.select(
            'body > div > div.main > table > tbody > tr > td.left > div > div > div.list > div > div.title > h2 > a')
        max_cnt -= 1
        time.sleep(random.uniform(0.5, 1.5))

        """
        cookies = requests.utils.dict_from_cookiejar(response.cookies)
        # print(cookies)
        # print(response.headers)
        print(response)
        for k in response.headers:
            if k == 'Set-Cookie':
                headers['Cookie'] = response.headers[k]
                # cookies = response.headers[k]
            else:
                headers[k] = response.headers[k]
        print(headers)
        """

        """
        if 'Set-Cookie' in response.headers:
            # 取出yunsuo_session_verify
            ysv = response.headers['Set-Cookie'].split("; ")[0]
            print(ysv)
            # 替换掉Cookie中旧的yunsuo_session_verify
            cookie_lst = headers['Cookie'].split("; ")[0:-1]
            cookie_lst.append(ysv)
            headers['Cookie'] = "; ".join(cookie_lst)
        # print(response.headers)
        """

    if (not a_lst) or len(a_lst) == 0:
        print("获取失败")
    else:
        for i in range(len(a_lst)):
            # 只保留essay id
            a_lst[i] = re.sub(r'(<a.*essays/)|(.html.*</a>)', "", str(a_lst[i]))
        with open(FILE_STORAGE, 'a+') as f:
            f.writelines("\n".join(a_lst) + "\n")
        print("第{}页写入完成".format(page))
