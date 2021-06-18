from django.contrib import admin

# Register your models here.
from organiz.models import *


class DisplayAllWithName(admin.ModelAdmin):
    """
    ModelAdmin 扩展 ，显示所有属性 包括用户名
    """
    list_display = []

    def __init__(self, *args, **kwargs):
        super(DisplayAllWithName, self).__init__(*args, **kwargs)
        self.list_display = [obj.name for obj in args[0]._meta.fields]


@admin.register(Department)
class DepartmentAdmin(DisplayAllWithName):
    search_fields = ('name', 'address')
    # list_display = ('name', 'address', 'contact', 'contact_num', 'super')

@admin.register(Admin)
class AdminAdmin(DisplayAllWithName):
    search_fields = ('name', 'user__username', 'department__name', 'phone')
    # list_display = ('name', 'user', 'department', 'phone' )

@admin.register(Channel)
class ChannelAdmin(DisplayAllWithName):
    search_fields = ('name', 'department__name')
    # list_display = ('name', 'department')

