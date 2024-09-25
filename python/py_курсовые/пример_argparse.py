import argparse


def multiply(a, b):
    return a*b


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', nargs='+', required=True, help='Required: one or more number.')
    parser.add_argument('-r', '--ratio', nargs=1, required=True, help='Required: ratio.')
    parser.add_argument('-v', action="count", help='Verbose level in range 0..+inf')

    args = parser.parse_args()

    numbers = map(int, args.input)
    ratio = int(args.ratio[0])
    verbose = (args.v if isinstance(args.v, int) else 0)
    verbose_out = ''
    multiply_out = ''

    if verbose >= 1:
        print(f'Коэффициент: {ratio}')
    for number in numbers:
        if verbose > 1:
            verbose_out += f'{number} * {ratio} = {multiply(number, ratio)}\n'
        multiply_out += f'{multiply(number, ratio)} '

    if verbose_out != '':
        print(verbose_out, end='')
    print(multiply_out)

if __name__ == '__main__':
    main()