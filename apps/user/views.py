from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView

from apps.user.serializers import UserSerializers
from apps.utils.response import CommonResponseMixin

User = get_user_model()


class LoginView(ObtainAuthToken, CommonResponseMixin):

    def post(self, request, *args, **kwargs):
        """
        登录函数
        :param request: 用户名、密码
        :return: 验证后登录
        """
        data = {}
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        user_obj = User.objects.filter(id=user.id)
        user_ser = UserSerializers(instance=user_obj, many=True)
        token, created = Token.objects.get_or_create(user=user)
        data['token'] = token.key
        data['username'] = user.username
        data['user_id'] = user.id
        data['user'] = user_ser.data
        response = self.wrap_json_response(data=data)
        return Response(response)


class LogoutView(APIView, CommonResponseMixin):
    queryset = User.objects.all()

    def get(self, request):
        try:
            Token.objects.filter(user=request.user).delete()
            response = self.wrap_json_response(message="退出成功！")
        except Exception as e:
            print(e)
            response = self.wrap_json_response(code=1002, message="退出失败！")
        return Response(response)


class UserViewSet(viewsets.ModelViewSet, CommonResponseMixin):
    """
    用户管理视图
    """
    queryset = User.objects.all()
    serializer_class = UserSerializers

    def list(self, request, *args, **kwargs):
        queryset = User.objects.all()
        ser = UserSerializers(instance=queryset, many=True)
        response = self.wrap_json_response(data=ser.data, count=queryset.count())

        from django.contrib.auth.models import Permission
        from django.contrib.contenttypes.models import ContentType

        content_type = ContentType.objects.get_for_model(User)
        permission = Permission.objects.create(
            codename='can_publish',
            name='打印用户列表',
            content_type=content_type,
        )

        return Response(response)

