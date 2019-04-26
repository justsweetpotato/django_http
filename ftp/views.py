# -*- coding: utf-8 -*-

from django.shortcuts import render
import sys

from .ftp import show_dir_file, upload_to_dir, get_host_ip, today_is_friday


# Create your views here.
def index(request):
    if request.method != "POST":
        local_ip = get_host_ip()  # 获取本机 IP
        local_port = (sys.argv[-1]).split(":")[-1]  # 获取运行的端口号

        content = show_dir_file()
        is_friday = today_is_friday()  # 今天是周五吗?
        content["is_friday"] = is_friday

        if local_port == "runserver":  # 判断是否是默认运行方式并给出提示
            local_port = "8000"
            error = "请注意, 您目前使用默认方式运行, 其他设备可能无法访问, 请使用 python manage.py runserver 0.0.0.0:8000"
            content["error"] = error

        if local_ip:
            host = "http://{}:{}".format(local_ip, local_port)
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

        if response == "OK":
            return render(request, "success.html")
