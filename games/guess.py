import random
from .economy.rewards import game_reward
from discord.ext import commands


class Guessing:
    players_playing = []
    games_running = []

    def __init__(self, player):
        self.player = player
        self.guess = None
        self.retries = 0
        self.correct_number = random.randint(1, 100)


async def guessing_game(ctx):
    async def new_game():
        new = Guessing(ctx.author.id)
        Guessing.players_playing.append(new.player)
        Guessing.games_running.append(new)
        await ctx.send("""
Welcome to the game where you try guess the correct number from 1 to 100!
- Type `d!g <number>` or `d!guess <number>` to make a guess
*Note: Don't worry, You'll be provided with hints with every wrong guess you make*
        """)

    if bool(Guessing.players_playing):
        for id in Guessing.players_playing:
            if ctx.author.id == id:
                await ctx.send("You already have a game running! `Type d!endgame or d!eg to end it`")
                break
        else:
            await new_game()
    else:
        await new_game()


async def guess(ctx, guess: int):
    operator = Guessing.games_running
    if Guessing.players_playing:
        for player in Guessing.players_playing:
            if ctx.author.id == player:
                game = operator[Guessing.players_playing.index(ctx.author.id)]
                if guess == game.correct_number:
                    await ctx.send(f"""
                    Congrats! You guessed the correct number!
`Number of retries: {game.retries}`
                    """)
                    Guessing.players_playing.pop(
                        Guessing.players_playing.index(ctx.author.id))
                    Guessing.games_running.pop(
                        Guessing.games_running.index(game))
                    reward = game_reward(ctx.author.id, "guess")
                    if reward:
                        await ctx.send(reward)
                    break
                elif guess > game.correct_number:
                    game.retries += 1
                    await ctx.send("Too High!")
                    break
                elif guess < game.correct_number:
                    game.retries += 1
                    await ctx.send("Too Low!")
                    break
        else:
            await ctx.send("You have no guessing games ongoing")
    else:
        await ctx.send("You have no guessing games ongoing")


async def guess_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("You either don't have a game currently running or you didn't make a guess")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Make sure to choose an integer for your guess")
