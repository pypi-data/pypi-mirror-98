# -*- coding: UTF-8 -*-

import sys
reload(sys)  # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入
sys.setdefaultencoding('utf-8')

from setuptools import setup, find_packages

setup(
    name="shopex_dingding_note_2.x",
    version=1.4,
    description="ShopEx dingding notify for python",
    long_description_content_type=open("README.md").read(),
    packages=find_packages(),
    author="ShopEx",
    author_email="xuhongtao@shopex.cn",
    license="LGPL",
    url="https://github.com/magic119/shopex_dingding_note_2.x.git",
    platforms=["README.md"],
    python_requires=">=2.7.0, <2.7.18",
)