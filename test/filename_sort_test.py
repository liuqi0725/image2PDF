# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# @File     : test.py
# @Created  : 2017/12/25 下午1:21
# @Software : PyCharm
# 
# @Author   : Liu.Qi
# @Contact  : liuqi_0725@aliyun.com
# 
# @Desc     : 目的?
# -------------------------------------------------------------------------------

from Image2PDF import convert_images2PDF_one_dir,convert_images2PDF_more_dirs

def name_val(file_path):
    # 文件路径为 /Users/alexliu/test/one_book/test_hello_img_*.jpg
    names = file_path.split("_")
    names = names[3].split(".")
    # names [0] 为 *.jpg 的数字表示
    return names[0]

# 转换一本书,按照数组的sort的排序规则排序  名称可以为空
# convert_images2PDF_one_dir("/Users/alexliu/test/one_book",save_name="test.pdf")

# 转换一本书,并且执行排序的回调函数 名称为 test_hello_img_1.jpg 这种类型,我要按照 数字排序
# convert_images2PDF_one_dir("/Users/alexliu/test/one_book",filename_sort_fn=name_val)

# 转换多本书
convert_images2PDF_more_dirs("/Users/alexliu/test/books")