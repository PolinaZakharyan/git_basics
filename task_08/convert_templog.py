import argparse
from array import array

ARGPARSER = argparse.ArgumentParser(
    prog='weather templog converter',
    description='convert weather temperature logs to/from binary format with data compression',
)

ARGPARSER.add_argument('input', nargs='?', type=str, help='input file')
ARGPARSER.add_argument('output', nargs='?', type=str, help='output file', default='templog.o')

ARGPARSER.add_argument('--text', '-t', action='store_true',
    help='if option specified, conversion mode is text to binary, inverse otherwise')

def to_text(input: bytearray) -> str:
    """Decode compressed templog data"""
    arr = array('f')
    arr.frombytes(input)
    return ''.join(map(lambda x: str(round(x, 2)) + '\n', arr))

def to_binary(input: str) -> bytearray:
    """Compress templog data by converting the string numbers to true floats"""
    return bytearray(array('f', map(float, input.strip().split('\n'))))


if __name__ == "__main__": # pragma: no cover
    from sys import argv
    ns = ARGPARSER.parse_args(argv[1:])

    if ns.text:
        with open(ns.input, 'r') as infile:
            with open(ns.output, 'wb') as outfile:
                outfile.write(to_binary(infile.read()))
    else:
        with open(ns.input, 'rb') as infile:
            with open(ns.output, 'w') as outfile:
                outfile.write(to_text(infile.read()))
