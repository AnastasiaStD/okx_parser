from datetime import datetime, timedelta
import random
import re

def parse_date(date_str):
    months = {
        'янв.': '01',
        'февр.': '02',
        'мар.': '03',
        'апр.': '04',
        'мая': '05',
        'июн.': '06',
        'июл.': '07',
        'ав':'08',
        'авг.': '08',
        'сент.': '09',
        'окт.': '10',
        'нояб.': '11',
        'дек.': '12'
    }
    cleaned_date_str = re.sub(r'Опубликовано\s*', '', date_str)
    cleaned_date_str = re.sub(r'г\.', '', cleaned_date_str).strip()
    l = list(cleaned_date_str.split(' '))
    l[1] = months[l[1]]
    date = '-'.join(l)
    
    return datetime.strptime(date, '%d-%m-%Y')


def generate_random_dates(start_date, end_date):
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')

    if start >= end:        
        raise ValueError("Дата начала должна быть раньше даты конца.")

    delta = (end - start).days
    random_days_1 = random.randint(0, delta)

    random_date_1 = start + timedelta(days=random_days_1)
    remaining_delta = (end - random_date_1).days
    
    if remaining_delta <= 0:
        raise ValueError("Нет доступных дат после первой случайной даты.")

    random_days_2 = random.randint(1, remaining_delta)
    random_date_2 = random_date_1 + timedelta(days=random_days_2)
    return random_date_1.strftime('%Y-%m-%d'), random_date_2.strftime('%Y-%m-%d')

def get_today_date():
    return datetime.now().strftime('%Y-%m-%d')
