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
    """
    转换图片至 PDF
    """

    # 支持的类型
    __allow_type = [".jpg", ".jpeg", ".bmp", ".png"]

    # 获取的文件夹
    __dirs = {}

    # a4的高宽
    __a4_w, __a4_h = landscape(A4)

    __rootDir = ""

    def __init__(self,dirPath,filename_sort_fn=None):
        """
        转换的主函数
        :param dirPath: 转换路径
        :param filename_sort_fn:

        文件名排序的回调函数,当此回调函数有值时,在文件名排序时,会回调,并将 file 的完整路径返回。
        回调函数需要返回一个可转换整形的内容,函数根据此回调函数的返回值,对文件名排序

        比如:
            现实中,文件名会是
            test_01_doc_0.png、
            test_01_doc_1.png、
            test_01_doc_2.png、
            test_01_doc_3.png、
            test_01_doc_11.png、
            test_01_doc_21.png
            等等,我们也希望读取出来的顺序如此,但是 mac、win 下,包括sort 排序出来的结果都不理想。

            结果为
            test_01_doc_0.png、
            test_01_doc_1.png、
            test_01_doc_11.png、
            test_01_doc_2.png、
            test_01_doc_21.png、
            test_01_doc_3.png

            不是我们想要得到的。

            通过 filename_sort_fn(filename) 返回的整形数字,对齐正确的排序

        """
        # 默认路径
        self.rootDir = dirPath
        self.begin(filename_sort_fn)

    # 开始解析
    def begin(self,filename_sort_fn=None):
        for parent, dirnames, filenames in os.walk(self.rootDir):

            for dirname in dirnames:
                # 假设每个文件夹下都有图片，都是一本书
                dirData ={"name":"","pages":[],"isBook":False}
                dirName = dirname.split('/')[0]
                dirData['name'] = dirName
                self.__dirs[dirName] = dirData

            # 查找有无图片
            for filename in filenames:

                real_filename = os.path.join(parent, filename)
                # 取父文件夹名称为书名
                parentDirName = real_filename.split('/')[-2]

                if parentDirName in self.__dirs.keys():
                    dirJsonData = self.__dirs[parentDirName]
                else:
                    continue

                # 检查是否图片
                if real_filename and (os.path.splitext(real_filename)[1] in self.__allow_type):
                    # 将图片添加至书本
                    dirJsonData['pages'].append(real_filename)

                    # 如果该书的isbook 是false 改为true
                    if not dirJsonData['isBook'] :
                        dirJsonData['isBook'] = True

        index = 1
        for dirName in self.__dirs.keys():

            dirData = self.__dirs[dirName]

            if dirData['isBook']:
                print("[*][转换PDF] : 开始. [名称] > [%s]" % (dirName))
                beginTime = time.clock()
                self.convert(dirData,filename_sort_fn)
                endTime = time.clock()
                print("[*][转换PDF] : 结束. [名称] > [%s] , 耗时 %f s " % (dirName,(endTime-beginTime)))
                index += 1

        print("[*][所有转换完成] : 本次转换检索目录数 %d 个，共转换的PDF %d 本 " % (len(self.__dirs),index-1))

    # 转换
    def convert(self,book,filename_sort_fn=None):
        """
        转换图片为 pdf
        :param book:
        :param filename_sort_fn:
        :return:
        """
        bookName = self.rootDir + book['name'] + ".pdf"
        bookPages = book['pages']

        # 对数据进行排序
        if (filename_sort_fn == None):
            # 将按图片按名称的ASCII排序以避免错乱问题
            bookPages.sort()
        else:
            # lambda 匿名函数, 第一个参数定义函数入参,第二个为参数的处理表达式
            # 这样理解
            # def getName(name):
            #   return name.split("-")[1]
            #
            # 用匿名函数就这么表示
            # name = lambda name:name.split("-")[1]
            # xname = name("haha-dd-23")
            #
            # 支持多个参数
            #
            bookPages = sorted(bookPages, key=lambda name: int(filename_sort_fn(name)))

        bookPagesData = []

        bookDoc = SimpleDocTemplate(bookName, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)

        for bookPage in bookPages:

            img_w , img_h = ImageTools().getImageSize(bookPage)

            #img_w = img.imageWidth
            #img_h = img.imageHeight


            if self.__a4_w / img_w < self.__a4_h / img_h:
                ratio = self.__a4_w / img_w
            else:
                ratio = self.__a4_h / img_h

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
