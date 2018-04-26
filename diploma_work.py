import requests
import time
import json


user = 5030613
TOKEN = '7b23e40ad10e08d3b7a8ec0956f2c57910c455e886b480b7d9fb59859870658c4a0b8fdc4dd494db19099'


def get_friends(user_id):
    print('Получаем список друзей')

    friends_params = {
        'user_id': user_id,
        'order': 'name',
        'access_token': TOKEN,
        'v': '5.74'
    }

    friends_json = requests.get('https://api.vk.com/method/friends.get?', friends_params)

    try:
        friends_dict = friends_json.json()['response']
        return set(friends_dict['items'])
    except KeyError:
        error = friends_json.json()['error']
        print('Ошибка № {0} {1}'.format(error['error_code'], error['error_msg']))
        get_friends(user_id)


def get_groups(user_id):
    print('Получаем список групп')

    group_params = {
        'user_id': user_id,
        'count': '1000',
        'access_token': TOKEN,
        'v': '5.74'
    }

    group_json = requests.get('https://api.vk.com/method/groups.get?', group_params)

    try:
        group_dict = group_json.json()['response']
        return set(group_dict['items'])
    except KeyError:
        error = group_json.json()['error']
        print('Ошибка № {0} {1}'.format(error['error_code'], error['error_msg']))
        get_groups(user_id)


def get_friends_groups(friends_set, group_set):
    print('Ищем совпадения')

    for friend in friends_set:
        time.sleep(1)
        print('Проверяем https://vk.com/id{}'.format(friend))
        friend_params = {
            'user_id': friend,
            'count': '1000',
            'access_token': TOKEN,
            'v': '5.74'
        }

        group_json = requests.get('https://api.vk.com/method/groups.get?', friend_params)

        try:
            group_dict = group_json.json()['response']
            group_users = set(group_dict['items'])
            group_set = group_set - group_users
        except KeyError:
            error = group_json.json()['error']
            print('Ошибка № {0} {1}'.format(error['error_code'], error['error_msg']))

    return group_set


def json_group(group_user_set):
    print('Формируем json-файл')

    group_list = []

    for group in group_user_set:
        time.sleep(1)
        params = {
            'group_id': group,
            'fields': 'members_count',
            'access_token': TOKEN,
            'v': '5.74'
        }

        group_json = requests.get('https://api.vk.com/method/groups.getById?', params)
        group_dict = group_json.json()['response']

        print('Собираем информацию о группе', group_dict[0]['name'])

        group_list.append({
            'name': group_dict[0]['name'],
            'gid': group_dict[0]['id'],
            'members_count': group_dict[0]['members_count']
        })

    with open('groups.json', 'w', encoding='utf8') as f:
        json.dump(group_list, f, ensure_ascii=False, indent=2)

    print('Файл groups.json сформирован и заполнен')


def search_groups(user_id):
    friends_set = get_friends(user_id)
    print('Список друзей получен')
    print(len(friends_set), 'человек')
    group_set = get_groups(user_id)
    print('Список групп получен')
    print(len(group_set), 'групп')
    group_user_set = get_friends_groups(friends_set, group_set)
    print('Результат получен:')
    print(len(group_user_set), 'групп')
    json_group(group_user_set)
    print('Выполнение программы завершено')


search_groups(user)
