# -*- encoding: utf-8 -*-
'''
@文件    :test_normal.py
@说明    :
@时间    :2021/02/23 14:16:46
@作者    :caimiao@kingsoft.com
@版本    :0.1
'''

import unittest

from guangmutools.base import project_root_path

class TestNormalFuncs(unittest.TestCase):
    def testProjectrootpath(self):
        print(project_root_path('f:\\work\\guangmu\\ms_sensitive_check\\controllers\\utils\\admin_helpers.py', 'ms_sensitive_check', 'abc', 'def'))