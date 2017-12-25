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

## 例子

* 详见 test/filename_sort_test.py


## 文件名排序

大多数情况下,我根据 filename.sort() 进行排序,已经可以满足大多数软件代码生成文件的逻辑。

但是这种方式,不能解决复杂的命名规则。

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
# test_hello_img_1.jpg
# test_hello_img_11.jpg
# test_hello_img_2.jpg
# test_hello_img_21.jpg
# test_hello_img_22.jpg
# test_hello_img_3.jpg
# test_hello_img_4.jpg
# test_hello_img_5.jpg

```


所以我在 `Image2PDF` 的想`convert_images2PDF_one_dir`,新增了一个 `filename_sort_fn`
用作在文件名排序时,进行回调处理。

```python

# 使用

# 如当前要转换的所有图片名如下
file_names = [
    "/User/download/book/test_hello_img_1.jpg",
    "/User/download/book/test_hello_img_2.jpg",
    "/User/download/book/test_hello_img_3.jpg",
    "/User/download/book/test_hello_img_4.jpg",
    "/User/download/book/test_hello_img_5.jpg",
    "/User/download/book/test_hello_img_11.jpg",
    "/User/download/book/test_hello_img_21.jpg",
    "/User/download/book/test_hello_img_22.jpg",
]

# 提供给转换函数使用的回调。
# 回调函数会返回 filepath , 包含文件路径的 filepath
# 每一个文件名回调一次
def fileName_sort_process(filepath):
    # 希望对示例数据中的文件,按照 末尾的数字排序
    # 那么回调函数就要截取这个数字
    filenames = filepath.split("_")
    # 取最后的 *.jpg
    name = filenames[3].split(".")[0]
    # name 因该为 1
    # return 必须为一个可以转换为整形的数据
    return name

convert_images2PDF_one_dir("/User/download/book",filename_sort_fn=fileName_sort_process)

```

> filename_sort_fn 函数，只有在转化一个文件下的所有图片时可以用。（因为在测试中，我发现多文件夹批量操作的，在通过回调来决定排序是件很困难的事情，因为有很多条件要去判断当前是哪个文件夹的内容，要如何排序。反而我使用的多的地方在我用代码生成的文件名，一般以时间戳等方式，name数组的 sort 已经能够满足了。）


