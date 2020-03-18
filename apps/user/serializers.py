from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission, Group
from rest_framework import serializers

from apps.user import models

User = get_user_model()


class PermissionsSerializers(serializers.ModelSerializer):
    """
    权限表序列化
    """
    content_type_id = serializers.IntegerField(source="content_type.id")
    content_type = serializers.CharField(source="content_type.app_label")

    class Meta:
        model = Permission
        fields = ('id', 'name', 'content_type_id', 'content_type', 'codename')


class GroupsSerializers(serializers.ModelSerializer):
    """
    用户组序列化
    """
    # 用户组和权限多对多关系
    permissions = serializers.SerializerMethodField()

    # 序列化用户组对应的权限
    # 钩子函数序列化必须以get_开头
    def get_permissions(self, obj):
        permission = obj.permissions.all()
        perm = PermissionsSerializers(permission, many=True)
        return perm.data

    class Meta:
        model = Group
        fields = ('id', 'name', 'permissions')


class UserSerializers(serializers.ModelSerializer):
    """
    用户表序列化
    """
    gender = serializers.CharField(source="get_gender_display")
    groups = serializers.SerializerMethodField()
    permissions = serializers.SerializerMethodField()

    # 序列化用户对应的权限组
    def get_groups(self, obj):
        groups = obj.groups.all()
        group = GroupsSerializers(groups, many=True)
        group_names = []
        for g in group.data:
            group_names.append(g['name'])

        return group_names

    # 序列化用户对应的权限
    def get_permissions(self, obj):
        permissions = obj.user_permissions.all()
        perm = PermissionsSerializers(permissions, many=True)
        return obj.get_all_permissions()

    class Meta:
        model = User
        fields = ('id', 'username', 'name', 'email', 'gender', 'cellphone', 'groups', 'permissions')



