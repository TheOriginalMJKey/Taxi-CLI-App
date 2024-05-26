import pandas as pd


@bot.message_handler(content_types=["text"])
def print_account_data(message, user, data):

    fdata = data[data["account"] == user]
    bot.send_message(
        message.chat.id,
        fdata.to_string(columns=["from", "to", "time"], index=False),
        parse_mode="HTML",
        reply_markup=types.ReplyKeyboardRemove(),
    )


def validate_time(time_str):
    try:
        hh, mm, ss = time_str.split(":")
        if 0 <= int(hh) <= 23 and 0 <= int(mm) <= 59 and 0 <= int(ss) <= 59:
            return True
        else:
            return False
    except:
        return False


@bot.message_handler(content_types=["text"])
def add_new_ride(message, user, data):

    args = message.text.split()

    if args[0].lower() == args[1].lower():
        bot.send_message(
            message.chat.id,
            "The path is specified incorrectly",
            parse_mode="HTML",
            reply_markup=types.ReplyKeyboardRemove(),
        )

    if not validate_time(args[2]):
        bot.send_message(
            message.chat.id,
            "The time is specified incorrectly",
            parse_mode="HTML",
            reply_markup=types.ReplyKeyboardRemove(),
        )

    new_ride = pd.DataFrame(
        {
            "account": [user],
            "from": [args[0]],
            "to": [args[1]],
            "time": [args[2]],
        }
    )

    new_data = pd.concat([data, new_ride], ignore_index=True)
    new_data.to_csv("data.csv", index=False)


@bot.message_handler(content_types=["text"])
def foo(message, user):

    args = message.text.split()
    data = pd.read_csv("data.csv")

    if args[0] == "history":
        print_account_data(message, user, data)

    if args[1] == "new":
        add_new_ride(message, user, data)
