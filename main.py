import csv

data_hesh = {}


def is_hesh(dict_data): # хеш-таблица в виде словаря, где ключ - параметры в виде строки, а значения - полученные данные
    global data_hesh
    if dict_data in data_hesh:
        return data_hesh[dict_data]
    return None


def select_sorted(sort_columns=["high"], limit=30, group_by_name=False, order='desc', filename='dump.csv'):
    fields = ['date', 'open', 'high', 'low', 'close', 'volume', 'Name']
    global data_hesh
    dict_data = str({'sort_columns': sort_columns,  # сделаем из параметров(без filename) строковый ключ для хеш-таблицы
                     'limit': limit,
                     'group_by_name': group_by_name,
                     'order': order})
    hesh = is_hesh(dict_data)  # проверим наличие ключа в хеш-таблице
    if hesh:
        list_rows = hesh  # заберем данные из хеш-таблицы
    else:  # ключ не найдем, читаем данные обычным образом

        is_reverse = True if order == 'asc' else False
        dictobj = csv.DictReader(open('all_stocks_5yr.csv'))  # чтение данных
        if len(sort_columns) == 1:  # сортировка по одному полю
            list_rows = sorted(dictobj, key=lambda d: d[sort_columns[0]], reverse=is_reverse)
        elif len(sort_columns) == 2:  # сортировка по 2 полям
            list_rows = sorted(dictobj, key=lambda d: (d[sort_columns[0]],
                                                       d[sort_columns[1]]), reverse=is_reverse)
        elif len(sort_columns) == 3:  # сортировка по 3 полям
            list_rows = sorted(dictobj, key=lambda d: (d[sort_columns[0]],
                                                       d[sort_columns[1]],
                                                       d[sort_columns[2]]), reverse=is_reverse)
        elif len(sort_columns) == 4:  # сортировка по 4 полям
            list_rows = sorted(dictobj, key=lambda d: (d[sort_columns[0]],
                                                       d[sort_columns[1]],
                                                       d[sort_columns[2]],
                                                       d[sort_columns[3]]), reverse=is_reverse)
        elif len(sort_columns) == 5:  # сортировка по 5 полям
            list_rows = sorted(dictobj, key=lambda d: (d[sort_columns[0]],
                                                       d[sort_columns[1]],
                                                       d[sort_columns[2]],
                                                       d[sort_columns[3]],
                                                       d[sort_columns[4]]), reverse=is_reverse)
        elif len(sort_columns) == 6:  # сортировка по 6 полям
            list_rows = sorted(dictobj, key=lambda d: (d[sort_columns[0]],
                                                       d[sort_columns[1]],
                                                       d[sort_columns[2]],
                                                       d[sort_columns[3]],
                                                       d[sort_columns[4]],
                                                       d[sort_columns[5]]), reverse=is_reverse)
        else:
            list_rows = sorted(dictobj, key=lambda d: d["high"], reverse=is_reverse)

        list_rows = list_rows[:limit]  # берем срез нужного количества
        dict_rows = {}  # если нужна группировка по имени
        if group_by_name:
            for each in list_rows:
                name = each["Name"]
                if name in dict_rows:
                    m_dict = dict_rows[name]
                    m_dict['date'] = min(m_dict['date'], each['date'])
                    for i in fields[1:-2]:
                        m_dict[i] = str((float(m_dict[i]) + float(each[i])) / 2)
                    m_dict['volume'] = str(int(m_dict['volume']) + int(each['volume']))
                    m_dict['Name'] = each['Name']
                    dict_rows[name] = m_dict
                else:
                    dict_rows[name] = each
            list_rows = dict_rows.values()
        data_hesh[dict_data] = list_rows  # запишем данные в хеш-таблицу

    writer = csv.DictWriter(open(filename, "w", newline=''), fieldnames=fields)  # запись данных
    writer.writeheader()
    for i in list_rows:
        writer.writerow(i)
        print(i)
    return list(list_rows)


if __name__ == '__main__':
    # пример использования
    # 1
    print('-1-')
    select_sorted(sort_columns=["high", "close"], limit=5, group_by_name=False, order='asc', filename='dump1.csv')
    # 2
    print('-2-')
    select_sorted(sort_columns=["close"], limit=5, group_by_name=True, order='asc', filename='dump2.csv')
    # 3 из кеша №1
    print('-3-')
    select_sorted(sort_columns=["high", "close"], limit=5, group_by_name=False, order='asc', filename='dump3.csv')
