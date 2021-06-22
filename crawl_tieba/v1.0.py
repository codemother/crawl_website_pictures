import os
import re
import urllib.request
import shutil

#获取一个url的html
def get_html(url):
    req =urllib.request.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36')
    req.add_header('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9')
    response =urllib.request.urlopen(req)
    html =response.read()
    return html

#输入一个贴吧主页的url
def input_url():
    url =str(input('请输入一个贴吧首页的url:'))
    return url

#获取十页的url
def get_allpages_url(url):
    html =get_html(url).decode('utf-8')
    all_pages_url =re.findall(r'a href="(//tie.+)" class=" pagination-item "',html)
    rel_pageurl =[]
    for i in all_pages_url:
        rel ='https:'+i
        rel_pageurl.append(rel)
    return rel_pageurl

#获取每一页中所有项的url
def get_every_url(url):
    html =get_html(url).decode('utf-8')
    all_items_url =re.findall(r'a rel="noreferrer" href="(.+)" title="',html)
    rel_url =[]
    for i in all_items_url:
        rel ='https://tieba.baidu.com'+i
        rel_url.append(rel)
    return rel_url

#获取每一项里首页所有张图片的url
def get_pictures(url):
    html =get_html(url).decode('utf-8')
    eachitem_picture_url =re.findall(r'img class="BDE_Image.+src="(.+jpg)" size',html)
    return eachitem_picture_url

#保存
def save(urls):
    for i in urls:
        filename =re.split(r'/',i)[-1]
        with open(filename, 'wb') as f:
                each_picture_html =get_html(i)
                f.write(each_picture_html)
#主函数
def main():
    try:
        os.mkdir(r'E:\PyCharm 2021.1.2\project\tieba picture')
    except:
        shutil.rmtree(r'E:\PyCharm 2021.1.2\project\tieba picture')
        os.mkdir(r'E:\PyCharm 2021.1.2\project\tieba picture')
    os.chdir(r'E:\PyCharm 2021.1.2\project\tieba picture')
    url =input_url()
    all_pages_url =get_allpages_url(url)
    all_item_url = []
    for x in all_pages_url:
        each_item_url =get_every_url(x)
        all_item_url.append(each_item_url)

    all_pictures_url = []
    number = 1
    for outside in all_item_url:
        for inside in outside:
                eachitem_pictures =get_pictures(inside)
                try:
                    save(eachitem_pictures)
                    print('已保存%d个贴子的所有图片'%number)
                    print('刚刚爬取的帖子：',inside)
                    print('刚刚保存的帖子里的图片：',eachitem_pictures)
                    number += 1
                except:
                    continue

if __name__ =='__main__':
    main()



