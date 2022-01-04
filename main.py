import discord
import utils.config as config  # import os
from discord.ext import commands

import utils.api_requests as api
import utils.keyword_responses as keyword
from utils.uptime import keep_alive

import games.tictactoe as ttt
import games.guess as gg
import games.rockpaperscissors as rps
import games.fight as fight

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
    if channel != previous_channel:
        console.log(
            f"[underline][bold][yellow]{channel}:[/yellow][/bold][/underline]")
    console.log(f"[bold][green]{message.author.name}:[/green][/bold] {msg}")
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
    if channel != previous_channel:
        console.log(
            f"[underline][bold][yellow]{channel}:[/yellow][/bold][/underline]")
    console.log(f"""[bold][green]{message.author.name}[/green][red] (Edit Event)[/red]:[/bold]
[cyan]Orginal Message:[/cyan] {message.content}
[red]Edited Message:[/red] {edited.content}""")
    previous_channel = channel


@client.command()
async def help(ctx):
    await ctx.send("""
>>> **List of commands:** :robot:
`- info`
`- inspire`
`- linux`
`- copypasta (Might be nsfw sometimes)`
`- nft <currency> (If no currency is provided, the default will be php)`

**Meme Commands:** :japanese_goblin: 
`- meme`
`- homicide (Comedy Homicide)`
`- coder (Programmer meme)`

**Game Commands:** :game_die:
`- ttt <person you would like to play with> (TicTacToe)
- place <tile>`
`- gg (Guess the number game)
- guess <number>`
`- rps (Rock, paper, scissors)
- choose <option>`
`- fight <person you want to fight>`
`- option <attack or defend>`
`- endgame`
- *(More will be added in the future)* :zap:
""")


@client.command()
async def info(ctx):
    await ctx.send("""
**Hello, This is a bot created by** `DragonWF#9321`
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


# -----TicTacToe-----
@client.command(aliases=["ttt"])
async def tictactoe(ctx, player2: discord.Member):
    await ttt.tictactoe(ctx, player2)


@client.command(aliases=["p"])
async def place(ctx, tile: int):
    await ttt.tictactoe(ctx, tile)


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
    await fight.fight(ctx, player2)


@client.command(aliases=("option", "opt"))
async def choice(ctx, choice: str):
    await fight.choice(ctx, choice)


@client.command()
async def flee(ctx):
    await fight.flee(ctx)


@fight.error
async def fight_error(ctx, error):
    await fight.fight_error(ctx, error)


@choice.error
async def choice_error(ctx, error):
    await fight.choice_error(ctx, error)


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
