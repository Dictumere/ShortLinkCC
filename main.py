import requests
import os
from urllib.parse import urlparse
from dotenv import load_dotenv


def shorten_link(token, url=None):
    url_request = 'https://api.vk.ru/method/utils.getShortLink/'
    payload = {
        'access_token': token,
        'v': '5.199',
        'url': url,
        'private': '0'
    }
    response = requests.post(url_request, json=payload, params=payload)

    answer = response.json()
    if 'error' in answer:
        print(f"Ошибка: {answer['error']['error_msg']}")
    else:
        short_link = answer['response']['short_url']
        return short_link


def count_clicks(token, link=None):
    parsed_link = urlparse(link)
    short_key = parsed_link.path.lstrip('/')
    url_request = 'https://api.vk.ru/method/utils.getLinkStats/'
    payload = {
        'access_token': token,
        'v': '5.199',
        'key': short_key,
        'interval': 'forever'
    }
    response = requests.post(url_request, json=payload, params=payload)

    answer = response.json()
    if 'error' in answer:
        print(f"Ошибка: {answer['error']['error_msg']}")

    elif len(answer['response']['stats']) < 1:
        return 0

    else:
        print(answer)
        clicks_count = answer['response']['stats'][0]['views']
        return clicks_count


def is_shorten_link(url=None):
    url = input('Введите ссылку: ')
    parsed_url = urlparse(url)
    if parsed_url.netloc == "vk.cc":
        count = count_clicks(access_token_vk, url)
        return f'Количество кликов: {count}'
    else:
        short = shorten_link(access_token_vk, url)
        return f'Короткая ссылка: {short}'


if __name__ == '__main__':
    load_dotenv()
    access_token_vk = os.getenv('ACCESS_TOKEN_VK')
    try:
        print(is_shorten_link())
    except requests.exceptions.HTTPError as error:
        print(f'Ошибка HTTP: {error}')
