import json
import sys
from field import field
from gen_random import gen_random
from unique import Unique
from print_result import print_result
from cm_timer import timer_1
import os

path = None
if len(sys.argv) > 1:
    path = sys.argv[1]
else:
    path = 'data_light.json'

if not os.path.exists(path):
    test_data = [
        {"job-name": "Программист Python", "salary": 180000, "city": "Москва"},
        {"job-name": "DevOps инженер", "salary": 160000, "city": "Санкт-Петербург"},
        {"job-name": "программист C++", "salary": 140000, "city": "Новосибирск"},
        {"job-name": "Бэкенд разработчик", "salary": 150000, "city": "Екатеринбург"},
        {"job-name": "Тестировщик ПО", "salary": 100000, "city": "Москва"},
        {"job-name": "Программист Java", "salary": 190000, "city": "Казань"},
        {"job-name": "программист python", "salary": 200000, "city": "Москва"}
    ]
    with open('data_light.json', 'w', encoding='utf-8') as f:
        json.dump(test_data, f, ensure_ascii=False, indent=2)
    path = 'data_light.json'

with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

@print_result
def f1(arg):
    return sorted(Unique(field(arg, 'job-name'), ignore_case=True), key=str.lower)

@print_result
def f2(arg):
    return list(filter(lambda x: x.lower().startswith('программист'), arg))

@print_result
def f3(arg):
    return list(map(lambda x: f"{x} с опытом Python", arg))

@print_result
def f4(arg):
    salaries = list(gen_random(len(arg), 100000, 200000))
    return [f"{job}, зарплата {salary} руб." for job, salary in zip(arg, salaries)]

if __name__ == '__main__':
    with timer_1():
        f4(f3(f2(f1(data))))
