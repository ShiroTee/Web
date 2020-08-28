#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/6/5 11:19
# @Author  : qidl
# @Software: PyCharm

import hashlib

m5 = hashlib.md5()
b = 'admin'.encode(encoding= 'utf-8')
m5.update(b)
str_md5 = m5.hexdigest()
print(str_md5)