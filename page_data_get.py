from bs4 import BeautifulSoup
from csv import writer
import os
import requests
import re
from tqdm import tqdm
import threading
import csv
import concurrent.futures

#GETTING CAR LINKS FROM MARKET PAGES
def get_pages(page_link:str) -> None:
    try:
        page_num = 1
        while page_num < 101:
            print('Working with page: ', page_link)
            html_page = requests.get(url = page_link)
            soup = BeautifulSoup(html_page.content, features='html.parser')
            if len(soup.find_all('a', class_='css-xb5nz8 ewrty961')) > 0:
                auto_links = soup.find_all('a', class_='css-xb5nz8 ewrty961')
                file = open('auto_links.csv', 'a', encoding='utf-8')
                for auto_link in auto_links:
                    print(auto_link.get('href'))
                    file.write(auto_link.get('href')+'\n')
                file.close()
                page_num += 1
                page_link = re.sub(r'page(\d+)', f'page{page_num}', page_link)
                print('OK')
            else:
                print('404, ', page_link)
                page_num = 1000
    except Exception as e:
        with open('logs.txt', 'a', encoding='utf-8') as log_file:
            log_file.write(str(e))
            log_file.close()

#GETTING CAR DATA FROM CAR PAGE
def get_auto_info(link:str) -> None:
    try:
        data = requests.get(link)
        full_data_dict = {}
        soup = BeautifulSoup(data.content, features='html.parser')
        title = soup.find('span', class_='css-1kb7l9z e162wx9x0').text.replace('Продажа', '').split('год')[0].strip()
        full_data_dict['Title'] = title
        data_block = soup.find('div', class_='css-0 epjhnwz1')
        price = data_block.find('div', class_="css-eazmxc e162wx9x0").text.replace('&nbsp;', '').replace('\xa0', '').strip()
        full_data_dict['Price'] = price
        info_table = data_block.find('table', class_="css-xalqz7 eppj3wm0")
        info_rows = info_table.find_all('tr')
        print(len(info_rows))

        for row in info_rows:
            try:
                key = row.find('th', class_='css-16lvhul ezjvm5n1').text.replace('\xa0', '').strip()
                value = row.find('td', class_='css-9xodgi ezjvm5n0').text.replace('\xa0', '').strip()
                full_data_dict[key] = value
            except:
                pass

        photos = soup.find('div', class_='css-1xr2wur e10f100')
        photos_links = [link.get('href') for link in photos.find_all('a')]

        full_data_dict['photo_list'] = photos_links
        print(full_data_dict)
        file_name = link.split('/')[-1].replace('.html', '')
        with open(f'autos/{file_name}.csv', 'w', encoding='utf-8', newline='') as dst_file:
            order = ['name', 'value']
            csv.DictWriter(dst_file, fieldnames=order).writeheader()
            for keys, values in full_data_dict.items():
                # print(keys, values)
                data = {'name': keys, 'value': values}
                csv.DictWriter(dst_file, fieldnames=list(data)).writerow(data)
            dst_file.close()
    except Exception as e:
        with open('logs.txt', 'a', encoding='utf-8') as log_file:
            log_file.write(str(e))
            log_file.close()

def parser_start():
    file = open('links_by_price.csv', 'r', encoding='utf-8')
    links = file.read().strip().split('\n')
    file.close()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(get_pages, links)

    file = open('auto_links.csv', 'r', encoding='utf-8')
    car_urls = file.read().strip().split('\n')
    file.close()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(get_auto_info, car_urls)


if __name__ == '__main__':
    parser_start()