import discord
import utils.config as config  # import os
from discord.ext import commands

import utils.api_requests as api
import utils.keyword_responses as keyword
import utils.message_logs as mlogs
from utils.uptime import keep_alive

import games.tictactoe as ttt
import games.guess as gg
import games.rockpaperscissors as rps
import games.fight as fg
import games.economy.actions as eco

from rich.console import Console

client = discord.Client()
client = commands.Bot(command_prefix=("d!", "D!"))
client.remove_command("help")

console = Console()
previous_channel = None


@client.event
async def on_ready():
    print("We logged in as {0.user}".format(client))
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="The Castle [d!help]"))


@client.event
async def on_message(message):
    global previous_channel

    if message.author == client.user:
        return

    msg, channel = message.content, message.channel
    mlogs.message_log(message.author.name, msg, channel,
                      message.guild.id, channel != previous_channel)
    previous_channel = channel

    if any(word in msg.lower() for word in keyword.dragon):
        await message.channel.send(keyword.dragon_response())

    if any(word in msg.lower() for word in keyword.jackbox):
        await message.channel.send(keyword.jackbox_response())

    await client.process_commands(message)


@client.event
async def on_message_edit(message, edited):
    global previous_channel
    channel = message.channel
    mlogs.message_edit_log(message.author.name,
                           edited.content, message.content, channel,
                           message.guild.id, previous_channel != channel)
    previous_channel = channel


@client.command()
async def help(ctx, category=None):
    help = """
>>> **List of Help Commands:** :robot:
`- d!help general`
`- d!help memes`
`- d!help games`
`- d!help economy`"""

    general = """
>>> **List of General Commands:** :classical_building:
`- d!info`
`- d!inspire`
`- d!nft <currency>`
`- d!linux`"""

    meme = """
>>> **List of Meme Commands:** :japanese_goblin:
`- d!meme`
`- d!homicide (Comedy Homicide)`
`- d!coder (Programmer meme)`
`- d!copypasta`"""

    games = """
>>> **Game Commands:** :game_die:

**TicTacToe:**
`- d!ttt <player2>`
`- d!place <tile>`

**Guessing Game:**
`- d!gg`
`- d!guess <number>` or `d!g <guess>`

**Rock, Paper, Scissors:**
`- d!rps `
`- d!choose <option>` or `d!c <option>`

**Fighting Game:**
`- d!fight <player2>`
`- d!option <attack or defend>` or `d!opt <attack or defend>`

**For Ending/Closing Games:**
`- d!endgame` or `d!eg`"""

    economy = """
**Economy Commands:** :money_with_wings:
- `d!e register`
- `d!e scavenge`
- `d!e gold`
- `d!e rich`
*(Still work in progress)*"""
    categories = {"general": general, "memes": meme,
                  "games": games, "economy": economy}
    await ctx.send(categories[category] if category else help)


@client.command()
async def info(ctx):
    await ctx.send("""
**Hello, This is a bot created by** `DragonWF#9321`
```
This is basically just a personal bot filled with fun commands and some practical ones like 
`d!nft` to view cryptocurrency values. Just for some extra information, you can earn gold *(Bot's game currency)*
just by winning mini-games.
```
""")


# ---Utility Commands---
@client.command()
async def inspire(ctx):
    await ctx.send(api.get_quote())


@client.command()
async def nft(ctx, currency="php"):
    await ctx.send(api.view_nft_values(currency.lower()))


# ---Reddit Commands---
@client.command()
async def copypasta(ctx):
    await ctx.send(embed=api.get_copypasta())


@client.command()
async def meme(ctx):
    await ctx.send(embed=api.get_meme("memes"))


@client.command()
async def homicide(ctx):
    await ctx.send(embed=api.get_meme("homicide"))


@client.command()
async def coder(ctx):
    await ctx.send(embed=api.get_meme("coder"))


@client.command()
async def linux(ctx):
    await ctx.send(embed=api.get_meme("linux"))


# -----Economy Commands------
@client.command(aliases=("e", "eco"))
async def economy(ctx, action: str):
    await ctx.send(eco.action(action.lower().strip(), ctx.author.id, ctx.author))


@economy.error
async def economy_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument) or isinstance(error, commands.BadArgument):
        await ctx.send("You can type `d!economy help` to get the list of commands")


# -----TicTacToe-----
@client.command(aliases=["ttt"])
async def tictactoe(ctx, player2: discord.Member):
    await ttt.tictactoe(ctx, player2)


@client.command(aliases=["p"])
async def place(ctx, tile: int):
    await ttt.place(ctx, tile)


@tictactoe.error
async def tictactoe_error(ctx, error):
    await ttt.tictactoe_error(ctx, error)


@place.error
async def place_error(ctx, error):
    await ttt.place_error(ctx, error)


# ---Guessing Game---
@client.command(aliases=("guessgame", "guess-game", "ggame", "guessing-game", "gg"))
async def guessing_game(ctx):
    await gg.guessing_game(ctx)


@client.command(aliases=["g"])
async def guess(ctx, guess: int):
    await gg.guess(ctx, guess)


@guess.error
async def guess_error(ctx, error):
    await gg.guess_error(ctx, error)


# ---Rock Paper Scissors---
@client.command(aliases=("rps", "rockpaperscissors", "rock-paper-scissors"))
async def rock_paper_scissors(ctx):
    await rps.rock_paper_scissors(ctx)


@client.command(aliases=("c", "chose", "ch"))
async def choose(ctx, player_choice: str):
    await rps.choose(ctx, player_choice)


@choose.error
async def choose_error(ctx, error):
    await rps.choose_error(ctx, error)


# ---Fight Game---
@client.command()
async def fight(ctx, player2: discord.Member):
    await fg.fight(ctx, player2)


@client.command(aliases=("option", "opt", "o"))
async def choice(ctx, choice: str):
    await fg.choice(ctx, choice)


@client.command()
async def flee(ctx):
    await fg.flee(ctx)


@fight.error
async def fight_error(ctx, error):
    await fg.fight_error(ctx, error)


@choice.error
async def choice_error(ctx, error):
    await fg.choice_error(ctx, error)


# ---End game---
@client.command(aliases=("eg", "egame", "endg"))
async def endgame(ctx):
    games = (gg.Guessing, rps.RPS)
    cog = False
    for game in games:
        if game.players_playing:
            for x in range(0, len(game.players_playing)):
                if ctx.author.id == game.players_playing[x]:
                    game.players_playing.pop(x)
                    game.games_running.pop(x)
                    if not cog:
                        await ctx.send("Your game/games has been ended")
                        cog = True

    tictactoe_cog = False
    for pair in ttt.TicTacToe.players_playing:
        for id in pair:
            if ctx.author.id == id:
                ttt.TicTacToe.games_running.pop(
                    ttt.TicTacToe.players_playing.index(pair))
                ttt.TicTacToe.players_playing.pop(
                    ttt.TicTacToe.players_playing.index(pair))
                if not cog:
                    await ctx.send("Your TicTacToe match has ended")
                tictactoe_cog = True
    if not cog:
        if not tictactoe_cog:
            await ctx.send("You have no ongoing games")


keep_alive()
client.run(config.token)  # client.run(os.environ['Lothern'])
