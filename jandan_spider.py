import requests
from bs4 import BeautifulSoup

index = 0


# 保存图片
def save_jpg(res_url):
    global index
    html = BeautifulSoup(requests.get(res_url).text)
    for link in html.find_all('a', {'class': 'view_img_link'}):
        with open('{}.{}'.format(index, link.get('href')[len(link.get('href'))-3: len(link.get('href'))]), 'wb') as jpg:
            jpg.write(requests.get(link.get('href')).content)
        index += 1


#  抓取煎蛋妹子图片，默认抓取5页
if __name__ == '__main__':
    url = 'http://jandan.net/ooxx'
    for i in range(0, 5):
        save_jpg(url)
        url = BeautifulSoup(requests.get(url).text).find('a', {'class': 'previous-comment-page'}).get('href')
