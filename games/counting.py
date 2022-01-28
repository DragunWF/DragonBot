import csv
import random
from discord.ext import commands

data_location = "data/counting.csv"


def create_counting_id(guild_id, channel_name):
    with open(data_location, "a", newline="") as file:
        file.write([guild_id, channel_name, 0])
    return "Setup is complete!"


def main_counting(guild_id, channel_name):
    with open(data_location, "r") as data:
        reader = csv.reader(data)
        for row in data:
            if row[0] == guild_id:
                pass
                break
        else:
            return create_counting_id(guild_id, channel_name)
