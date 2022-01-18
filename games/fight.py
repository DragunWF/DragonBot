import discord
import random
from discord.ext import commands
from .economy.rewards import game_reward


class Fight:
    players_playing = []
    games_running = []

    def __init__(self, player1, player2, p1_name, p2_name):
        self.player1, self.player2 = player1, player2  # IDs
        self.p1_name, self.p2_name = p1_name, p2_name
        self.p1_health, self.p2_health = 100, 100
        self.p1_def_lvl, self.p2_def_lvl = 1, 1
        self.turn = ""


async def fight(ctx, player2: discord.Member):
    async def create_game():
        statements = (f"<@{ctx.author.id}> has challenged <@{player2.id}> to a fight!",
                      f"<@{player2.id}> has been challenged by <@{ctx.author.id}> to a duel!",
                      f"<@{ctx.author.id}> has decided to fight <@{player2.id}>!")
        game = Fight(ctx.author.id, player2.id, ctx.author.name, player2.name)
        Fight.players_playing.append((ctx.author.id, player2.id))
        Fight.games_running.append(game)
        first_turn = ("p1", "p2")
        game.turn = random.choice(first_turn)
        await ctx.send(random.choice(statements))
        if game.turn == "p1":
            await ctx.send(f"<@{ctx.author.id}> gets to make the first move!")
        else:
            await ctx.send(f"<@{player2.id}> gets to make the first move!")
        await ctx.send("To make a move, type `d!choice <attack or defend>`. If you ever want to flee, Type `d!flee` to attempt to run away from the fight")
    in_a_fight = False
    for pair in Fight.players_playing:
        for player in pair:
            if ctx.author.id == player or player2.id == player:
                await ctx.send("One of you is already in a fight mate, finish that one before starting a new one")
                in_a_fight = True
                break
    if not in_a_fight:
        await create_game()


async def choice(ctx, choice: str):
    async def activity_log(turn=None):
        async def check_win():
            async def delete_game():
                Fight.games_running.pop(
                    Fight.players_playing.index((game.player1, game.player2)))
                Fight.players_playing.pop(
                    Fight.players_playing.index((game.player1, game.player2)))
                reward = game_reward(ctx.author.id, "fight")
                if reward:
                    await ctx.send(reward)
            gameover = False
            players = (game.p1_health, game.p2_health)
            for player in players:
                if player <= 0:
                    gameover = True
                    if game.turn == "p1":
                        await ctx.send(f"<@{game.player1}> has won the fight!")
                        await delete_game()
                    else:
                        await ctx.send(f"<@{game.player2}> has won the fight!")
                        await delete_game()
                    break
            if not gameover:
                game.turn = "p2" if game.turn == "p1" else "p1"
        defense = game.p2_def_lvl if turn == "p1" else game.p1_def_lvl
        def_lvls = ((1, 5), (5, 10), (10, 15))
        damage_values = random.randint(5, 40)
        def_lvl = def_lvls[defense - 1]
        min_lvl, max_lvl = def_lvl[0], def_lvl[1]
        defense_values = random.randint(min_lvl, max_lvl)
        final_damage = damage_values - defense_values
        names = (f"{game.p1_name}", f"{game.p2_name}")
        attacker = names[0] if turn == "p1" else names[1]
        defender = names[1] if turn == "p1" else names[0]
        if choice.lower().strip() == "attack":
            if final_damage <= 0:
                final_damage = 0
                await ctx.send(f"{attacker} has dealt no damage to {defender}!")
            else:
                await ctx.send(f"{attacker} has attacked {defender} for **{final_damage} damage!**")
            if turn == "p1":
                game.p2_health -= final_damage
            else:
                game.p1_health -= final_damage
        else:
            if turn == "p1":
                game.p1_def_lvl += 1
            else:
                game.p2_def_lvl += 1
            defense_statement = game.p1_def_lvl if turn == "p1" else game.p2_def_lvl
            await ctx.send(f"{attacker} has decided to increase their defense level to **{defense_statement}!**")
        await ctx.send(f"""
`{game.p1_name}: {game.p1_health} hp
{game.p2_name}: {game.p2_health} hp`""")
        await check_win()

    choices_available = ("attack", "defend")
    in_a_fight = False
    for pairs in Fight.players_playing:
        for id in pairs:
            if ctx.author.id == id:
                in_a_fight = True
                for option in choices_available:
                    if choice.lower().strip() == option:
                        game = Fight.games_running[
                            Fight.players_playing.index(pairs)]
                        if game.turn == "p1":
                            if ctx.author.id == game.player1:
                                if game.p1_def_lvl >= 3 and choice.lower().strip() == "defend":
                                    await ctx.send("You already have a maxed out defense level")
                                    return
                                await activity_log("p1")
                            else:
                                await ctx.send("It is not your turn mate")
                        elif game.turn == "p2":
                            if ctx.author.id == game.player2:
                                if game.p2_def_lvl >= 3 and choice.lower().strip() == "defend":
                                    await ctx.send("You already have a maxed out defense level")
                                    return
                                await activity_log("p2")
                            else:
                                await ctx.send("It is not your turn mate")
                        break
                else:
                    await ctx.send("That's an invalid choice there lad, The only choices available are `attack`, `defend`")
    if not in_a_fight:
        await ctx.send("""
You're not in a fight right now mate, what are ya trying to do?
If you wanna start a fight do `d!fight <player2>` to start one""")


async def flee(ctx):
    in_fight = False
    for pair in Fight.players_playing:
        for id in pair:
            if ctx.author.id == id:
                Fight.games_running.pop(Fight.players_playing.index(pair))
                Fight.players_playing.pop(Fight.players_playing.index(pair))
                await ctx.send(f"`{ctx.author.name}` has decided to run away from the fight. What a coward!")
                in_fight = True
    if not in_fight:
        await ctx.send("What are you trying to flee from? The wind?")


async def fight_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Make sure to ping the player you want to fight")
    if isinstance(error, commands.BadArgument):
        await ctx.send("Wot.. Well make sure you ping the player you want to fight with")


async def choice_error(ctx, error):
    in_fight = False
    for pair in Fight.players_playing:
        for id in pair:
            if ctx.author.id == id:
                in_fight = True
    if in_fight:
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Make sure to choose an option... `attack` or `defend`")
        if isinstance(error, commands.BadArgument):
            await ctx.send("Invalid choice mate. You either choose `defend` or `attack`")
    else:
        await ctx.send("You're not in a fight right now. Type `d!fight <player2>` to start one")
