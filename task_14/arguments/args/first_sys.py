import sys

args = sys.argv

if args[2] == "+":
    print(int(args[1]) + int(args[3]))
elif args[2] == "-":
    print(int(args[1]) - int(args[3]))
