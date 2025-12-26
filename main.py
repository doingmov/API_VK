import requests
import os
from dotenv import load_dotenv


def shorten_link(token, url):
    api_url = 'https://api.vk.com/method/utils.getShortLink'
    params = {
        'url': url,
        'access_token': token,
        'v': '5.199'
    }

    response = requests.get(api_url, params=params)
    response.raise_for_status()

    vk_response = response.json()
    if 'error' in vk_response:
        raise RuntimeError(vk_response['error']['error_msg'])

    return vk_response['response']['short_url']


def count_clicks(token, short_url):
    api_url = 'https://api.vk.com/method/utils.getLinkStats'
    params = {
        'access_token': token,
        'link': short_url,
        'v': '5.199'
    }

    response = requests.get(api_url, params=params)
    response.raise_for_status()

    vk_response = response.json()
    if 'error' in vk_response:
        raise RuntimeError(vk_response['error']['error_msg'])

    return vk_response['response']['clicks']


def is_short_link(token, url):
    api_url = 'https://api.vk.com/method/utils.getLinkStats'
    params = {
        'access_token': token,
        'link': url,
        'v': '5.199'
    }
    
    response = requests.get(api_url, params=params)
    response.raise_for_status()
    vk_response = response.json()
    if 'error' in vk_response:
        return False

    return 'response' in vk_response and 'clicks' in vk_response['response']


def main():
    load_dotenv()
    vk_token = os.environ('VK_TOKEN')
    user_url = input('Введите ссылку: ').strip()

    try:
        if is_short_link(vk_token, user_url):
            clicks = count_clicks(vk_token, user_url)
            print(f'Количество кликов: {clicks}')
        else:
            short_link = shorten_link(vk_token, user_url)
            print(f'Короткая ссылка: {short_link}')

    except requests.ConnectionError:
        print('Ошибка сети: не удалось подключиться к VK API')
    except requests.HTTPError as error:
        print(f'HTTP ошибка при обращении к VK API: {error}')
    except RuntimeError as error:
        print(f'Ошибка VK API: {error}')


if __name__ == '__main__':
    main()

