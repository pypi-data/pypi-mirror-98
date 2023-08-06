#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@author: yuejl
@application:
@contact: lewyuejian@163.com
@file: setup.py.py
@time: 2021/3/9 0009 22:13
@desc:
'''
#!/usr/bin/env python
# coding: utf-8

from setuptools import setup, find_packages

setup(
    name='mobs', # 项目名称 将来通过pip install mobs安装，不能与其他项目重复，否则上传失败
    version='0.1.2', # 项目版本号
    author='YJ-L',
    author_email='lewyuejian@163.com',
    url='', # 项目的地址，比如github或者gitlib地址
    description=u'Mobs tool', # 项目描述
    #packages=find_packages(),  # 这个函数可以帮你找到包下的所有文件，你可以手动指定 ['jujube_pill'],
    packages=["mobs","mobs.utils"],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ], # 该软件包仅与Python 3兼容，根据MIT许可证进行许可，并且与操作系统无关。您应始终至少包含您的软件包所使用的Python版本，软件包可用的许可证以及您的软件包将使用的操作系统。有关分类器的完整列表，请参阅 https://pypi.org/classifiers/。

    install_requires=[
        'pyyaml',
        'xlrd',
        'loguru',
    ]
    # # 指定入口
    # entry_points={
    #     # 添加命令行脚本
    #     'console_scripts': [
    #         'jujube=jujube_pill:jujube',
    #         'pill=jujube_pill:pill'
    # #     ] # 项目依赖，也可以指定依赖版本
    # }
)