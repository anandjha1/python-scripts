from bs4 import BeautifulSoup
from lxml import etree
import requests

base_url = 'https://xkcd.com/'
url = base_url+'/1'

while '#' not in url:
    html_page = requests.get(url)
    soup = BeautifulSoup(html_page.content, 'lxml')
    img_link = soup.find('div', id='comic').find('img')['src']
    img_name = img_link.split('/')[-1]
    img_link = 'https:' + img_link
    img_data = requests.get(img_link)
    # print(img_data)
    with open('images/'+img_name, 'wb') as img_file:
        img_file.write(img_data.content)

    print(img_name)
    next_link = soup.find('a', rel='next')
    url = base_url + next_link['href']
