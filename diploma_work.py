import requests
import time


user = 5030613
TOKEN = '7b23e40ad10e08d3b7a8ec0956f2c57910c455e886b480b7d9fb59859870658c4a0b8fdc4dd494db19099'


def get_friends(user_id):
    friends_params = {
        'user_id': user_id,
        'order': 'name',
        'access_token': TOKEN,
        'v': '5.74'
    }

    friends_json = requests.get('https://api.vk.com/method/friends.get?', friends_params)
    friends_dict = friends_json.json()['response']
    return set(friends_dict['items'])


def get_groups(user_id):
    group_params = {
        'user_id': user_id,
        # 'extended': 1,
        'count': '1000',
        'access_token': TOKEN,
        'v': '5.74'
    }

    group_json = requests.get('https://api.vk.com/method/groups.get?', group_params)
    # print(type(group_json), group_json)
    # print(group_json.text.encode('utf-8'))
    # print(group_json.response)
    # exit(0)
    group_dict = group_json.json()['response']
    return set(group_dict['items'])


def search_group_user(group_set, friends_set):
    print('Ищем совпадения')
    groups = []
    for group in group_set:
        group_params = {
            'group_id': group,
            'access_token': TOKEN,
            'v': '5.74'
        }

        group_json = requests.get('https://api.vk.com/method/groups.getMembers?', group_params)
        time.sleep(3)
        group_dict = group_json.json()['response']
        group_users = set(group_dict['items'])

        if group_users & friends_set:
            print('Совпадения есть, пролетаем мимо')
        else:
            print('Совпадений нет, группа нам подходит')
            groups.append(group)

    return groups


def search_groups(user_id):
    print('Получаем список друзей')
    friends_set = get_friends(user_id)
    print('Список друзей получен')
    print('Получаем список групп')
    group_set = get_groups(user_id)
    print('Список групп получен')
    group_user_set = search_group_user(group_set, friends_set)
    print('Результат получен')
    print(group_user_set)


search_groups(user)
