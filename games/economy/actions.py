import random
import time
import csv

# It ignored the map function because of the empty lines in the csv file

data_location = "data/economy_data.csv"

list_of_commands = """
**List of commands:**
- Register
- Gold
- Scavenge
"""

list_of_jobs = """
>>> **List of Jobs:**
- Farmer
- Miner
- Engineer
"""


def register(player, username):
    # [id, level, gold, job, inventory, username]
    with open(data_location, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([player, 0, 0, "none", [], username])
    return "You have been registered"


def rich_leaderboard():
    values, output = [], ""
    with open(data_location, "r", newline="") as file:
        reader = list(csv.reader(file))
        reader = list(map(lambda arr: [int(arr[0]), int(
            arr[1]), int(arr[2]), arr[3], arr[4], arr[5]], reader))
        for data_set in reader:
            values.append((data_set[2], data_set[5]))
        values.sort(reverse=True)
        placing = 1
        for data in values:
            output += f"**{placing}:** `{data[1]}` = **{'{:,}'.format(data[0])} gold**\n"
            placing += 1
    return f"""
>>> **Richest citizens in Dragon's Economy:**
{output}"""


def scavenge(player_data):
    locations = ("caves", "trash cans", "bushes",
                 "Tom's bag", "Tom's destroyed linux machine", "Warcook's house",
                 "CPT's cave", "shoes", "DJDAN's anime pillows", "dumpsters", "CPT's Chalice")
    gold_gained = random.randint(5, 25)
    with open(data_location, "r", newline="") as data:
        data_sets = [x for x in list(csv.reader(data)) if x]
        data_sets = list(map(lambda arr: [int(arr[0]), int(
            arr[1]), int(arr[2]), arr[3], arr[4], arr[5]], data_sets))
        index = data_sets.index(player_data)
        data_sets[index][2] += gold_gained
        with open(data_location, "w", newline="") as file:
            writer = csv.writer(file)
            for row in data_sets:
                writer.writerow(row)
    return f"You scavenged **{gold_gained} gold** from {random.choice(locations)}!"


def action(command, player_id, username=None, option=None):
    registered = False
    with open(data_location, "r", newline="") as file:
        data = [x for x in list(csv.reader(file)) if x]
        for data_set in data:
            if player_id == int(data_set[0]):
                registered = True
                break

    if command == "help":
        return list_of_commands

    if command == "register":
        if not registered:
            return register(player_id, username)
        else:
            return "You are already registered"

    if registered:
        player_data = None
        with open(data_location, "r", newline="") as file:
            reader = list(csv.reader(file))
            for data in reader:
                if player_id == int(data[0]):
                    player_data = data
                    player_data = [int(player_data[0]), int(player_data[1]),
                                   int(player_data[2]), player_data[3], player_data[4], player_data[5]]
                    break

        if command == "scavenge":
            return scavenge(player_data)

        if command == "gold":
            return f"You have **{'{:,}'.format(player_data[2])} gold**."

        if command == "rich":
            return rich_leaderboard()

        if command == "work":
            pass

        if command == "jobs":
            return list_of_jobs

        if command == "shop":
            pass
    else:
        return "You are not registered, Type `d!economy register` to register."
