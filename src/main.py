import json
import datetime as dt


def open_json_file(file_path):
    """открываем файл и преобразуем его в список"""
    with open(file_path) as file:
        return json.load(file)


def filter_vacancies(operations_data):
    """Функция фильтрации по статусу выполненных операций"""
    file_list = []
    for operation in operations_data:
        if operation['state'] == 'EXECUTED':
            file_list.append(operation)
            continue
        return file_list


def sort_operations(operations_data: list[dict]) -> list[dict]:
    """Функция сортировки операций по дате"""
    sorted_list = sorted(operations_data, key=lambda x: x['date'], reverse=True)
    return sorted_list


def mask_operation_from(operation_from):
    """Функция маскировки номера отправителя"""
    operation_ = operation_from.get('from')
    if operation_:
        parts = operation_.split(' ')
        numbers = parts[-1]
        # если длина номера равна 16, то маскируем
        if len(numbers) == 16:
            masked_numbers = f"{numbers[:4]} {numbers[4:6]}** **** {numbers[-4:]} ->"
            return f"{(' '.join(parts[:-1]))} {masked_numbers}"
        # если длина номера равна 20, то маскируем
        if len(numbers) == 20:
            masked_numbers = f"**{numbers[-4:]} ->"
            return f"{(' '.join(parts[:-1]))} {masked_numbers}"
        # если длина номера не равна 16 и не равна 20, то не маскируем
    return "Без номера ->"


def mask_operation_to(operation_to):
    """Функция маскировки номера получателя"""
    operation_ = operation_to.get('to')
    if operation_:
        parts = operation_.split(' ')
        numbers = parts[-1]
        if len(numbers) == 16:
            masked_numbers = f"{numbers[:4]} {numbers[4:6]}** **** {numbers[-4:]}"
            return f"{(' '.join(parts[:-1]))} {masked_numbers}"
        if len(numbers) == 20:
            masked_numbers = f"**{numbers[-4:]}"
            return f"{(' '.join(parts[:-1]))} {masked_numbers}"
    return f"Без номера"


def money_count(money):
    """функция количества денег в операциях и какой курс"""
    for operation in money:
        # считаем количество денег в операции и выводим курс
        amount = operation['operationAmount']['amount']
        rub_usd = operation['operationAmount']['currency']['name']
        return f"{amount} {rub_usd}"


def descrtiption(descr):
    """Функция форматирования описания операции"""
    if isinstance(descr, dict) and 'description' in descr:
        # описание операции
        name_description = descr['description']
        return name_description


def format_date(operation):
    """Функция форматирования даты операции"""
    date: str = operation['date']
    dt_time = dt.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%f")
    return dt_time.strftime("%d.%m.%Y")


# передаем параметры в функции
data = open_json_file('data/operations.json')
operations = filter_vacancies(data)
operations = sort_operations(operations)

# выводим первые 5 операций
for i in operations[:5]:
    print(f"{format_date(i)} {descrtiption(i)}")
    print(f"{mask_operation_from(i)} {mask_operation_to(i)}")
    print(f"{money_count([i])}\n")
