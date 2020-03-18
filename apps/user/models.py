from django.contrib.auth.models import AbstractUser
from django.db import models


# 继承AbstractUser
class UserInfo(AbstractUser):
    GENDER = [
        ('M', "男"),
        ('F', "女")
    ]
    name = models.CharField(max_length=150, verbose_name='用户姓名', help_text='用户姓名')
    gender = models.CharField(max_length=1, choices=GENDER, default='M', verbose_name='性别', help_text='性别')
    cellphone = models.CharField(max_length=15, verbose_name='联系电话', help_text="联系电话")
    wx_open_id = models.CharField(max_length=50, verbose_name="微信号", help_text="微信号")
    register_time = models.DateField(auto_now_add=True, verbose_name='注册时间', help_text='注册时间')
    image = models.ImageField(upload_to="users/", null=True, blank=True, verbose_name="头像", help_text="头像")

    class Meta:
        verbose_name = "用户信息表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

    def get_name(self):
        """
        查询用户姓名
        :return: 中文名
        """
        return self.name




