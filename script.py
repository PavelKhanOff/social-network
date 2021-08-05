import configparser
import requests
from faker import Faker
import random
from time import time
from typing import List
config = configparser.ConfigParser()
config.read('config.ini')

NUMBER_OF_USERS = int(config.get('SETTINGS', 'number_of_users'))
MAX_POSTS_PER_USER = int(config.get('SETTINGS', 'max_posts_per_user'))
MAX_LIKES_PER_USER = int(config.get('SETTINGS', 'max_likes_per_user'))
fake = Faker()


def main() -> str:
    start_time: time = time()
    users_token: List = [register_and_get_token({
        'username': fake.simple_profile()['username']
                    + fake.simple_profile()['username'],
        'password': fake.password(),
        'email': fake.email()
    }) for number in range(NUMBER_OF_USERS)]
    posts_list: List = []
    for token in users_token:
        users_post: List = [create_post(token) for number in
                      range(random.randint(1, MAX_POSTS_PER_USER))]
        posts_list += users_post
    like_list: List = []
    for token in users_token:
        user_like: List = [like_post(post, token) for post in random.sample(
            posts_list, random.randint(1, MAX_LIKES_PER_USER))]
        like_list += user_like
    end_time: time = time()
    return (f'Создано {len(posts_list)} поста(ов) и '
            f'{len(like_list)} лайков за '
            f'{round(end_time-start_time, 2)} секунд.')


def signup(data):
    url: str = 'http://127.0.0.1:8000/api/users/'
    try:
        response = requests.post(url=url, json=data, timeout=8)
    except requests.exceptions.ConnectionError as e:
        return {'message': f'Connection error: {e}'}
    except Exception as e:
        return {'message': f'Exception caught: {e}'}
    return response.json()


def get_token(data):
    url = 'http://127.0.0.1:8000/api/token/'
    try:
        response = requests.post(url=url, json=data, timeout=8)
    except requests.exceptions.ConnectionError as e:
        return {'message': f'Connection error: {e}'}
    except Exception as e:
        return {'message': f'Exception caught: {e}'}
    return response.json().get('access')


def create_post(token):
    url = 'http://127.0.0.1:8000/api/posts/'
    headers = {'Content-Type': 'application/json',
               'Authorization': 'Bearer ' + token}
    data = {
        'title': fake.name() + "'s Post",
        'text': fake.paragraph(nb_sentences=1)
    }
    try:
        response = requests.post(
            url=url, headers=headers, json=data, timeout=8)
    except requests.exceptions.ConnectionError as e:
        return {'message': f'Connection error: {e}'}
    except Exception as e:
        return {'message': f'Exception caught: {e}'}
    return response.json()['id']


def like_post(post_id, token):
    url = f'http://127.0.0.1:8000/api/posts/{post_id}/like/'
    headers = {'Content-Type': 'application/json',
               'Authorization': 'Bearer ' + token}
    try:
        response = requests.get(url=url, headers=headers, timeout=8)
    except requests.exceptions.ConnectionError as e:
        return {'message': f'Connection error: {e}'}
    except Exception as e:
        return {'message': f'Exception caught: {e}'}
    if response.text != '"Лайк успешно поставлен"':
        return 'ошибка', post_id
    return response.text


def register_and_get_token(data):
    signup(data)
    return get_token(data)


print(main())
