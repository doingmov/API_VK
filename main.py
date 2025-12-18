import requests
import os
from dotenv import load_dotenv


load_dotenv()

VK_TOKEN = os.getenv('API_VK')

def shorten_link(token, url):
    api_url = 'https://api.vk.com/method/utils.getShortLink'
    params = {
        'url': url,
        'access_token': token,
        'v': '5.199'
    }

    try:
        response = requests.get(api_url, params=params)
        data = response.json()
    except requests.RequestException:
        return 'Ошибка: ошибка запроса к VK API'
    except ValueError:
        return 'Ошибка: ответ от VK API не является JSON'

    if 'error' in data:
        return f"Ошибка: {data['error']['error_msg']}"

    if 'response' in data and 'short_url' in data['response']:
        return data['response']['short_url']

    return 'Ошибка: не удалось получить короткую ссылку'


def count_clicks(token, short_url):
    api_url = 'https://api.vk.com/method/utils.getLinkStats'
    params = {
        'access_token': token,
        'link': short_url,
        'v': '5.199'
    }

    try:
        response = requests.get(api_url, params=params)
        data = response.json()
    except requests.RequestException:
        return 'Ошибка: ошибка запроса к VK API'
    except ValueError:
        return 'Ошибка: ответ от VK API не является JSON'

    if 'error' in data:
        return f"Ошибка: {data['error']['error_msg']}"

    if 'response' in data and 'clicks' in data['response']:
        return data['response']['clicks']

    return 'Ошибка: не удалось получить количество кликов'


def is_short_link(url):
    return url.startswith("https://vk.cc/") or url.startswith("http://vk.cc/")


if __name__ == "__main__":
    user_url = input("Введите ссылку: ").strip()

    if is_short_link(user_url):
        clicks = count_clicks(VK_TOKEN, user_url)
        print(clicks)
    else:
        short = shorten_link(VK_TOKEN, user_url)
        print(short)
