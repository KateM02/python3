import yaml
import json
from tqdm import tqdm
from valid import validator
import random
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('path_in', help='Путь до файла с исходными данными')
parser.add_argument('path_out', help='Путь до файла в который будут выведены валижные записи')
parser.add_argument('path_fin', help='Путь до файла в который будут сохранены отсортированные записи')
args = parser.parse_args()


def shell(dicts, field):
    inc = len(dicts) // 2
    while inc:
        for i, el in enumerate(dicts):
            while i >= inc and dicts[i - inc][field] > el[field]:
                dicts[i] = dicts[i - inc]
                i -= inc
            dicts[i] = el
        if inc == 2:
            inc = 1
        else:
            inc = int(inc//2)


def val(path_in, path_out) -> None:
    data = json.load(open(path_in, encoding='windows-1251'))

    true_data = list()
    email = 0
    height = 0
    inn = 0
    passport_number = 0
    university = 0
    age = 0
    political_views = 0
    worldview = 0
    address = 0

    with tqdm(total=len(data)) as progressbar:
        for person in data:
            temp = True
            if not validator.check_email(person['email']):
                email += 1
                temp = False
            if not validator.check_height(person['height']):
                height += 1
                temp = False
            if not validator.check_inn(person['inn']):
                inn += 1
                temp = False
            if not validator.check_passport_number(person['passport_number']):
                passport_number += 1
                temp = False
            if not validator.check_university(person["university"]):
                university += 1
                temp = False
            if not validator.check_age(person['age']):
                age += 1
                temp = False
            if not validator.check_political_views(person['political_views']):
                political_views += 1
                temp = False
            if not validator.check_worldview(person['worldview']):
                worldview += 1
                temp = False
            if not validator.check_address(person["address"]):
                address += 1
                temp = False
            if temp:
                true_data.append(person)
            progressbar.update(1)

    out_put = open(path_out, 'w', encoding='utf-8')
    beauty_data = json.dumps(true_data, ensure_ascii=False, indent=4)
    out_put.write(beauty_data)
    out_put.close()

    print(f'Число валидных записей: {len(true_data)}')
    print(f'Число невалидных записей: {len(data) - len(true_data)}')
    print(f'   Число невалидных адрессов почты:  {email}')
    print(f'   Число невалидных ростовых замеров: {height}')
    print(f'   Число невалидных ИНН: {inn}')
    print(f'   Число невалидных номеров паспорта: {passport_number}')
    print(f'   Число невалидных университетов: {university}')
    print(f'   Число невалидных возрастов:  {age}')
    print(f'   Число невалидных политических взглядов: {political_views}')
    print(f'   Число невалидных мировоззрений: {worldview}')
    print(f'   Число невалидных адрессов: {address}')
    pass


def sort_shell(path_out, path_fin):
    sort_data = json.load(open(path_out, encoding='UTF-8'))
    print("По какому полю сортировать записи?\n1.\'passport_number\'\n2.\'age\'\n")
    choice1 = int(input())
    if choice1 == 1:
        shell(sort_data, 'passport_number')
    elif choice1 == 2:
        shell(sort_data, 'age')
    with open(path_fin, 'w') as fin:
        fin_data = yaml.dump(sort_data)
        # print(fin_data)
        fin.write(fin_data)
    print("Сортировка завершена\n")


def print_data(path_fin) -> None:
    with open(path_fin, 'r') as t_put:
        test = yaml.safe_load(t_put)
        for i in range(7):
            print(test[random.randint(i*10000, (i+1)*10000)])


print("\nВыберите операцию:\n1. Проверить валидность исходных записей.\n2. Отсортирвать валидные записи.\n3. Вывести сортиванные записи на экран.\n4. Завершить.")
while True:
    choice = int(input())
    if choice == 1:
        val(args.path_in, args.path_out)
    elif choice == 2:
        sort_shell(args.path_out, args.path_fin)
    elif choice == 3:
        print_data(args.path_fin)
    elif choice == 4:
        break
