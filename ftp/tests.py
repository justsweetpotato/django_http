# -*- coding: utf-8 -*-

from django.test import TestCase

# Create your tests here.

import os
import glob
import time

SUFFIXES = {1000: ['KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'],
            1024: ['KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB']}


def approximate_size(size, a_kilobyte_is_1024_bytes=True):
    '''Convert a file size to human-readable form.
    Keyword arguments:
    size -- file size in bytes
    a_kilobyte_is_1024_bytes -- if True (default), use multiples of 1024
                                if False, use multiples of 1000
    Returns: string
    '''
    if size < 0:
        raise ValueError('number must be non-negative')

    multiple = 1024 if a_kilobyte_is_1024_bytes else 1000
    for suffix in SUFFIXES[multiple]:
        size /= multiple
        if size < multiple:
            return '{0:.1f} {1}'.format(size, suffix)

    raise ValueError('number too large')


with open("test.txt", 'a') as f:
    f.write("test" * 28 + '\n')

metadate = os.stat("test.txt")
print("                   当前绝对路径:", os.getcwd())
print("带相对路径不包含隐藏文件的文件列表:", glob.glob('../*'))
print("   不带路径包含隐藏文件的文件列表:", os.listdir('../.'))
print("                   文件所有信息:", os.stat('test.txt'))
print("       文件最后一次访问时间(纪元):", metadate.st_atime)
print("            文件最后一次访问时间:", time.localtime(metadate.st_atime))
print("  经过格式化的文件最后一次访问时间:", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(metadate.st_atime)))
print("                   文件字节大小:", metadate.st_size)
print("            经过格式化的文件大小:", approximate_size(metadate.st_size, False))

all_sizes_info = [
    (f, approximate_size(os.stat(f).st_size), time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.stat(f).st_atime)))
    for f in glob.glob("*")]

print("  文件名, 文件大小, 文件访问时间:", all_sizes_info)
print("                  文件绝对路径:", os.path.realpath("test.txt"))
print("           文件相对路径, 文件名:", os.path.split("test.txt"))
print("  文件名(不包含后缀), 文件后缀名:", os.path.splitext("test.txt"))
