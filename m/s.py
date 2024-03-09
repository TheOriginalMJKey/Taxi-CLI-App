import argparse
import pandas as pd

# python3 s.py sasha --new msk spb 10:00:00
# python3 s.py sasha --history


parser = argparse.ArgumentParser(add_help=False)

parser.add_argument("account", type=str)
parser.add_argument("--history", action="store_true")
parser.add_argument("--new", nargs=3, type=str)

args = parser.parse_args()
data = pd.read_csv("data.csv")


if args.history:
    fdata = data[data["account"] == args.account]
    print(fdata.to_string(columns=["from", "to", "time"], index=False))


if args.new:
    
    t = pd.DataFrame(
        {
            "account": [args.account],
            "from": [args.new[0]],
            "to": [args.new[1]],
            "time": [args.new[2]],
        }
    )

    new_data = pd.concat([data, t], ignore_index=True)
    new_data.to_csv("data.csv", index=False)
