#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render, HttpResponseRedirect
import sys

from .ftp import show_dir_file, upload_to_dir, get_host_ip, today_is_friday, remove_files, open_dir


# Create your views here.
def index(request):
    if request.method != "POST":
        local_ip = get_host_ip()  # 获取本机 IP
        input_port = (sys.argv[-1]).split(":")[-1]  # 获取输入的端口号
        input_ip = (sys.argv[-1]).split(":")[0]  # 获取输入的 ip 地址

        content = show_dir_file()  # 遍历文件夹下的所有文件名
        is_friday = today_is_friday()  # 今天是周五吗?
        content["is_friday"] = is_friday

        if input_ip == "127.0.0.1":  # 判断是否只允许来自本地 ip 的访问
            error = "请注意, 您当前程序运行在本地, 其他设备可能无法访问, 请使用 python manage.py runserver 0.0.0.0:8000 (不应使用 127.0.0.1)"
            content["error"] = error
        if input_ip == input_port:  # 两者的值都为 runserver 表示以默认方式运行
            input_port = "8000"
            error = "请注意, 您目前使用默认方式运行, 其他设备可能无法访问, 请使用 python manage.py runserver 0.0.0.0:8000"
            content["error"] = error

        if local_ip:
            host = "http://{}:{}".format(local_ip, input_port)
        else:
            host = None

        content["host"] = host
        return render(request, "index.html", content)

    else:
        try:
            file_name = request.FILES["file"].name
            file = request.FILES['file']
            # file_size = round(file.size / 1024 / 1024)  # 文件大小(单位 MB)
            response = upload_to_dir(file_name, file)

        except Exception as e:
            content = {"content": e}
            return render(request, "fail.html", content)

        if response:
            return HttpResponseRedirect("/")


def tools_rm_files(request, file_name):
    try:
        res = remove_files(file_name)  # 删除文件或文件夹
    except:
        content = {"content": "删除失败!"}
        return render(request, "error.html", content)

    return HttpResponseRedirect("/")


def tools_open_dir(request):
    try:
        open_dir()  # 打开文件夹
    except Exception as e:
        content = {"content": "打开文件夹失败!", "error": e}
        return render(request, "error.html", content)

    # 成功打开文件夹则重定向到主页
    return HttpResponseRedirect("/")
