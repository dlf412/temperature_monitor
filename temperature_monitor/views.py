#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2020/3/12 16:31 
# @Author : Denglingfei 
# @File : views.py
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import generic

from temperature_monitor.forms import LoginForm


class IndexView(LoginRequiredMixin, generic.View):
    def get(self, request):
        return render(request, 'index.html', locals())


class LoginView(generic.View):
    """
    登录系统
    """
    def get(self, request):
        redirect_to = request.GET.get("next", '/')
        form = LoginForm()
        return render(request, 'login.html', locals())

    def post(self, request):
        redirect_to = request.POST.get("next", "/")
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user:
                login(request, user)
                response = HttpResponseRedirect(redirect_to)
                return response
            else:
                msg = "用户名密码错误！"
                return render(request, 'login.html', locals())
        else:
            return render(request, 'login.html', locals())

class LogoutView(generic.View):
    """
    退出登录
    """

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse("login"))