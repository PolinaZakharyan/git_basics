from argparse import ArgumentParser
from user_functions import edit_user, save_user, get_all_users, get_user_by_id, delete_user


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
elif int(args.operation) == 5:
    KEYS = 'first_name', 'last_name', 'email',
    edit_user(int(args.identifier),
        {k: v for k, v in vars(args).items() if (v is not None) and k in KEYS})
