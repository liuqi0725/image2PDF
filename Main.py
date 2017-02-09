# coding: utf-8
# -------------------------------------------------------------------------------
# Name:         image2pdf
# Purpose:      图片转换pdf
#
# Author:       Liu.Qi
#
# Created:      20/10/2016
# Copyright:    (c) Chengdu Gerdige Technology Co., Ltd.
# -------------------------------------------------------------------------------

import sys

from app.business.ImageProcessService import Convert2PDF

class SysMain:

    def __init__(self, target):
        self.target = target
        self.encoding = 'utf-8'
        self.errors = 'replace'
        self.encode_to = self.target.encoding

    def write(self, s):
        if type(s) == str:
            s = s.decode('utf-8')
        s = s.encode(self.encode_to, self.errors).decode(self.encode_to)
        self.target.write(s)

    def flush(self):
        self.target.flush()

if sys.stdout.encoding == 'cp936':
    sys.stdout = SysMain(sys.stdout)

#log = LoggerHandler.getLogger("main")

# 默认转换路径
rootDir = 'your dir-Path which one that you want to convert' # like '/Users/alexliu/Software/DM/waits/'

Convert2PDF(rootDir)

