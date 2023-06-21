import re
import requests
import bs4
import fake_headers
import json


def get_headers():
    class_object = fake_headers.Headers()
    headers = class_object.generate()
    return headers


def write_json(file):
    with open('vacancy.json', 'w') as file_json:
        json.dump(file, file_json)


def get_vacancy(url, pattern):
    result = requests.get(url, headers=get_headers())
    html = result.text
    soup = bs4.BeautifulSoup(html, 'lxml')
    div = soup.find('div', id='a11y-main-content')
    list_vacancy = []
    for vacancy in div.find_all(class_='vacancy-serp-item-body'):
        dict_ads = {}
        if re.search(pattern, str(vacancy.find_all('h3'))):
            href = vacancy.find(class_="serp-item__title").get('href')
            city = vacancy.find(class_='vacancy-serp-item__info').find('div', attrs={'data-qa': 'vacancy-serp__vacancy'
                                                                                             '-address'}).contents[0]
            company = vacancy.find(class_='vacancy-serp-item__info').find('div', class_='bloko-v-spacing-container '
                                                                                    'bloko-v-spacing-container_base-2').find('a', attrs={'data-qa':'vacancy-serp__vacancy-employer'}).contents[0]
            if vacancy.find('span', class_='bloko-header-section-3') is not None:
                salary = vacancy.find('span', class_='bloko-header-section-3').contents[0]
                dict_ads['salary'] = salary.replace('\u202f', '')
            else:
                salary = 'Нет информации'
                dict_ads['salary'] = salary
            dict_ads['href'] = href
            dict_ads['city'] = city
            dict_ads['company'] = company.replace('\xa0', '')
            list_vacancy.append(dict_ads)
    return list_vacancy

url = r'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2'
pattern = r'([Dd]jango|[Ff]lask)'

if __name__ == '__main__':
    vacancy = get_vacancy(url, pattern)
    write_json(vacancy)