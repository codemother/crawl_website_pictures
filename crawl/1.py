import urllib.request
import os
import base64


# 定义一个读取源码的函数，方便后面代码的引用
def url_open(url):
    # 获取url
    req = urllib.request.Request(url)
    # 设置头信息模拟浏览器
    req.add_header('User-Agent',
                   'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36')
    # 访问
    response = urllib.request.urlopen(req)
    # 读取源码
    html = response.read()
    return html


# 定义一个获取页码的函数
def get_num(url):
    html = url_open(url).decode('utf-8')
    # 查找需要的图片所在页在代码中的位置,这里加上偏移量后刚好到页码前的一个字符
    a = html.find('current-comment-page') + 23
    # 从起始位置a开始查找，目标是页码后的一个字符
    b = html.find(']', a)
    # 返回从a到b的值，即页码
    return html[a:b]


# 定义一个在已知地址寻找图片的函数
def find_imgs(url):
    html = url_open(url).decode('utf-8')
    img_addrs = []
    # 对于find()，找不到会返回-1，找到了会返回开始的索引值
    a = html.find('img src=')
    while a != -1:
        b = html.find('.jpg', a, a + 255)
        if b != -1:
            img_addrs.append(html[a + 9:b + 4])
        else:
            b = a + 9
        a = html.find('img src =', b)
    return img_addrs


# 保存图片
def save_imgs(folder, img_addrs):
    for each in img_addrs:
        filename = each.split('/')[-1]
        with open(filename, 'wb')as f:  # 首先执行with后的open，值返回给as后的f，然后运行下面的语句
            img = url_open('http:' + each)
            f.write(img)


# 主程序
def download(folder='girl pictures', pages=10):
    # 在当前目录创建文件夹，名称girl pictures
    os.mkdir(folder)
    # os.chdir()方法用于改变当前工作目录到指定的路径.这里就是将路径切换到folder
    os.chdir(folder)

    url = 'http://jandan.net/girl/'
    page_num = int(get_num(url))

    for i in range(pages):
        page_num -= i
        # 网址使用了加密技术，这里我们把解密后经过改写的地址再次加密，和其他字符串拼接，最终显示出网站使用的url
        # base64的加密需要输入bytles格式，所以这里用encode()转换
        # strip()是用来去除字符串首尾指定字符的，这里用来去除加密后产生的'b'
        # eval()是用来去除字符串首尾的双引号的，这里因为格式化字符串时里面本身就带有引号，导致最终多了一对引号
        code = '20210604' + '-' + str(page_num)
        page_url = url + eval(str(base64.b64encode(code.encode())).strip('b')) + '#comments'
        img_addrs = find_imgs(page_url)
        save_imgs(folder, img_addrs)


# if __name__ == '__main__'的意思是：当.py文件被直接运行时，if __name__ == '__main__'之下的代码块将被运行；当.py文件以模块形式被导入时，if __name__ == '__main__'之下的代码块不被运行。
if __name__ == '__main__':
    download()