#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import socket
import json
import glob
from time import localtime, strftime
from datetime import datetime
from .humansize import approximate_size


def get_host_ip():
    # 优雅的获得 ip 地址
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # 不需要网络连接只要网卡处于工作状态就能取得 ip
        s.connect(('8.8.8.8', 80))
    except:
        # 这个函数一般不会被执行, 假如执行了(没有网的状态)也取不到 ip
        ip = gen_host_ip()
    else:
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip


def gen_host_ip():
    # 获取 ip 的另一种方法
    # 如果 socket 方法无法获得 ip 则读取本地文件中的 ip
    try:
        if os.name == 'nt':
            # Windows 下获取 ip 地址的方法
            ip = [a for a in os.popen('route print').readlines() if ' 0.0.0.0 ' in a][0].split()[-2]
        else:
            # Linux 下获取 ip 地址的方法
            ip = os.popen("ifconfig | grep inet").readlines()[0].strip().split(' ')[1]
    except:
        ip = None

    return ip


def show_dir_info():
    # 返回当前目录下所有文件的 文件名, 访问时间, 文件大小
    files = glob.glob("./static/share/*")  # 返回带相对路径的文件列表

    files_name = show_files_name()
    files_size = []
    files_atime = []

    for file in files:
        files_size.append(approximate_size(os.stat(file).st_size))
        files_atime.append(strftime('%Y-%m-%d %H:%M:%S', localtime(os.stat(file).st_atime)))
    content = {"content": zip(files_name, files_atime, files_size)}

    return content


def show_files_name():
    files = os.listdir('./static/share')

    return files


def upload_to_dir(file_name, file):
    # 上传文件到文件夹
    with open('./static/share/{0}'.format(file_name), 'wb') as f:
        for chunk in file.chunks():
            f.write(chunk)

    return


def today_is_friday():
    # 今天是周五吗
    friday = datetime.now().weekday()
    sunday = datetime.now().weekday()

    if friday == 4:
        friday = True
    else:
        friday = False

    if sunday == 6:
        sunday = True
    else:
        sunday = False

    return friday, sunday


def morning_or_night():
    # 问好
    time_now = strftime("%H:%M", localtime())  # 获取现在的时间
    time_hour = str(datetime.now().time()).split(":")[0]  # 获取现在的小时

    if os.path.exists('./config/time_dict.txt'):
        with open("./config/time_dict.txt", 'r') as f:
            time_dict = json.loads(f.read())
    else:
        time_dict = gen_time_dict()

    return time_dict[time_hour], time_now


def gen_time_dict():
    print("文件不存在, 生成中...")
    time_dict = {"{:02d}".format(i): None for i in range(0, 24)}

    for i in time_dict:
        if i in ["{:02d}".format(i) for i in range(5, 8)]:
            time_dict[i] = "早上"
        elif i in ["{:02d}".format(i) for i in range(8, 12)]:
            time_dict[i] = "上午"
        elif i in ["{:02d}".format(i) for i in range(12, 13)]:
            time_dict[i] = "中午"
        elif i in ["{:02d}".format(i) for i in range(13, 18)]:
            time_dict[i] = "下午"
        elif i in ["{:02d}".format(i) for i in range(18, 19)]:
            time_dict[i] = "傍晚"
        elif i in ["{:02d}".format(i) for i in range(19, 24)]:
            time_dict[i] = "晚上"
        elif i in ["{:02d}".format(i) for i in range(0, 1)]:
            time_dict[i] = "午夜"
        elif i in ["{:02d}".format(i) for i in range(1, 3)]:
            time_dict[i] = "深夜"
        elif i in ["{:02d}".format(i) for i in range(1, 5)]:
            time_dict[i] = "凌晨"

    with open("./config/time_dict.txt", 'w') as f:
        f.write(json.dumps(time_dict))

    return time_dict


def remove_files(file_name):
    # 删除文件
    try:
        os.remove("./static/share/{}".format(file_name))
    except:
        import shutil
        shutil.rmtree("./static/share/{}".format(file_name))

    return


def open_dir():
    # 打开文件夹
    if os.name == 'nt':
        os.startfile(r'.\static\share')
    else:
        import subprocess
        subprocess.Popen(['xdg-open', r"./static/share"])
        # os.startfile(r'./static/share')

    return


if __name__ == '__main__':
    print(get_host_ip())
