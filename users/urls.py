"""users URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include

import xadmin
from apps.user.views import LoginView
from xadmin.plugins import xversion
# 导入辅助函数get_schema_view
from rest_framework.schemas import get_schema_view
# 导入两个类
from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer

xadmin.autodiscover()
xversion.register_models()

# 利用辅助函数引入所导入的两个类
schema_view = get_schema_view(title='api', renderer_classes=[SwaggerUIRenderer, OpenAPIRenderer])


urlpatterns = [
    # path('admin/', admin.site.urls),
    path('xadmin/', xadmin.site.urls),
    path('api-token-auth/', LoginView.as_view()),
    path('api-auth/', include('rest_framework.urls')),
    path('docs/', schema_view, name='docs'),  # 配置docs的url路径
    path('api/user/', include('apps.user.urls')),
]
