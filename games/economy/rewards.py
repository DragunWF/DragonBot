import random
import csv

data_location = "data/economy_data.csv"


def game_reward(player_id, game):
    with open(data_location, "r") as file:
        reader = [x for x in list(csv.reader(file)) if x]
        reader = list(map(lambda arr: [int(arr[0]), int(
            arr[1]), int(arr[2]), arr[3], arr[4]], reader))
        for data_set in reader:
            if player_id == data_set[0]:
                index = reader.index(data_set)
                break
        else:
            return False

        reward_lvls = {"guess": (50, 150), "rockpaperscissors": (350, 500),
                       "fight": (250, 350), "tictactoe": (400, 450)}
        min_num, max_num = reward_lvls[game][0], reward_lvls[game][1]
        gold_reward = random.randint(min_num, max_num)
        reader[index][2] += gold_reward
        with open(data_location, "w") as data:
            writer = csv.writer(data)
            for row in reader:
                writer.writerow(row)
        return f"Congrats, You have earned **{gold_reward} gold** from this mini-game!"