import random
import csv

data_location = "data/economy_data.csv"

list_of_commands = """
**List of commands:**
- Register
- Gold
- Scavenge
"""

list_of_jobs = """
List of Jobs:
- Farmer
- Miner
- Engineer
"""


def work():
    pass


def register(player):
    with open(data_location, "r") as file:
        reader = list(csv.reader(file))
        for data in reader:
            if player == data[0]:
                return "You're already registered in the kingdom!"

    with open(data_location, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([player, 0, 0, "none", []])
    return "You have been registered"


def action(command, player_id):
    registered = False
    with open(data_location, "r") as file:
        data = list(csv.reader(file))
        for player_id in data:
            if player_id == data[0]:
                registered = True

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
            print(reader)
            for data in reader:
                print(data)
                print(f"{data[0]} : {player_id} ? {data[0] == player_id}")
                if player_id == int(data[0]):
                    print('passed')
                    player_data = data
                    player_data[1], player_data[2] = int(data[1]), int(data[2])
                    break

        if command == "scavange":
            locations = ("caves", "trash cans", "bushes",
                         "Tom's bag", "Tom's destroyed linux machine", "Warcook's house")
            gold_gained = random.randint(5, 50)
            with open(data_location, "r") as data:
                data_sets = list(csv.reader(data))
                index = data_sets.index(player_data)
                data_sets[index][2] += gold_gained
                with open(data_location, "w") as file:
                    writer = csv.writer(file)
                    for row in list(csv.reader(data_sets)):
                        writer.writerow(row)
            return f"You have scavenged {gold_gained} gold from {random.choice(locations)}!"

        if command == "gold":
            return f"You have {player_data[2]} gold."

        if command == "work":
            pass

        if command == "jobs":
            return list_of_jobs

        if command == "shop":
            pass
    else:
        return "You are not registered, Type `d!economy register` to register."
