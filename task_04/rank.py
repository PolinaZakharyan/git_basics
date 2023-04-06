#!/usr/bin/env python3



def make_table(args, reverse):
    table = {}
    max_len = 0
    for arg in args:
        key, value = arg.split(':')
        key = key.capitalize()
        table[key] = sorted(table.get(key, []) + [value])
        if max_len < len(key):
            max_len = len(key)
    first_value = lambda k: table[k][0]
    table = {key: table[key] for key in sorted(table, key=first_value, reverse=reverse)}
    return table, max_len

def format_table(table, max_len):
    result = []
    for key, value in table.items():
        key += (max_len - len(key)) * ' '
        value = value[0] if len(value) == 1 else " ... ".join([value[0], value[-1]])
        result.append(f'{key} {value}')
    return '\n'.join(result)

INV_OPTION = '--inv'

def main(args: list):
    inv = INV_OPTION in args
    if inv:
        args.remove(INV_OPTION)
    print(format_table(*make_table(args, reverse=not inv)))

HELP = """USAGE: rank.py [--inv] [<name>:<salary>] ...

Print names and salaries as a formatted table with all the names capitalized.

--inv: sort by salaries in ascending order, otherwise in descending
If inputting the same name more than once, output a range between min and max values. Sorting of ranged values is done by min value.
"""

if __name__ == '__main__':
    from sys import argv
    if (len(argv) == 1):
        print(HELP)
    else:
        main(argv[1:])