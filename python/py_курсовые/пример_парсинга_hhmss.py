data = ['1h32m14s', '32m14s', '14s', '120h3s', '13m', '10h']

for value in data:
    if value.find('-') != -1:
        raise ValueError('Period must be positive value')
    hours = '0'
    minutes = '0'
    seconds = '0'

    position_h = value.find('h')
    if position_h != -1:
        hours = value[:position_h]

    position_m = value.find('m')
    if position_m != -1:
        minutes = value[position_h + 1:position_m]

    position_s = value.find('s')
    if position_s != -1:
        if position_m != -1:
            seconds = value[position_m + 1:position_s]
        else:
            seconds = value[position_h + 1:position_s]
    print(f'{value}: {hours}h, {minutes}m, {seconds}s')

    sum_seconds = int(hours) * 3600 + int(minutes) * 60 + int(seconds)
    print(f'seconds: {sum_seconds}')