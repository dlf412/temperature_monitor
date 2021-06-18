from django.contrib import admin

# Register your models here.

from pyrometer.models import *

from organiz.admin import DisplayAllWithName

@admin.register(Device)
class DeviceAdmin(DisplayAllWithName):
    search_fields = ('uuid', 'department__name', 'channel__name')
    # list_display = ('name', 'address', 'contact', 'contact_num', 'super')


@admin.register(RealData)
class RealDataAdmin(DisplayAllWithName):
    search_fields = ('device__uuid',)


@admin.register(EventSummary)
class EventSummaryAdmin(DisplayAllWithName):
    search_fields = ('device__uuid',)

@admin.register(Event)
class EventAdmin(DisplayAllWithName):
    search_fields = ('device__uuid',)

@admin.register(Configure)
class ConfigureAdmin(DisplayAllWithName):
    search_fields = ('device__uuid',)

@admin.register(OperationLog)
class OperationLogAdmin(DisplayAllWithName):
    search_fields = ('device__uuid', 'admin__name')



