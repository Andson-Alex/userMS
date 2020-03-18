import xadmin
from .models import UserInfo


# 设置自定义皮肤
class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


xadmin.site.register(xadmin.views.BaseAdminView, BaseSetting)


# 设置title和公司名称
class GlobalSettings(object):
    site_title = "港城业务管理系统"
    site_footer = "智能港口创新工作室"
    menu_style = 'accordion'  # 修改菜单栏 改成收缩样式


xadmin.site.register(xadmin.views.base.CommAdminView, GlobalSettings)
