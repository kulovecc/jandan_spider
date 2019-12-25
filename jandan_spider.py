import os
import requests
from bs4 import BeautifulSoup
import argparse
import ast
import atexit
import multiprocessing

parser = argparse.ArgumentParser(description='Spider for jiandan.net')
parser.add_argument('--page', dest='page', action='store', default=5, type=int, help='max page number')
parser.add_argument('--dir', dest='dir', action='store', default='images', help='the dir where the image save')
args = parser.parse_args()

page = args.page
_dir = args.dir
if not os.path.exists(_dir):
    os.mkdir(_dir)
headers = {'referer': 'http://jandan.net/',
           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0'}

image_cache = set()

if os.path.exists(".cache"):
    with open('.cache', 'r') as f:
        image_cache = ast.literal_eval(f.read(-1))


@atexit.register
def hook():
    with open('.cache', 'w+') as f:
        f.write(str(image_cache))


index = len(image_cache)


# 保存图片
def save_jpg(res_url):
    global index
    html = BeautifulSoup(requests.get(res_url, headers=headers).text, features="html.parser")
    for link in html.find_all('a', {'class': 'view_img_link'}):
        if link.get('href') not in image_cache:
            with open(
                    '{}/{}.{}'.format(_dir, index, link.get('href')[len(link.get('href')) - 3: len(link.get('href'))]),
                    'wb') as jpg:
                jpg.write(requests.get("http:" + link.get('href')).content)
            image_cache.add(link.get('href'))
            print("正在抓取第%s条数据" % index)
            index += 1


if __name__ == '__main__':
    url = 'http://jandan.net/ooxx'
    for i in range(0, page):
        save_jpg(url)
        ahref = BeautifulSoup(requests.get(url, headers=headers).text, features="html.parser").find('a', {'class': 'previous-comment-page'})
        if ahref is None:
            print('no more page')
            exit(0)
        else:
            url = "http:" + ahref.get('href')
