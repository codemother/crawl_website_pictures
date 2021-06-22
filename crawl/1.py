import urllib.request
import os
import base64
import re
import datetime
import shutil

#定义一个读取源码的函数，方便后面代码的引用
def url_open(url):
    # 获取url
    req = urllib.request.Request(url)
    # 设置头信息模拟浏览器
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36')
    # 访问
    response = urllib.request.urlopen(req)
    # 读取源码
    html = response.read()
    return html

#定义一个获取页码的函数
def get_num(url):
    html = url_open(url).decode('utf-8')
    a =re.search(r'"current-comment-page">(\[\d+\])',html)
    b =a.group(1)
    c =re.search(r'\d+',b)
    return c.group()

#获取当前日期
def get_date():
    today =datetime.date.today()
    today_format =re.sub('-','',str(today))
    return today_format

#定义一个在已知地址寻找图片的函数
def find_imgs(url):
    page_html = url_open(url).decode('utf-8')
    all_img_url_0 =re.findall(r'a href="(//wx.+jpg)" target=',page_html)
    all_img_url_1 =[]
    for i in all_img_url_0:
        i ='http:'+i
        all_img_url_1.append(i)
    return all_img_url_1

#定义一个保存的函数
def save_imgs(all_img_urls):
    for each_img_url in all_img_urls:
        filename =re.split('/',each_img_url)[-1]
        # 一般用下面这种方式在当前目录创建一个名为filename的文件，下面的语句是对这个文件的操作
        with open(filename,'wb') as f:
            each_img_html =url_open(each_img_url)
            f.write(each_img_html)

def main(folder = 'girl pictures',pages = 10):
	try:
	    #在当前目录创建文件夹，名称girl pictures
	    os.mkdir(folder)
	except:
		print('检测到之前存在的文件，将覆盖')
		shutil.rmtree(folder)#删除原有文件夹
        os.mkdir(folder)#创建新的同名文件夹
    #os.chdir()方法用于改变当前工作目录到指定的路径.这里就是将路径切换到folder
    os.chdir(folder)

    url = 'http://jandan.net/girl'
    page_num = int(get_num(url))

    for i in range(pages):
        page_num -= i
        #网址使用了加密技术，这里我们把解密后经过改写的地址再次加密，和其他字符串拼接，最终显示出网站使用的url
        #base64的加密需要输入bytles格式，所以这里用encode()转换
        #strip()是用来去除字符串首尾指定字符的，这里用来去除加密后产生的'b'
        #eval()是用来去除字符串首尾的双引号的，这里因为格式化字符串时里面本身就带有引号，导致最终多了一对引号
        code = get_date() + '-' + str(page_num)
        page_url = url +'/'+ eval(str(base64.b64encode(code.encode())).strip('b')) + '#comments'
        all_img_urls = find_imgs(page_url)
        save_imgs(all_img_urls)

#if __name__ == '__main__'的意思是：当.py文件被直接运行时，if __name__ == '__main__'之下的代码块将被运行；当.py文件以模块形式被导入时，if __name__ == '__main__'之下的代码块不被运行。
if __name__=='__main__':
    main()
