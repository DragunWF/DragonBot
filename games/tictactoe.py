import discord
import random
from discord.ext import commands
from .economy.rewards import game_reward


class TicTacToe:
    players_playing = []
    games_running = []

    def __init__(self, player1, player2):
        self.player1, self.player2 = player1, player2  # IDs
        self.turn = ""
        self.board = [
            ":white_large_square:", ":white_large_square:", ":white_large_square:",
            ":white_large_square:", ":white_large_square:", ":white_large_square:",
            ":white_large_square:", ":white_large_square:", ":white_large_square:"
        ]
        self.mark = ":regional_indicator_x:"
    winning_conditions = (
        (0, 1, 2),
        (3, 4, 5),
        (6, 7, 8),
        (0, 3, 6),
        (1, 4, 7),
        (2, 5, 8),
        (0, 4, 8),
        (2, 4, 6)
    )


async def tictactoe(ctx, player2: discord.Member):
    async def create_game():
        game = TicTacToe(ctx.author.id, player2.id)
        turn_choice = ("p1", "p2")
        game.turn = random.choice(turn_choice)
        TicTacToe.players_playing.append((ctx.author.id, player2.id))
        TicTacToe.games_running.append(game)
        await ctx.send("Welcome to TicTacToe!, type `!place <tile>` or `!p <tile>` to place your mark")
        if game.turn == "p1":
            await ctx.send(f"<@{ctx.author.id}> goes first")
        elif game.turn == "p2":
            await ctx.send(f"<@{player2.id}> goes first")

    in_game = False
    if TicTacToe.players_playing:
        for pair in TicTacToe.players_playing:
            for player in pair:
                if ctx.author.id == player or player2.id == player:
                    await ctx.send("One of you is already in a game, Type `d!eg` or `d!endgame` to end those games")
                    in_game = True
                    break
        if not in_game:
            await create_game()
    else:
        await create_game()


async def place(ctx, tile: int):
    async def change_board(tile):
        async def delete_game():
            TicTacToe.players_playing.pop(
                TicTacToe.players_playing.index((game.player1, game.player2)))
            TicTacToe.games_running.pop(TicTacToe.games_running.index(game))
            reward = game_reward(ctx.author.id, "tictactoe")
            if reward:
                await ctx.send(reward)

        async def check_win():
            conditions = TicTacToe.winning_conditions
            for cond in conditions:
                if game.board[cond[0]] == x_mark and game.board[cond[1]] == x_mark and game.board[cond[2]] == x_mark:
                    await delete_game()
                    await ctx.send(f"<@{ctx.author.id}> wins the game!")
                elif game.board[cond[0]] == o_mark and game.board[cond[1]] == o_mark and game.board[cond[2]] == o_mark:
                    await delete_game()
                    await ctx.send(f"<@{ctx.author.id}> wins the game!")
            for tile in game.board:
                if tile == ":white_large_square:":
                    break
            else:
                await delete_game()
                await ctx.send(f"No one won the game...")

        async def switch_turn():
            if game.turn == "p1":
                game.turn = "p2"
            else:
                game.turn = "p1"
        tile -= 1
        if game.board[tile] == ":white_large_square:":  # :white_large_square:
            game.board[tile] = game.mark
            if game.mark == x_mark:
                game.mark = o_mark
            else:
                game.mark = x_mark
            await ctx.send(f"{game.board[0]} {game.board[1]} {game.board[2]}")
            await ctx.send(f"{game.board[3]} {game.board[4]} {game.board[5]}")
            await ctx.send(f"{game.board[6]} {game.board[7]} {game.board[8]}")
            await check_win()
            await switch_turn()
        else:
            await ctx.send("There's already a mark on that tile m8")
    player_in_game = False
    for pair in TicTacToe.players_playing:
        for id in pair:
            if ctx.author.id == id:
                player_in_game = True
                game = TicTacToe.games_running[
                    TicTacToe.players_playing.index(pair)]
                allow = {"p1": game.player1, "p2": game.player2}
                x_mark, o_mark = ":regional_indicator_x:", ":o2:"
                if game.turn == "p1":
                    if ctx.author.id != allow["p1"]:
                        await ctx.send("It is not your turn mate..")
                    else:
                        await change_board(tile)
                elif game.turn == "p2":
                    if ctx.author.id != allow["p2"]:
                        await ctx.send("It is not your turn mate..")
                    else:
                        await change_board(tile)
    if not player_in_game:
        await ctx.send("You don't have a game running at the moment. Type `d!ttt <player2>` to start one")


async def tictactoe_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Don't forget to mention the player you want to play with")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Oi lad, As I said.. Choose an integer from 1 to 9, nothing else")


async def place_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("I think you forgot to select a tile...")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Mate... Choose an integer from 1 to 9, nothing else..")
