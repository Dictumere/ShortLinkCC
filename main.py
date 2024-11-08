import requests
import os
from urllib.parse import urlparse
from dotenv import load_dotenv


def shorten_link(token, url):
    request_url = 'https://api.vk.ru/method/utils.getShortLink/'
    payload = {
        'access_token': token,
        'v': '5.199',
        'url': url,
        'private': '0'
    }
    response = requests.post(request_url, json=payload, params=payload)
    response.raise_for_status()

    answer = response.json()
    if 'error' in answer:
        raise ValueError(f"{answer['error']['error_msg']}")
    else:
        short_link = answer['response']['short_url']
        return short_link


def count_clicks(token, link):
    parsed_link = urlparse(link)
    short_key = parsed_link.path.lstrip('/')
    request_url = 'https://api.vk.ru/method/utils.getLinkStats/'
    payload = {
        'access_token': token,
        'v': '5.199',
        'key': short_key,
        'interval': 'forever'
    }
    response = requests.post(request_url, json=payload, params=payload)
    response.raise_for_status()

    answer = response.json()
    if 'error' in answer:
        raise ValueError(f"{answer['error']['error_msg']}")

    clicks_count = answer['response'].get('stats', [])
    if not clicks_count:
        return 0


def is_shorten_link(token, url):
    # parsed_url = urlparse(url)
    # return parsed_url.netloc == "vk.cc"
    answer = shorten_link(token, url)
    if answer['error']['error_msg'] == 100:
        count_clicks(token, url)


if __name__ == '__main__':
    load_dotenv()
    access_vk_token = os.environ['ACCESS_VK_TOKEN']
    url = input('Введите ссылку: ')

    try:
        if is_shorten_link(url):
            count = count_clicks(access_vk_token, url)
            print(f'Количество кликов: {count}')
        else:
            short = shorten_link(access_vk_token, url)
            print(f'Короткая ссылка: {short}')
    except requests.exceptions.HTTPError as error:
        print(f'Ошибка HTTP: {error}')
    except requests.exceptions.ConnectionError as error:
        print(f'Ошибка соединения: {error}')
