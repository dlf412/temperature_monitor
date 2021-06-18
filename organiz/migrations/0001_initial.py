# Generated by Django 3.0.4 on 2020-03-11 15:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('modify_time', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='修改时间')),
                ('name', models.CharField(help_text='名称', max_length=80, unique=True, verbose_name='名称')),
                ('contact', models.CharField(blank=True, help_text='联系人', max_length=20, verbose_name='联系人')),
                ('contact_num', models.CharField(blank=True, help_text='联系电话', max_length=20, verbose_name='联系电话')),
                ('address', models.CharField(blank=True, help_text='详细地址', max_length=100, verbose_name='详细地址')),
                ('super', models.ForeignKey(help_text='上级部门', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subs', to='organiz.Department', verbose_name='上级部门')),
            ],
            options={
                'verbose_name': '部门',
                'verbose_name_plural': '部门',
            },
        ),
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('modify_time', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='修改时间')),
                ('name', models.CharField(blank=True, max_length=20, verbose_name='管理员姓名')),
                ('phone', models.CharField(blank=True, max_length=20, verbose_name='管理员手机号')),
                ('department', models.ForeignKey(help_text='所属部门', on_delete=django.db.models.deletion.PROTECT, to='organiz.Department', verbose_name='所属部门')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '管理员',
                'verbose_name_plural': '管理员',
            },
        ),
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('modify_time', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='修改时间')),
                ('name', models.CharField(help_text='名称', max_length=80, verbose_name='名称')),
                ('department', models.ForeignKey(help_text='所在部门', on_delete=django.db.models.deletion.CASCADE, to='organiz.Department', verbose_name='所在部门')),
            ],
            options={
                'verbose_name': '通道',
                'verbose_name_plural': '通道',
                'unique_together': {('name', 'department')},
            },
        ),
    ]
