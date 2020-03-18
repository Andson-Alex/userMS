from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from apps.user.auths import PermissionsViewSet, GroupViewSet
from apps.user.views import UserViewSet, LogoutView

app_name = 'apps.user'
urlpatterns = [
    url(r'^infos/$', UserViewSet.as_view({"get": "list"})),
    url(r'^logout/$', LogoutView.as_view()),
    url(r'^create-perms/$', PermissionsViewSet.as_view({"post": "create_permissions"})),
    url(r'^user-add-perms/$', PermissionsViewSet.as_view({"post": "user_add_permissions"})),
    url(r'^user-remove-perms/$', PermissionsViewSet.as_view({"post": "user_remove_permissions"})),
    url(r'^create-groups-perms/$', GroupViewSet.as_view({"post": "create_group_and_permissions"})),
    url(r'^user-add-groups/$', GroupViewSet.as_view({"post": "user_add_group"})),
]

# 定义视图集的路由
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'permissions', PermissionsViewSet, basename='permission')
router.register(r'groups', GroupViewSet, basename='group')
urlpatterns += router.urls
