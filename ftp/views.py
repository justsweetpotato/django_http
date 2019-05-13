#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render, HttpResponseRedirect
import sys

from .ftp_tools import show_dir_info, show_files_name, upload_to_dir, get_host_ip, today_is_friday, remove_files, \
    open_dir, morning_or_night


# Create your views here.
def index(request):
    if request.method != "POST":
        local_ip = get_host_ip()  # 获取本机 IP
        input_port = (sys.argv[-1]).split(":")[-1]  # 获取输入的端口号
        input_ip = (sys.argv[-1]).split(":")[0]  # 获取输入的 ip 地址
        inner_ip_address = request.META['REMOTE_ADDR']

        content = show_dir_info()  # 遍历文件夹下的所有文件信息
        is_friday, is_sunday = today_is_friday()  # 今天是周五吗?
        content["is_friday"] = is_friday
        content["is_sunday"] = is_sunday
        time_name, time_now = morning_or_night()
        content["hello"] = "{}好".format(time_name)
        content["time"] = time_now

        if input_ip == "127.0.0.1":  # 判断是否只允许来自本地 ip 的访问
            error = "当前禁止其他设备访问, 请使用 python manage.py runserver 0.0.0.0:8000 (不应使用 127.0.0.1)"
            content["error"] = error
        if input_ip == input_port:  # 两者的值都为 runserver 表示以默认方式运行
            input_port = "8000"
            error = "当前以默认方式运行, 其他设备无法访问, 请使用 python manage.py runserver 0.0.0.0:8000"
            content["error"] = error

        if local_ip:
            host = "http://{}:{}".format(local_ip, input_port)
        else:
            host = None

        if inner_ip_address == "127.0.0.1":
            content['info'] = True

        content["host"] = host
        return render(request, "index.html", content)

    else:
        local_files = show_files_name()
        try:
            file_name = request.FILES["file"].name
            file = request.FILES['file']
            # file_size = round(file.size / 1024 / 1024)  # 文件大小(单位 MB)
        except:
            content = {"content": "上传失败!", "error": "没有选择文件."}
            return render(request, "error.html", content)

        if file_name in local_files:
            content = {"content": "上传失败!", "error": "文件已存在."}
            return render(request, "error.html", content)

        try:
            upload_to_dir(file_name, file)

        except Exception as e:
            content = {"content": "上传失败!", "error": e}
            return render(request, "error.html", content)

        return HttpResponseRedirect("/")


def tools_rm_files(request, file_name):
    inner_ip_address = request.META['REMOTE_ADDR']

    if inner_ip_address != "127.0.0.1":  # 确认是否是在主机运行
        content = {"content": "删除失败!", "error": "没有权限(你不是管理员)."}
        return render(request, "error.html", content)

    try:
        remove_files(file_name)  # 删除文件或文件夹
    except Exception as e:
        content = {"content": "删除失败!", "error": e}
        return render(request, "error.html", content)

    return HttpResponseRedirect("/")


def tools_open_dir(request):
    inner_ip_address = request.META['REMOTE_ADDR']

    if inner_ip_address != "127.0.0.1":
        content = {"content": "打开文件夹失败!", "error": "没有权限(你不是管理员)."}
        return render(request, "error.html", content)

    try:
        open_dir()  # 打开文件夹
    except Exception as e:
        content = {"content": "打开文件夹失败!", "error": e}
        return render(request, "error.html", content)

    # 成功打开文件夹则重定向到主页
    return HttpResponseRedirect("/")
