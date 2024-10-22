import discord
from discord.ext import commands
import chess
import chess.svg

class ChessGame(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.games = {}

    async def send_board(self, ctx, board):
        """Send the current chess board to the chat."""
        board_image = board.unicode()
        await ctx.send(f"```\n{board_image}\n```")

    @commands.command(name="chess_start")
    async def start_game(self, ctx, opponent: discord.Member = None):
        """Start a new chess game. If no opponent is specified, the user plays against the bot."""
        if ctx.author.id in self.games:
            await ctx.send("You already have an ongoing game!")
            return

        board = chess.Board()

        # Check if playing against bot or another user
        if opponent is None:
            self.games[ctx.author.id] = {
                "board": board,
                "opponent": "bot"
            }
            await ctx.send("Starting a game against the bot!")
        else:
            self.games[ctx.author.id] = {
                "board": board,
                "opponent": opponent.id
            }
            self.games[opponent.id] = self.games[ctx.author.id]
            await ctx.send(f"Starting a game between {ctx.author.mention} and {opponent.mention}!")

        await self.send_board(ctx, board)

    @commands.command(name="chess_move")
    async def make_move(self, ctx, move: str):
        """Make a move in your ongoing chess game."""
        if ctx.author.id not in self.games:
            await ctx.send("You don't have an active game! Start one with !chess_start")
            return

        game = self.games[ctx.author.id]
        board = game['board']

        try:
            chess_move = chess.Move.from_uci(move)
            if chess_move not in board.legal_moves:
                await ctx.send("Invalid move! Please try again.")
                return

            board.push(chess_move)
            await self.send_board(ctx, board)

            if board.is_game_over():
                if board.is_checkmate():
                    await ctx.send("Checkmate! Game over!")
                elif board.is_stalemate():
                    await ctx.send("Stalemate! It's a draw!")
                else:
                    await ctx.send("The game is over!")
                self.games.pop(ctx.author.id)
                if game['opponent'] != 'bot':
                    self.games.pop(game['opponent'])
                return

            # Bot move if playing against the bot
            if game['opponent'] == "bot":
                move = self.bot_move(board)
                board.push(move)
                await ctx.send(f"Bot played: {move}")
                await self.send_board(ctx, board)

                if board.is_game_over():
                    if board.is_checkmate():
                        await ctx.send("Checkmate! The bot wins!")
                    elif board.is_stalemate():
                        await ctx.send("Stalemate! It's a draw!")
                    else:
                        await ctx.send("The game is over!")
                    self.games.pop(ctx.author.id)
                    return

        except Exception as e:
            await ctx.send(f"Error: {str(e)}")

    def bot_move(self, board):
        """Simple AI move (just a random legal move)."""
        import random
        legal_moves = list(board.legal_moves)
        return random.choice(legal_moves)

    @commands.command(name="chess_resign")
    async def resign_game(self, ctx):
        """Resign from your chess game."""
        if ctx.author.id not in self.games:
            await ctx.send("You don't have an active game!")
            return

        game = self.games.pop(ctx.author.id)
        if game['opponent'] != 'bot':
            self.games.pop(game['opponent'])

        await ctx.send(f"{ctx.author.mention} has resigned. Game over!")

def setup(bot):
    bot.add_cog(ChessGame(bot))
