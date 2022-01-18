import random
from discord.ext import commands
from .economy.rewards import game_reward


class RPS:
    players_playing = []
    games_running = []

    def __init__(self, player):
        self.player = player
        self.option = ""
        self.ai_option = None
        self.player_points = 0
        self.ai_points = 0


async def rock_paper_scissors(ctx):
    async def new_game():
        new = RPS(ctx.author.id)
        RPS.players_playing.append(new.player)
        RPS.games_running.append(new)
        await ctx.send("""
Welcome to the game where you play Rock, Paper, Scissors against me!
- Type `d!choose <option>` or `d!c <option>` to choose an option (Rock, Paper, Scissors)
*(First to three points wins the game)*
        """)
    if bool(RPS.players_playing):
        for id in RPS.players_playing:
            if ctx.author.id == id:
                await ctx.send("You already have a game running! `Type d!endgame or d!eg to end it`")
                break
        else:
            await new_game()
    else:
        await new_game()


async def choose(ctx, player_choice: str):
    async def check_win():
        def delete_game():
            RPS.players_playing.pop(RPS.players_playing.index(ctx.author.id))
            RPS.games_running.pop(RPS.games_running.index(game))
        if game.player_points >= 3:
            await ctx.send("Congrats you win the game!")
            reward = game_reward(ctx.author.id, "rockpaperscissors")
            if reward:
                await ctx.send(reward)
            delete_game()
        elif game.ai_points >= 3:
            await ctx.send("LEL I WIN YOU LOSE LELELELELELELELELLELELELELELEL")
            delete_game()
    operator = RPS.games_running
    choices = ("rock", "paper", "scissors")
    counter_parts = ("paper", "scissors", "rock")
    if bool(RPS.players_playing):
        if ctx.author.id in RPS.players_playing:
            for player in RPS.players_playing:
                if ctx.author.id == player:
                    game = operator[RPS.players_playing.index(ctx.author.id)]
                    game.option = player_choice.lower()
                    for choice in choices:
                        if game.option == choice:
                            game.ai_option = random.choice(choices)
                            draw = False
                            for x in range(3):
                                if game.option == choices[x] and game.ai_option == counter_parts[x]:
                                    game.ai_points += 1
                                    await ctx.send(f"I chose **{game.ai_option}**, I win a point")
                                    break
                                elif game.option == counter_parts[x] and game.ai_option == choices[x]:
                                    game.player_points += 1
                                    await ctx.send(f"I chose **{game.ai_option}**, I lose a point")
                                    break
                                elif game.option == choices[x] and game.ai_option == choices[x]:
                                    draw = True
                                    await ctx.send(f"I chose **{game.ai_option}**, draw")
                                    break
                            if not draw:
                                await ctx.send(f"""
`Current Points:
{ctx.author.name}: {game.player_points}
DragonBot: {game.ai_points}`
                            """)
                            await check_win()
                            break
                    else:
                        await ctx.send("That's an invalid choice there lad")
        else:
            await ctx.send("You have no rock, paper, scissors game ongoing at the moment")
    else:
        await ctx.send("You have no rock, paper, scissors game ongoing at the moment")


async def choose_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        if ctx.author.id in RPS.players_playing:
            await ctx.send("Oi lad, Choose an option `(Rock, Paper, Scissors)`")
        else:
            await ctx.send("You're not in a game right now. Type `d!rps` to start one")
