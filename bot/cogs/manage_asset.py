from discord import app_commands, Interaction
import discord
from discord.ext import commands
from bot.services.interface_service import SelectCountModal
from database.db import ensure_user

class ManageAssetCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="start",
        description="Commencer la sélection d'actifs"
    )
    async def start(self, interaction: Interaction):
        # S'assurer que l'utilisateur est dans la base
        await ensure_user(self.bot.pool, interaction.user.id, interaction.user.name)

        # Lancer le modal
        modal = SelectCountModal(interaction, self.bot.pool)
        await interaction.response.send_modal(modal)


GUILD_ID = 1440323642796937328 
async def setup(bot):
    cog = ManageAssetCog(bot)
    await bot.add_cog(cog)
    
    # Ajouter explicitement la commande au tree
    bot.tree.add_command(cog.start, guild=discord.Object(id=GUILD_ID))
    print("[DEBUG] Slash commands dans ce cog :", [c.name for c in bot.tree.get_commands()])

