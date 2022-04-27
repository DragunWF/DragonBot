import csv
import random
from string import digits
from .economy.rewards import game_reward

data_location = "data/counting.csv"


def create_counting_id(guild_id, channel_id):
    with open(data_location, "r") as data:
        reader = list(csv.reader(data))
        for row in reader:
            if row[0] == guild_id:
                return "You already have a counting channel setup!"

        with open(data_location, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([guild_id, channel_id, 123, "none", 0, 0])
        return "Counting channel setup is complete!"


def trigger_event(previous_number, event_type):
    random_number_1, random_number_2, random_number_3 = random.randint(
        2, 8), random.randint(2, 6), random.randint(1, 4)
    p, x, y, z = previous_number, random_number_1, random_number_2, random_number_3
    events = {"multiplication": (p * x, f"p * {x}"),
              "addition": (p + x, f"p + {x}"),
              "algebra_1": (p - x + y, f"p - {x} + {y}"),
              "algebra_2": ((p + x) * y, f"(p + {x}) * {y}"),
              "algebra_3": ((p + x) * (y - z), f"(p + {x}) * ({y} - {z})"),
              "algebra_4": ((p + x - y) * z, f"(p + {x} - {y}) * {z}")}
    # event = random.choice([x for x in events])
    return events[event_type]


def check_event():
    event_chance = random.randint(1, 10)
    return False if event_chance != 1 else True


def main_counting(guild_id, channel_id, user_id, number):
    for chr in number:
        if not chr in digits and not chr in ("+", "-", "*", "/"):
            return
    number = eval(number.strip())

    with open(data_location, "r") as data:
        reader = list(csv.reader(data))
        reader = list(map(lambda x: [int(x[0]), int(x[1]), int(x[2]), x[3], int(x[4]), int(x[5])],
                          reader))
        for row in reader:
            if row[0] == guild_id and row[1] == channel_id:
                index = reader.index(row)
                break
        else:
            return

        statement, outputs = "", []
        event_occuring, equation_solved = False, False
        if reader[index][3] == "none":
            correct_number = reader[index][4] + 1
        else:
            correct_number = reader[index][5]
            reader[index][3] = "none"
            event_occuring = True

        def reset_counting():
            reader[index][4] = 0
            reader[index][3] = "none"
            reader[index][2] = 123

        if number == correct_number and user_id != reader[index][2]:
            reader[index][4] = correct_number
            reader[index][2] = user_id
            if event_occuring:
                equation_solved = True
        elif user_id == reader[index][2]:
            statement = f"WRONG, <@{user_id}> ruined it. The same person can't count twice! Next number is **1**."
            reset_counting()
        else:
            statement = f"WRONG, <@{user_id}> ruined it at **{reader[index][4]}**. The correct number was **{correct_number}**, nerd! Next number is **1**."
            reset_counting()

        outputs.append(statement if statement else True)

        if not statement and equation_solved:
            outputs.append(game_reward(user_id, "counting"))

        if check_event() and not statement:
            events = ("multiplication", "addition",
                      "algebra_1", "algebra_2", "algebra_3", "algebra_4")
            reader[index][3] = random.choice(events)
            event_getter = trigger_event(reader[index][4], reader[index][3])
            equation = event_getter[1]
            reader[index][5] = event_getter[0]

            outputs.append(f"**Event alert!**")
            outputs.append(
                f"Next number is the result of the following equation `(p = {reader[index][4]})`:")
            outputs.append(f"```{equation}```")

        with open(data_location, "w", newline="") as file:
            writer = csv.writer(file)
            for row in reader:
                writer.writerow(row)

        return outputs
