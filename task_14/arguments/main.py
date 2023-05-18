from argparse import ArgumentParser
from user_functions import save_user, get_all_users, get_user_by_id, delete_user


parser = ArgumentParser()

parser.add_argument("-o", "--operation", required=True)
parser.add_argument("-f", "--first_name")
parser.add_argument("-l", "--last_name")
parser.add_argument("-e", "--email")
parser.add_argument("-id", "--identifier")

args = parser.parse_args()

if int(args.operation) == 1:
    save_user(args.first_name, args.last_name, args.email)
elif int(args.operation) == 2:
    get_all_users()
elif int(args.operation) == 3:
    get_user_by_id(int(args.identifier))
elif int(args.operation) == 4:
    delete_user(int(args.identifier))