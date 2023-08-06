#discord
import discord
from discord.ext import commands
#secret
from secret import *
#constants
from _constants import *


#Errors cog
class Errors(commands.Cog,name="Errors Cog"):
    def __init__(self,bot):
        self.bot=bot

    @commands.Cog.listener()
    async def on_command_error(self,ctx, error):
       await ctx.send(f"<@{ctx.author.id}> {error}")
        

def setup(bot):
    bot.add_cog(Errors(bot))