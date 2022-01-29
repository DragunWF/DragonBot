import csv
import random
from string import digits
from discord.ext import commands

data_location = "data/counting.csv"


def create_counting_id(guild_id, channel_id):
    with open(data_location, "r") as data:
        reader = csv.reader(data)
        for row in reader:
            if row[0] == guild_id:
                return "You already have a counting channel setup!"

        with open(data_location, "a", newline="") as file:
            file.write([guild_id, channel_id, 0])
        return "Setup is complete!"


def trigger_event(previous_number):
    events = {"multiplication": previous_number * random.randint(2, 5),
              "addition": previous_number + random.randint(3, 15),
              "algebra_1": previous_number - random.randint(2, 4) + random.randint(5, 10),
              "algebra_2": (previous_number + random.randint(2, 5)) * random.randint(2, 4)}
    event = random.choice([x for x in events])
    return events[event]


def check_event():
    event_chance = random.randint(1, 10)
    return False if event_chance != 1 else True


def main_counting(guild_id, channel_id, number):
    if not number in digits:
        return

    with open(data_location, "r") as data:
        reader = csv.reader(data)
        for row in data:
            if row[0] == guild_id and row[1] == channel_id:
                index = reader.index(row)
                break
            else:
                return

        statement = ""
        if not check_event():
            correct_number = reader[index][2] + 1
        else:
            correct_number = trigger_event(reader[index][2])

        if number == correct_number:
            pass
        else:
            wrong_number = True

        if wrong_number:
            reader[index][2] = 0
            statement = f"The correct number was **{correct_number}** nerd!."

        with open(data_location, "w", newline="") as file:
            writer = csv.writer(file)
            for row in reader:
                writer.writerow(row)

        return statement
