from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.utils import json
from rest_framework.response import Response

from apps.user.models import UserInfo
from apps.user.serializers import PermissionsSerializers, GroupsSerializers
from apps.utils.response import CommonResponseMixin

User = get_user_model()


class PermissionsViewSet(viewsets.ModelViewSet, CommonResponseMixin):
    """
    权限管理
    """
    queryset = Permission.objects.all()
    serializer_class = PermissionsSerializers
    permission_classes = [IsAuthenticated]

    def create_permissions(self, request):
        """
        换件权限
        :param request: content_type_id，codename, name
        :return: 创建成功
        """
        data = json.loads(request.body.decode())
        content_type_id = data['content_type_id']
        content_type = ContentType.objects.get(id=content_type_id)
        permission = Permission.objects.create(
            codename=data['codename'],
            name=data['name'],
            content_type=content_type,
        )

        response = self.wrap_json_response()
        return Response(response)

    def user_add_permissions(self, request):
        """
        用户绑定权限
        :param request: user_id：用户id，permission_list：权限列表
        :return: 保存结果
        """
        try:
            data = request.data
            user_id = data['user_id']
            permission_list = data['permission_list']
            user_obj = get_object_or_404(UserInfo, pk=user_id)
            print(user_obj.get_all_permissions())
            for per in permission_list:
                permission = Permission.objects.get(id=per)
                user_obj.user_permissions.add(permission)
            print(user_obj.get_all_permissions())
            # 重新加载user 对象，获取最新权限
            user_obj_new = get_object_or_404(UserInfo, pk=user_id)
            print(user_obj_new.get_all_permissions())
            print(user_obj_new.get_group_permissions())
            response = self.wrap_json_response()
            pass
        except Exception as e:
            print(e)
            response = self.wrap_json_response(code=1002, message="用户绑定权限失败！")
        return Response(response)

    def user_remove_permissions(self, request):
        """
        用户删除权限
        :param request: user_id：用户id，permission_list：删除权限列表
        :return: 保存结果
        """
        try:
            print("测试用户删除权限")
            data = json.loads(request.body.decode())
            user_id = data['user_id']
            permission_list = data['permission_list']
            user_obj = get_object_or_404(UserInfo, pk=user_id)
            print(user_obj.get_all_permissions())
            for per in permission_list:
                permission = Permission.objects.get(id=per)
                user_obj.user_permissions.remove(permission)
            print(user_obj.get_all_permissions())
            # 重新加载user 对象，获取最新权限
            user_obj_new = get_object_or_404(UserInfo, pk=user_id)
            print(user_obj_new.get_all_permissions())
            print(user_obj_new.get_group_permissions())
            response = self.wrap_json_response()
            pass
        except Exception as e:
            print(e)
            response = self.wrap_json_response(code=1002, message="用户移除权限失败！")
        return Response(response)


class GroupViewSet(viewsets.ModelViewSet, CommonResponseMixin):
    """
    权限组管理
    """
    queryset = Group.objects.all()
    serializer_class = GroupsSerializers

    def create_group_and_permissions(self, request):
        """
        创建用户组并绑定权限
        :param request: group_name: 用户组名称；permission_list[]: 权限列表
        :return: 保存成功
        """
        try:
            data = json.loads(request.body.decode())
            group_name = data['group_name']
            permission_list = data['permission_list']
            group = Group.objects.create(
                name=group_name
            )
            for per in permission_list:
                permission = Permission.objects.get(id=per)
                group.permissions.add(permission)
            response = self.wrap_json_response()
        except Exception as e:
            print(e)
            response = self.wrap_json_response(code=1002, message="创建用户权限组失败！")
        return Response(response)

    def user_add_group(self, request):
        """
        用户绑定用户组
        :param request: user_id: 用户ID，group_list[]: 权限组列表
        :return: 绑定成功
        """
        try:
            data = json.loads(request.body.decode())
            user_id = data['user_id']
            group_list = data['group_list']
            user_obj = UserInfo.objects.get(id=user_id)
            for g in group_list:
                group = Group.objects.get(id=g)
                user_obj.groups.add(group)
            response = self.wrap_json_response()
        except Exception as e:
            print(e)
            response = self.wrap_json_response(code=1002, message="用户组绑定失败！")
        return Response(response)

