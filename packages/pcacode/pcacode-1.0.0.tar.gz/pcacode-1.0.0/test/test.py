# -*- coding: utf-8 -*-
# @Time    : 2021/3/10 4:05 下午
# @Author  : john
# @Site    : 
# @File    : test.py
# @Software: PyCharm

from pcacode import pcacode
pca=pcacode()
info = pca.get_info(province='北京',content='朝阳区')
print(info)

