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

    # 获取的书本
    books = []

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
                # 查找有无图片
                self.findImage(os.path.join(parent, dirname))

        print("共找到 %d 本书需要转换" % len(self.books))

        index = 1
        for book in self.books:
            print("转换第 %d 本书[%s]开始..." % (index,book['name']))
            beginTime = time.clock()
            self.convert(book)
            endTime = time.clock()
            print("转换第 %d 本书[%s]结束，耗时 %f s " % (index ,book['name'],(endTime-beginTime)))
            index += 1

    #
    # 找到对应目录下的图片文件
    #
    def findImage(self,dirPath):
        book = {}
        bookpages = []
        makebook = False

        for parent, dirnames, filenames in os.walk(dirPath):
            for filename in filenames:

                real_filename = os.path.join(parent, filename)
                # 取父文件夹名称为书名
                bookName = real_filename.split('/')[-2]

                # 检查是否图片
                if real_filename and (os.path.splitext(real_filename)[1] in self.Const_Image_Format):
                    bookpages.append(real_filename)

                    if not makebook:
                        book["name"] = bookName
                        book["pages"] = bookpages
                        makebook = True
        if book:
            self.books.append(book)

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

            #print("ratio="+ str(ratio) +" , im_w * ratio = " + str(img_w * ratio) +" , im_h * ratio = "+ str(img_h * ratio))
            data = Image(bookPage, img_w * ratio, img_h * ratio)
            bookPagesData.append(data)
            bookPagesData.append(PageBreak())

        bookDoc.build(bookPagesData)

        print("已转换 >>>> "+bookName)



class ImageTools :

    def getImageSize(self,imagePath):
        img = pilImage.open(imagePath)
        return img.size