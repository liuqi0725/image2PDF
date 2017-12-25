# image2PDF

> Dev-language: python3.x 以上

> python 依赖包：reportlab、PIL

> Version:V1.0.1

> Author:liu.qi

## 特性：

* 将图片转换至PDF，适用于批量转换。如漫画。图片文档等。
* 自动对图片大小进行处理，适用与kindle、iphone、ipad等终端。
* 支持多重文件路径检索进行转换。
* 支持jpg、png、bmp


## 文件名排序

大多数情况下,我根据 filename.sort() 进行排序,但是这种方式,不能解决复杂的命名规则。

如: 
```python

file_names = [
    "test_hello_img_1.jpg",
    "test_hello_img_2.jpg",
    "test_hello_img_3.jpg",
    "test_hello_img_4.jpg",
    "test_hello_img_5.jpg",
    "test_hello_img_11.jpg",
    "test_hello_img_21.jpg",
    "test_hello_img_22.jpg",
]

file_names.sort()

for file_name in file_names:
    print(file_name)
    
# 得到的是
test_hello_img_1.jpg
test_hello_img_11.jpg
test_hello_img_2.jpg
test_hello_img_21.jpg
test_hello_img_22.jpg
test_hello_img_3.jpg
test_hello_img_4.jpg
test_hello_img_5.jpg

```





