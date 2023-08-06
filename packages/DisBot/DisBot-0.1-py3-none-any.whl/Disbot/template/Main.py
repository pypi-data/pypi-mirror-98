import discord
from discord.ext import commands
from settings import COGS
from secret import DISCORD_TOKEN


def main():

    # For version >1.5.0 of discord py
    intents=discord.Intents.default()
    intents.members=True
    
    # Default command prefix is '!!'.
    bot=commands.Bot(command_prefix="!!",intents=intents)
    
    for PATH in COGS:
        bot.load_extension(PATH)
    
    bot.run(DISCORD_TOKEN)


if __name__ == "__main__":
    main()