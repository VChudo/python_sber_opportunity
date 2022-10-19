import json
from datetime import datetime, timedelta


def count_category(cat: str) -> dict:
    res = {}
    for i in df['transactions']:
        res[df['transactions'][i][cat]] = res.get(df['transactions'][i][cat], 0) + 1
    return res


def count_multi_pass(more_then: int = 8) -> dict:
    res, temp = {}, []
    for i in df['transactions']:
        if df['transactions'][i]['card'] not in temp:
            temp.append(df['transactions'][i]['card'])
            res[df['transactions'][i]['passport']] = res.get(df['transactions'][i]['passport'], 0) + 1
    return {i: res[i] for i in res if res[i] > more_then}


def count_city(more_then: int = 1) -> dict:
    res, temp = {}, []
    for i in df['transactions']:
        if df['transactions'][i]['card'] not in temp:
            temp.append(df['transactions'][i]['card'])
            res[df['transactions'][i]['address']] = res.get(df['transactions'][i]['address'], 0) + 1
    return {i: res[i] for i in res if res[i] > more_then}


def count_for_lenght(cat: str):
    res = {}
    for i in df['transactions']:
        res[(df['transactions'][i][cat])] = res.get((df['transactions'][i][cat]), 0) + 1
    return res


def out_info(category: str) -> list:
    res = []
    for i in df['transactions']:
        if category in df['transactions'][i].values():
            res.append(df['transactions'][i])
    return res


def get_transaction(category: str, list_value: list | dict, full_view=False) -> list:
    res = []
    for i in df['transactions']:
        if df['transactions'][i][category] in list_value or df['transactions'][i][category] == list_value:
            res.append(i)
    return res


def get_value_transaction(category: str, list_value: list | dict | str) -> list:
    res = []
    if type(list_value) in (list, dict):
        for i in list_value:
            for j in df['transactions']:
                if df['transactions'][j][category] == i:
                    res.append(df['transactions'][j])
    else:
        for j in df['transactions']:
            if df['transactions'][j][category] == list_value:
                res.append(df['transactions'][j])
    return res


def get_short_time_city_change(values: list):
    res, first = [], values[0]
    for i in values[1:]:  # values need be sorted?
        if first['card'] == i['card'] and first['city'] != i['city'] \
                and datetime.strptime(i['date'], '%Y-%m-%dT%H:%M:%S') - datetime.strptime(first['date'],
                                                                                          '%Y-%m-%dT%H:%M:%S') < timedelta(
            minutes=60):
            res.append(first)
            res.append(i)
        first = i
    return res


def get_value_of_transaction(category: str, list_value: list | dict, full_view=False) -> list:
    res = []
    for i in df['transactions']:
        if df['transactions'][i][category] in list_value:
            res.append(i)
    return res


def get_value_of_transaction_dict(list_value: dict) -> list:
    res = []
    for i in df['transactions']:
        if df['transactions'][i] in list_value:
            res.append(i)
    return res


def get_lot_of_wrong():
    list_of_cards = count_category("card")
    list_of_cards = [i for i in list_of_cards if list_of_cards[i] > 2]
    res = []
    for i in list_of_cards:
        count, city = 0, ''
        for j in get_value_of_transaction('card', i):
            if df['transactions'][j]['oper_result'] == 'Отказ':
                count += 1
                city = df['transactions'][j]['city']
        if count > 2:
            for j in get_value_of_transaction('card', i):
                if df['transactions'][j]['city'] == city:
                    res.append(j)
    return res


with open('transactions.json') as file:
    df = json.load(file)

# паттерн много отказов
print('паттерн много отказов')
print(get_lot_of_wrong())

# паттерн разные города в коротком промежутке времени
list_of_cards = count_category("card")
list_of_cards = [i for i in list_of_cards if list_of_cards[i] > 1]
print('паттерн разные города в коротком промежутке времени')
print(get_value_of_transaction_dict(get_short_time_city_change(get_value_transaction('card', list_of_cards))))

# multiaccaunt
print('multiaccaunt')
print(get_value_of_transaction('passport', count_multi_pass()))

