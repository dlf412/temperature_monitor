from django.db import models

from organiz.models import Department, Channel, AbstractEntity, Admin


# Create your models here.

class Device(AbstractEntity):
    uuid = models.CharField(max_length=40, help_text="设备唯一识别码", verbose_name="设备唯一识别码", unique=True)
    department = models.ForeignKey(Department, verbose_name="关联部门", help_text="关联部门",
                                   on_delete=models.SET_NULL, null=True)
    channel = models.ForeignKey(Channel, verbose_name="关联通道", help_text="关联通道",
                                on_delete=models.SET_NULL, null=True)
    is_online = models.BooleanField(default=False, verbose_name="是否在线", help_text="true:在线, false:不在线")
    last_online_time = models.DateTimeField(verbose_name="最后一次在线时间",
                                            help_text="最后一次在线时间",
                                            default=None, null=True)
    total_online_time = models.IntegerField(verbose_name="总在线时间(秒)", help_text="总在线时间", default=0)


    class Meta:
        verbose_name_plural = verbose_name = "设备"

    def __str__(self):
        return self.uuid


class RealData(AbstractEntity):
    device = models.ForeignKey(Device, help_text="设备", on_delete=models.PROTECT, verbose_name="设备")
    temperature = models.SmallIntegerField(verbose_name="实时温度", default=0, help_text="实时温度*100")
    visitors = models.PositiveSmallIntegerField(verbose_name="当日人流量", default=0, help_text="当然人流量")
    people_temperature = models.PositiveSmallIntegerField(verbose_name="当前通过的人体温", default=0, help_text="当前通过的人体温")
    device_rtc_time = models.PositiveIntegerField(verbose_name="设备RTC时间", default=0, help_text="设备RTC时间")
    device_control_time = models.PositiveIntegerField(verbose_name="设备控制器时间", default=0, help_text="设备控制器时间")

    class Meta:
        verbose_name_plural = verbose_name = "设备实时数据"


class Configure(AbstractEntity):
    device = models.ForeignKey(Device, help_text="设备", on_delete=models.CASCADE, verbose_name="设备")
    low_threshold = models.PositiveSmallIntegerField(help_text="有人通过的最低温", verbose_name="有人通过的最低温", default=3200)
    normal_threshold = models.PositiveSmallIntegerField(help_text="正常的最低温度", verbose_name="正常的最低温度", default=3400)
    high_threshold = models.PositiveSmallIntegerField(help_text="发烧的最低温度", verbose_name="发烧的最低温度", default=3720)
    delay_after_warn = models.PositiveSmallIntegerField(help_text="报警后，多久自动关闭，单位：秒", verbose_name="报警后多久自动关闭",
                                                        default=0)
    auto_close = models.PositiveSmallIntegerField(help_text="报警后，检测到下一人时，"
                                                            "是否自动关闭。1检测到下一人自动关闭；0不自动关闭",
                                                  verbose_name="警后，检测到下一人时，是否自动关闭。1检测到下一人自动关闭；0不自动关闭",
                                                  default=0)
    reverse = models.PositiveSmallIntegerField(help_text="保留", verbose_name="保留", default=0)
    relay1 = models.PositiveSmallIntegerField(help_text="继电器1动作类型：0电平，1脉冲", verbose_name="继电器1动作类型：0电平，1脉冲", default=0)
    relay1_time = models.PositiveSmallIntegerField(help_text="继电器1动作时长，单位100ms，最大6553.5秒",
                                                   verbose_name="继电器1动作时长，单位100ms，最大6553.5秒", default=0)
    relay1_interval = models.PositiveSmallIntegerField(help_text="继电器1间歇时长，单位100ms，最大6553.5秒",
                                                       verbose_name="继电器1间歇时长，单位100ms，最大6553.5秒", default=0)
    relay2 = models.PositiveSmallIntegerField(help_text="继电器2动作类型：0电平，1脉冲", verbose_name="继电器2动作类型：0电平，1脉冲", default=0)
    relay2_time = models.PositiveSmallIntegerField(help_text="继电器2动作时长，单位100ms，最大6553.5秒",
                                                   verbose_name="继电器2动作时长，单位100ms，最大6553.5秒", default=0)
    relay2_interval = models.PositiveSmallIntegerField(help_text="继电器2间歇时长，单位100ms，最大6553.5秒",
                                                       verbose_name="继电器2间歇时长，单位100ms，最大6553.5秒", default=0)
    device_time = models.PositiveIntegerField(help_text="2000年到当前时间的秒数", verbose_name="设备时间", default=0)


    class Meta:
        verbose_name_plural = verbose_name = "设备参数配置"


class EventSummary(AbstractEntity):
    device = models.OneToOneField(Device, help_text="设备", on_delete=models.PROTECT, verbose_name="设备")
    oldest_no = models.PositiveIntegerField(help_text="最早记录编号", verbose_name="最早记录编号")
    newest_no = models.PositiveIntegerField(help_text="最新记录编号", verbose_name="最新纪录编号")
    max_record = models.PositiveSmallIntegerField(help_text="最大记录数", verbose_name="最大记录数")
    sync_no = models.PositiveIntegerField(help_text="已同步的最新编号", verbose_name="已经同步的最新编号", default=0)


    class Meta:
        verbose_name_plural = verbose_name = "设备报警概要"


class Event(AbstractEntity):
    device = models.ForeignKey(Device, help_text="设备", on_delete=models.PROTECT, verbose_name="设备")
    no = models.PositiveIntegerField(help_text="编号", verbose_name="报警事件编号")
    type = models.SmallIntegerField(help_text="报警事件类型", verbose_name="报警事件类型")
    visitors = models.SmallIntegerField(help_text="当日人流量", verbose_name="当日人流量")
    temperature = models.SmallIntegerField(verbose_name="当前温度", default=0, help_text="温度*100")
    warn_temperature = models.SmallIntegerField(verbose_name="报警设置温度", default=0, help_text="温度*100")
    warn_time = models.PositiveIntegerField(verbose_name="报警时间", help_text="2000年到当前秒数")


    class Meta:
        verbose_name_plural = verbose_name = "设备报警事件"
        unique_together = ('no', 'device')

class OperationLog(AbstractEntity):
    device = models.ForeignKey(Device, help_text="设备", on_delete=models.CASCADE, verbose_name="设备")
    command = models.CharField(max_length=60, help_text='操作指令', verbose_name="操作指令")
    data = models.CharField(help_text="指令数据", verbose_name="指令数据", max_length=200)
    user = models.ForeignKey(Admin, verbose_name="操作人", help_text="操作人",
                             on_delete=models.SET_NULL, default=None, null=True)

    class Meta:
        verbose_name_plural = verbose_name = "设备操作日志表"




