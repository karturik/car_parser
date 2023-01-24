import re
import requests

minprice = 1000
maxprice = 2000

url = f'https://auto.drom.ru/all/page2/?minprice={minprice}&maxprice={maxprice}'

def get_pages(url):
    pass

for time in range(1, 100000):
    url = f'https://auto.drom.ru/all/page1/?minprice={str(minprice)}&maxprice={str(maxprice)}'
    with open('links_by_price.csv', 'a', encoding='utf-8') as file:
        file.write(url+'\n')
        file.close()
    minprice = maxprice+1
    maxprice = maxprice+1000
