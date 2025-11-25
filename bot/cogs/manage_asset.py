from discord.ext import commands
from bot.services.interface_service import UnifiedSearch
import discord

class ManageAssetCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 

    # ----------------------------------------------------
    # Commande selection des assets 
    # ----------------------------------------------------
    @commands.command(name="select", help="Sélectionne un actif.")
    async def select_command(self, ctx):
        embed = discord.Embed(
            title="🔎 Recherche d’actifs",
            description="Clique sur le bouton ci-dessous pour commencer.",
            color=0x2ECC71
        )

        await ctx.send(
            embed=embed,
            view=UnifiedSearch()
        )
    
    # ----------------------------------------------------
    # Commande récap des assets sélectionnés
    # ----------------------------------------------------
    #todo ajouter une commande pour récap des assets sélectionnés en dm

async def setup(bot):
    await bot.add_cog(ManageAssetCog(bot))
