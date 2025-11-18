from discord.ext import commands
import discord

class HelloCog(commands.Cog):
    """
    Un Cog simple pour démontrer l'utilisation des commandes de base.
    """
    
    def __init__(self, bot):
        # Stocke l'instance du bot.
        self.bot = bot 
    
    # --- Commande $hello ---
    @commands.command(name='hello', help='Dit bonjour en retour !')
    async def hello_command(self, ctx):
        """
        Répond à l'utilisateur qui exécute la commande avec un message de bienvenue.
        """
        await ctx.send(f"Salut {ctx.author.display_name} ! Je suis le bot.")


# ----------------------------------------------------
# Fonction OBLIGATOIRE pour charger le Cog
# ----------------------------------------------------
async def setup(bot):
    await bot.add_cog(HelloCog(bot))