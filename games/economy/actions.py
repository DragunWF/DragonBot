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
>>> List of Jobs:
- Farmer
- Miner
- Engineer
"""


def register(player):
    with open(data_location, "a") as file:
        writer = csv.writer(file)
        writer.writerow([player, 0, 0, "none", []])
        file.write("\n")
    return "You have been registered"


def work():
    pass


def scavenge(player_data):
    locations = ("caves", "trash cans", "bushes",
                 "Tom's bag", "Tom's destroyed linux machine", "Warcook's house",
                 "CPT's cave", "shoes", "DJDAN's pillows")
    gold_gained = random.randint(5, 50)
    with open(data_location, "r") as data:
        data_sets = [x for x in list(csv.reader(data)) if x]
        data_sets = list(map(lambda arr: [int(arr[0]), int(
            arr[1]), int(arr[2]), arr[3], arr[4]], data_sets))
        index = data_sets.index(player_data)
        data_sets[index][2] += gold_gained
        with open(data_location, "w") as file:
            writer = csv.writer(file)
            for row in data_sets:
                writer.writerow(row)
    return f"You have scavenged **{gold_gained} gold** from {random.choice(locations)}!"


def action(command, player_id, option=None):
    registered = False
    with open(data_location, "r") as file:
        data = [x for x in list(csv.reader(file)) if x]
        for data_set in data:
            if player_id == int(data_set[0]):
                registered = True
                break

    if command == "help":
        return list_of_commands

    if command == "register":
        if not registered:
            return register(player_id)
        else:
            return "You are already registered"

    if registered:  # The problem here being the fact that the player id turned into a list
        player_data = None
        with open(data_location, "r") as file:
            reader = list(csv.reader(file))
            for data in reader:
                if player_id == int(data[0]):
                    player_data = data
                    player_data = [int(player_data[0]), int(player_data[1]),
                                   int(player_data[2]), player_data[3], player_data[4]]
                    break

        if command == "scavenge":
            return scavenge(player_data)

        if command == "gold":
            return f"You have **{player_data[2]} gold**."

        if command == "work":
            pass

        if command == "jobs":
            return list_of_jobs

        if command == "shop":
            pass
    else:
        return "You are not registered, Type `d!economy register` to register."
