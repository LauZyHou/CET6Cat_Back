# CET6Cat_Back
CET6Cat英语六级辅导网后端，Django REST framework。
## 前端项目地址
[CET6Cat_Front](https://github.com/LauZyHou/CET6Cat_Front)
## 项目构建
#### 创建并填充文件
/CET6Cat/privacy.py

#### 配置数据库
创建MySQL数据库，并将相关信息配置。数据库使用utf8编码，且选择第一种排序方式。
#### 运行Task指令
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