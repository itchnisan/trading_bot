from discord import app_commands, Interaction
import discord
from discord.ext import commands
from bot.services.interface_service import SelectCountModal
from database.db import ensure_user

class Analyze_strategies(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="ask_defensive_analyze",
        description="Commencer la sélection d'actifs"
    )
    async def ask_defensive_analyze(self, interaction: Interaction):
        # launch strategy
        print("Defensive analyze command invoked")

    @app_commands.command(
        name="ask_aggressive_analyze",
        description="Commencer la sélection d'actifs"
    )
    async def ask_aggressive_analyze(self, interaction: Interaction):
        # launch strategy
        
        print("Aggressive analyze command invoked")


GUILD_ID = 1440323642796937328 
async def setup(bot):
    cog = Analyze_strategies(bot)
    await bot.add_cog(cog)
    
    # Ajouter explicitement la commande au tree
    bot.tree.add_command(cog.ask_defensive_analyze, guild=discord.Object(id=GUILD_ID))
    bot.tree.add_command(cog.ask_aggressive_analyze, guild=discord.Object(id=GUILD_ID))
    print("[DEBUG] Slash commands dans ce cog :", [c.name for c in bot.tree.get_commands()])

