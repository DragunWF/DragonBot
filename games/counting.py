import csv
import random
from string import digits
from discord.ext import commands

data_location = "data/counting.csv"


def create_counting_id(guild_id, channel_id):
    with open(data_location, "r") as data:
        reader = list(csv.reader(data))
        for row in reader:
            if row[0] == guild_id:
                return "You already have a counting channel setup!"

        with open(data_location, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([guild_id, channel_id, "user", "none", 0])
        return "Counting channel setup is complete!"


def trigger_event(previous_number):
    random_number_1, random_number_2, random_number_3 = random.randint(
        2, 8), random.randint(2, 6), random.randint(1, 4)
    p, x, y, z = previous_number, random_number_1, random_number_2, random_number_3
    events = {"multiplication": (p * x, f"p * {x}"),
              "addition": (p + x, f"p + {x}"),
              "algebra_1": (p - x + y, f"p - {x} + {y}"),
              "algebra_2": ((p + x) * y, f"(p + {x}) * {y}"),
              "algebra_3": ((p + x) * (y - z), f"(p + {x}) * ({y} - {z})")}
    event = random.choice([x for x in events])
    return events[event]


def check_event():
    event_chance = random.randint(1, 10)
    return False if event_chance != 1 else True


def main_counting(guild_id, channel_id, user_id, number):
    global previous_user
    # Fix bug tomorrow, problem here is that fact that the event
    # trigger is happening before the event info is announced
    # I could try adding an extra item to the data_set in the csv file
    # that displays what type of event is occuring

    for chr in number:
        if not chr in digits and not chr in ("+", "-", "*", "/"):
            return
    number = eval(number.strip())

    with open(data_location, "r") as data:
        reader = list(csv.reader(data))
        reader = list(
            map(lambda x: [int(x[0]), int(x[1]), x[2], x[3], int(x[4])], reader))
        for row in reader:
            if row[0] == guild_id and row[1] == channel_id:
                index = reader.index(row)
                break
        else:
            return

        statement, outputs, equation = "", [], None
        print(reader[index][3])
        if reader[index][3] != "event":
            correct_number = reader[index][4] + 1
        else:
            event_getter = trigger_event(reader[index][4])
            correct_number = event_getter[0]
            equation = event_getter[1]
            reader[index][3] = "none"

        def reset_counting():
            reader[index][4] = 0
            reader[index][3] = "none"
            reader[index][2] = "user"

        if number == correct_number and user_id != reader[index][2]:
            reader[index][4] = correct_number
            reader[index][2] = user_id
        elif user_id == reader[index][2]:
            statement = f"WRONG, <@{user_id}> ruined it. The same person can't count twice! Next number is **1**."
            reset_counting()
        else:
            statement = f"WRONG, <@{user_id}> ruined it at **{reader[index][4]}**. The correct number was **{correct_number}**, nerd! Next number is **1**."
            reset_counting()

        with open(data_location, "w", newline="") as file:
            writer = csv.writer(file)
            for row in reader:
                writer.writerow(row)

        outputs.append(statement if statement else True)
        if check_event() and not statement:
            reader[index][3] = "event"
            outputs.append(f"**Event alert!**")
            outputs.append(f"""```
Next number is the result of the following equation (p = {reader[index][4] - 1}):
{equation}
```
""")

        return outputs
