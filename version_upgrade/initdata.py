# coding=utf-8
import os, time
import sys
import django
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "temperature_monitor.settings")


def main():
    """Entry Point"""

    import shutil
    print ('设置环境...')
    django.setup()

    if os.path.exists("organiz/migrations"):
        shutil.rmtree("organiz/migrations")
    if os.path.exists('pyrometer/migrations'):
        shutil.rmtree('pyrometer/migrations')



    os.system('python manage.py flush')
    os.system('python manage.py makemigrations organiz pyrometer')
    os.system('python manage.py migrate')


    print ('创建超级管理员...')

    from django.contrib.auth.models import User
    from organiz.models import Department, Admin, Channel

    User.objects.create_superuser('18888888888', '18888888888@qq.com', 'admin123')
    user1 = User.objects.create_user('test1', 'test01@qq.com', '123456')
    user2 = User.objects.create_user('test2', 'test01@qq.com', '123456')

    super_depart = Department.objects.create(name="一级机构", super=None)
    depart = Department.objects.create(name="二级机构", super=super_depart)
    Admin.objects.create(user=user1, department=super_depart, name="一级机构管理员", phone="13388888888")
    Admin.objects.create(user=user2, department=depart, name="二级机构管理员", phone="13399999999")

    Channel.objects.create(department=super_depart, name="一级机构通道")
    Channel.objects.create(department=depart, name="二级机构通道")




if __name__ == '__main__':
    main()

