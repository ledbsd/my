from collections import deque


def main():

    proxies = input()[1:-1].split(', ')
    proxy_numbers = deque([int(x.lstrip('"proxyhost').rstrip('.slurm.io"')) for x in proxies])
    request = 1

    while request <= 1000:
        current_number = proxy_numbers.popleft()
        print(f'Обращение при помощи прокси "proxyhost{current_number}.slurm.io"')
        if current_number % 3 == 0 or current_number % 8 == 0:
            continue
        print(f'Было осуществлено обращение к ресурсу при помощи прокси "proxyhost{current_number}.slurm.io"')
        proxy_numbers.append(current_number)
        request += 1
    print(f'Число оставшихся в очереди прокси: {len(proxy_numbers)}')


if __name__ == '__main__':
    main()
