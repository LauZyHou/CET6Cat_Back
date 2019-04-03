# CET6Cat_Back
CET6Cat英语六级辅导网后端，Django REST framework。
## 前端项目地址
[CET6Cat_Front](https://github.com/LauZyHou/CET6Cat_Front)
## 项目构建
### 导入环境
``` bash
conda env create -f environment.yml
```
### 创建并填充文件
文件`/CET6Cat/privacy.py`中配置了必要但隐私的信息（如API KEY），按照同目录下的模板文件创建该文件。

### 配置数据库
创建MySQL数据库，并将相关信息配置。数据库使用utf8编码，且选择第一种排序方式。
### 运行Task指令
``` bash
python manage.py makemigrations

python manage.py migrate

python manage.py collectstatic

python manage.py createsuperuser
```
注意，在创建超级用户时，需将配置的
```
'users.apps.UsersConfig'
```
暂时改为
```
'users'
```
### 填充数据
填充六级单词数据，直接运行`db_tools/`目录下的`gen_word.py`脚本。

注意，不要重复运行，不然数据库表里的单词就越来越多了（我没有做联合unique约束）。

如果重复运行了怎么办？先把`words_word`表删掉，然后删除表`django_migrations`中生成`words_word`表的那项记录，然后在Task中重新`migrate`就生成了空表，然后再运行上面那个脚本一次。
