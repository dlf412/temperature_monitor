from django.db import models
from django.contrib.auth.models import User
from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField

# Create your models here.

class AbstractEntity(models.Model):
    create_time = CreationDateTimeField(verbose_name='创建时间')
    modify_time = ModificationDateTimeField(verbose_name='修改时间')

    class Meta(object):
        abstract = True


class Department(AbstractEntity):
    name = models.CharField(max_length=80, verbose_name="名称", help_text="名称", unique=True)
    contact = models.CharField(max_length=20, verbose_name="联系人", help_text="联系人", blank=True)
    contact_num = models.CharField(max_length=20, verbose_name="联系电话", help_text="联系电话", blank=True)
    address = models.CharField(max_length=100, verbose_name="详细地址", help_text="详细地址", blank=True)
    super = models.ForeignKey('self', verbose_name="上级部门", related_name='subs',
                              null=True, help_text="上级部门", on_delete=models.SET_NULL)

    class Meta:
        verbose_name_plural = verbose_name = "部门"

    def __str__(self):
        return self.name


class Channel(AbstractEntity):
    name = models.CharField(max_length=80, verbose_name="名称", help_text="名称")
    department = models.ForeignKey(Department, verbose_name="所在部门", help_text="所在部门", on_delete=models.CASCADE)


    class Meta:
        verbose_name_plural = verbose_name = "通道"
        unique_together = ('name', 'department')

    def __str__(self):
        return self.department.name + self.name


class Admin(AbstractEntity):
    user = models.OneToOneField(User, verbose_name="用户", on_delete=models.CASCADE)
    department = models.ForeignKey(Department, verbose_name="所属部门", on_delete=models.PROTECT, help_text="所属部门")
    name = models.CharField(max_length=20, verbose_name="管理员姓名", blank=True)
    phone = models.CharField(max_length=20, verbose_name="管理员手机号", blank=True)

    class Meta:
        verbose_name_plural = verbose_name = "管理员"

    def __str__(self):
        return self.name



