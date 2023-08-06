#discord
import discord
from discord.ext import commands
#secret
from secret import *
#constants
from _constants import *


#Base Cog
class Base(commands.Cog,name="Base Cog"):
    def __init__(self,bot):
        self.bot=bot
    
    @commands.Cog.listener()
    async def on_member_join(self,member):
        pass

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening))
        print(f'{self.bot.user.name} has connected to Discord!')

    # YOUR FUNCTIONS





def setup(bot):
    bot.add_cog(Base(bot))