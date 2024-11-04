from collections import Counter


def get_mediana(values_list):
    quotient, remainder = divmod(len(values_list), 2)
    return int(values_list[quotient] if remainder else sum(values_list[quotient - 1:quotient + 1]) / 2)


def get_average(values_list):
    return int((sum(values_list)) / len(values_list))


def check_current_state(median_value, average_value):
    load_pattern = (average_value - median_value) / average_value * 100
    if load_pattern < -25:
        current_state = "происходят снижения"
    elif load_pattern > 25:
        current_state = "происходят скачки"
    else:
        current_state = "нагрузка стабильна"
    print(f'Среднее значение: {average_value}, медианное зачение: {median_value}, {current_state}')


def get_frequencies_of_values(values_list):
    rps_counter = Counter(values_list)
    print(f'Частоты вхождения:')
    for rps, rps_frequency in rps_counter.items():
        print(rps, rps_frequency, sep=':', end='; ')
    # делаю пустой перенос, чтобы было разделение между выводом частот и строкой-пояснением для ввода новых данных
    print()


def proccess_new_value(rps_values, new_values):
    is_wait_new_value = True

    if new_values.isdigit():
        rps_values.append(new_values)
    elif ';' in new_values:
        rps_values.extend(new_values.split(';'))
    elif new_values == '':
        is_wait_new_value = False
    elif new_values[0] == '[' and new_values[-1] == ']':
        begin, end = new_values.strip('[]').split(',')
        # от левой границы среза отнимаем 1, т.к. строка начинается с индекса 0.
        rps_values = rps_values[int(begin) - 1:int(end)]
        is_wait_new_value = False
    return rps_values, is_wait_new_value


def main():
    rps_values = (
    5081, '17184', 10968, 9666, '9102', 12321, '10617', 11633, 5035, 9554, '10424', 9378, '8577', '11602', 14116,
    '8066', '11977', '8572', 9685, 11062, '10561', '17820', 16637, 5890, 17180, '17511', '13203', 13303, '7330', 7186,
    '10213', '8063', '12283', 15564, 17664, '8996', '12179', '13657', 15817, '16187', '6381', 8409, '5177', 17357,
    '10814', 6679, 12241, '6556', 12913, 16454, '17589', 5292, '13639', '7335', '11531', '14346', 7493, 15850, '12791',
    11288)
    rps_values = list(rps_values)

    while True:
        print('Введите дополнительные данные в формате: value либо value1;value2;...valueN либо [value1,valueN].')
        print('После ввода пустой строки либо [value1,valueN] программы будет завершена.')

        new_values = input()
        rps_values, is_wait_new_value = proccess_new_value(rps_values, new_values)

        sorted_rps_values = sorted(map(int, rps_values))
        
        mediana = get_mediana(sorted_rps_values)
        average = get_average(sorted_rps_values)
        check_current_state(mediana, average)

        get_frequencies_of_values(sorted_rps_values)

        if not is_wait_new_value:
            break


if __name__ == '__main__':
    main()
