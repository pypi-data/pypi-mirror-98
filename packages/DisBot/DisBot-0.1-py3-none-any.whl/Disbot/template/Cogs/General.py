#discord
import discord
from discord.ext import commands
#constants
from _constants import *
#secret
from secret import *


#General Cog
class General(commands.Cog,name="General Cog"):
    def __init__(self,bot):
        self.bot=bot
    
    @commands.command(name="disbot",help="Test command by Disbot")
    async def _default(self,ctx):
        await ctx.send(f"<@{ctx.author}> Hurray! You have successfully setup the required things! I know you are gonna make me a :star: with your skills.")    



def setup(bot):
    bot.add_cog(General(bot))