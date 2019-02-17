import xadmin
from xadmin import views
from users.models import VerifyCode


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    site_title = "CET6Cat后台管理系统"
    site_footer = "2018-2019 Zhihao Liu at SHU"
    # menu_style = "accordion"


# 这个配置类让VerifyCode这个Model也受XAdmin管理
# 注意,因为UserProfile已经作为系统的默认User类,所以不用像这样配置
class VerifyCodeAdmin(object):
    """验证码"""
    list_display = ['code', 'mobile', "add_time"]


xadmin.site.register(VerifyCode, VerifyCodeAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)
