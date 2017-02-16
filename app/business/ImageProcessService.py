# -------------------------------------------------------------------------------
# Name:         PTools
# Purpose:      转换PDF
#
# Author:       Liu.Qi
#
# Created:      20/10/2016
# Copyright:    (c) Chengdu Gerdige Technology Co., Ltd.
# -------------------------------------------------------------------------------

import os

from reportlab.platypus import SimpleDocTemplate,Image, PageBreak
from reportlab.lib.pagesizes import A4, landscape

import time

from PIL import Image as pilImage

class Convert2PDF:

    # 支持的类型
    Const_Image_Format = [".jpg", ".jpeg", ".bmp", ".png"]

    # 获取的文件夹
    dirs = {}

    # a4的高宽
    a4_w, a4_h = landscape(A4)

    rootDir = ""

    def __init__(self,dirPath):
        # 默认路径
        self.rootDir = dirPath
        self.begin()

    # 开始解析
    def begin(self):
        for parent, dirnames, filenames in os.walk(self.rootDir):
            for dirname in dirnames:
                # 假设每个文件夹下都有图片，都是一本书
                dirData ={"name":"","pages":[],"isBook":False}
                dirName = dirname.split('/')[0]
                dirData['name'] = dirName
                self.dirs[dirName] = dirData

            # 查找有无图片
            for filename in filenames:

                real_filename = os.path.join(parent, filename)
                # 取父文件夹名称为书名
                parentDirName = real_filename.split('/')[-2]

                if parentDirName in self.dirs.keys():
                    dirJsonData = self.dirs[parentDirName]
                else:
                    continue

                # 检查是否图片
                if real_filename and (os.path.splitext(real_filename)[1] in self.Const_Image_Format):
                    # 将图片添加至书本
                    dirJsonData['pages'].append(real_filename)

                    # 如果该书的isbook 是false 改为true
                    if not dirJsonData['isBook'] :
                        dirJsonData['isBook'] = True

        index = 1
        for dirName in self.dirs.keys():

            dirData = self.dirs[dirName]

            if dirData['isBook']:
                print("[*][转换PDF] : 开始. [名称] > [%s]" % (dirName))
                beginTime = time.clock()
                self.convert(dirData)
                endTime = time.clock()
                print("[*][转换PDF] : 结束. [名称] > [%s] , 耗时 %f s " % (dirName,(endTime-beginTime)))
                index += 1

        print("[*][所有转换完成] : 本次转换检索目录数 %d 个，共转换的PDF %d 本 " % (len(self.dirs),index-1))

    #
    # 开始转换
    #
    def convert(self,book):

        bookName = self.rootDir + book['name'] + ".pdf"
        bookPages = book['pages']

        bookPagesData = []

        bookDoc = SimpleDocTemplate(bookName, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)

        for bookPage in bookPages:

            img_w , img_h = ImageTools().getImageSize(bookPage)

            #img_w = img.imageWidth
            #img_h = img.imageHeight


            if self.a4_w / img_w < self.a4_h / img_h:
                ratio = self.a4_w / img_w
            else:
                ratio = self.a4_h / img_h

            data = Image(bookPage, img_w * ratio, img_h * ratio)
            bookPagesData.append(data)
            bookPagesData.append(PageBreak())

        try:
            bookDoc.build(bookPagesData)
            #print("已转换 >>>> " + bookName)
        except Exception as err:
            print("[*][转换PDF] : 错误. [名称] > [%s]" % (bookName))
            print("[*] Exception >>>> ",err)

class ImageTools :

    def getImageSize(self,imagePath):
        img = pilImage.open(imagePath)
        return img.size