import argparse

import pandas as pd

# python3 s.py sasha --new msk spb 10:00:00
# python3 s.py sasha --history


def parse_arguments():

    parser = argparse.ArgumentParser(add_help=False)

    parser.add_argument("account", type=str)
    parser.add_argument("--history", action="store_true")
    parser.add_argument("--new", nargs=3, type=str)

    return parser.parse_args()


def print_account_data(args, data):

    fdata = data[data["account"] == args.account]
    print(fdata.to_string(columns=["from", "to", "time"], index=False))


def validate_time(time_str):
    try:
        hh, mm, ss = time_str.split(":")
        if 0 <= int(hh) <= 23 and 0 <= int(mm) <= 59 and 0 <= int(ss) <= 59:
            return True
        else:
            return False
    except:
        return False


def add_new_ride(args, data):

    if args.new[0].lower() == args.new[1].lower():
        print("The path is specified incorrectly")

    if not validate_time(args.new[2]):
        print("The time is specified incorrectly")

    new_ride = pd.DataFrame(
        {
            "account": [args.account],
            "from": [args.new[0]],
            "to": [args.new[1]],
            "time": [args.new[2]],
        }
    )

    new_data = pd.concat([data, new_ride], ignore_index=True)
    new_data.to_csv("data.csv", index=False)


if __name__ == "__main__":

    args = parse_arguments()
    data = pd.read_csv("data.csv")

    if args.history:
        print_account_data(args, data)

    if args.new:
        if not (input("Do you want to cancel the trip ? ").lower() == "yes"):
            add_new_ride(args, data)
