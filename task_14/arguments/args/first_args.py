import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-fn", "--first-number")
parser.add_argument("-sn", "--second-number")
parser.add_argument("-o", "--operator")

args = parser.parse_args()
if args.operator == "+":
    print(int(args.first_number) + int(args.second_number))
elif args.operator == "-":
    print(int(args.first_number) - int(args.second_number))
elif args.operator == "*":
    print(int(args.first_number) * int(args.second_number))
elif args.operator == "/":
    print(int(args.first_number) / int(args.second_number))