# CET6Cat_Back
CET6Cat英语六级辅导网后端，Django REST framework。
## 前端项目地址
[CET6Cat_Front](https://github.com/LauZyHou/CET6Cat_Front)
## 项目构建
### 数据库和管理员
``` bash
python manage.py makemigrations

python manage.py migrate

python manage.py createsuperuser
```
### XAdmin for Django2
建立根目录下的static和collect_static目录。
``` bash 
pip install https://codeload.github.com/sshwsfc/xadmin/zip/django2

python manage.py collectstatic
```