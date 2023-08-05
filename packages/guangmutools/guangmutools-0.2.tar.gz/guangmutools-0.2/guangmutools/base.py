# -*- encoding: utf-8 -*-
'''
@文件    :base.py
@说明    :
@时间    :2021/02/22 17:59:21
@作者    :caimiao@kingsoft.com
@版本    :0.1
'''

import os

def project_root_path(cur_file, projectname, *args, **kwargs):

    _project_root_dir = os.path.join(os.path.abspath(os.path.dirname(cur_file)).split(projectname)[0], projectname)
    return os.path.join(_project_root_dir, *args)

