#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2020/3/12 16:33 
# @Author : Denglingfei 
# @File : forms.py 

from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(max_length=12, label="用户名", error_messages={
        "max_length": "用户名长度不超过12位", "required": "账号必填"
    })
    password = forms.CharField(min_length=6, label="用户密码", error_messages={
        "min_length": "密码长度必须大于6位", "required": "密码必填"})