"""从文件生成英语六级单词到数据库表"""
import sys
import os

# 将当前文件所在目录设置到django环境下
pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(pwd + "../")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CET6Cat.settings")

# 初始化django环境
import django

django.setup()

# 导入django内部的model必须在初始化django之后,不能放在最上边
from words.models import Word

# 读取文件,写入数据库
with open("../static/words", 'r', encoding='utf8') as f:
    while True:
        line = f.readline()  # 每次读取一行
        lst = line.split()  # 切分成列表
        size = len(lst)
        if not line:
            break
        # 至少应含有两项:名称和释义
        # 找到第一个释义项的位置,释义一定含有"."因为要指明词汇类型,如"v."
        k = 0
        for k in range(size):
            if lst[k].find(".") != -1:
                break
        # 从第一个释义项之前的所有项合在一起是name
        name = ""
        for i in range(k):
            if i != 0:
                name += " "
            name += lst[i]
        # 从第一个释义项到结尾合在一起是explian
        explain = ""
        for i in range(k, size):
            if i != k:
                explain += " "
            explain += lst[i]
        # 保存到数据库
        word = Word()
        word.name = name
        word.explain = explain
        word.save()

print("生成完成,见words_word表")
