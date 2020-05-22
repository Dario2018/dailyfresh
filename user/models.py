from django.db import models
from django.contrib.auth.models import AbstractUser
from db.base_model import BaseModel
from itsdangerous import TimedJSONWebSignatureSerializer
from django.conf import settings


# Create your models here.

class User(AbstractUser, BaseModel):
    # def generate_active_token(self):
    #     """生成用户签名字符串"""
    #     serializer = TimedJSONWebSignatureSerializer(settings.SECRET_KEY, 3600)
    #     info = {"confirm": self.id}
    #     token = serializer.dumps(info)
    #     return token.decode()

    class Meta:
        db_table = "userinfo"
        verbose_name = "用户"
        verbose_name_plural = verbose_name


class AddressManager(models.Manager):
    """地址模型管理器"""

    def get_default_addr(self, user):
        try:
            default_addr = self.get(user=user, is_default=True)
        except UserAddress.DoesNotExist:
            default_addr = None
        return default_addr


class UserAddress(BaseModel):
    recipient = models.CharField(max_length=20, verbose_name="收件人")
    contact_num = models.CharField(max_length=11, verbose_name="联系电话")
    address = models.CharField(max_length=100, verbose_name="收件人地址")
    zip_code = models.IntegerField(null=True, verbose_name="邮政编码")
    is_default = models.BooleanField(default=False, verbose_name="是否默认")
    user = models.ForeignKey("User", verbose_name="所属账户", on_delete=models.CASCADE)
    objects = AddressManager()

    class Meta:
        db_table = "address"
        verbose_name = "地址"
        verbose_name_plural = verbose_name
