# Django 文件传输工具

使用 Django 框架完成的简单、小巧的文件传输工具,  支持下载与上传文件到指定文件夹, 让您在局域网中、 主机和虚拟机之间方便的传输文件.
<br>
![界面](https://raw.githubusercontent.com/justsweetpotato/makedown-img-store/master/ftp/django_http.png)

### 一、安装依赖
#### 1.1 Python 安装
<a href="https://www.python.org/downloads/">Python</a>

#### 1.2. Django 框架安装
打开 Windows 命令提示符:<br>
安装最新版 Django.
```
$ pip install Django
```
或者更新 Django 到最新版.
```
$ pip install --upgrade django
```

### 二、运行
<del>$ python manage.py migrate  # 仅执行一次</del>
```
$ cd django_ftp
$ python manage.py runserver 0.0.0.0:8000
```
"0.0.0.0:8000"
<br>
"0.0.0.0" 表示运行在本地并开放来自任何地址的访问.
<br>
"8000" 表示运行的端口, 可自定.

### 三、连接
在本机运行之后, 在本机浏览器上访问 http://127.0.0.1:8000<br>
页面会自动提示局域网下其他设备应该访问的地址.<br>
共享的文件保存在 django_http/static/share 目录下.<br>
出于安全性的考虑, 只有主机(当前运行此程序的电脑)可以通过页面按钮"打开文件夹"与"删除文件". 

### 一些问题
<del>程序使用 file.write() 写入文件, 所以上传超过 1G 的大文件可能会出现问题, 正在计划使用模型的方式改善这个功能.</del>
<br>
目前不支持文件夹下载与上传, 请打包后分享, 正在计划改善这个功能(大误).
<br>

### 计划更新
[X] 增加侧面留言板功能, 拖延中...<br>
[X] 将权限改为登录账号后获得, 进行中...<br>
[O] 只有主机才有删除功能的权限, 已完成...<br>
[O] 打开文件夹功能已完成...<br>
[O] 删除功能已完成...<br>
 
