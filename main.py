import os
import dotenv
from discord.ext import commands
import discord


dotenv.load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
intents = discord.Intents.default()
intents.message_content = True 


bot = commands.Bot(command_prefix='$', intents=intents)


async def load_cogs():
    for filename in os.listdir('./bot/cogs'):
        if filename.endswith('.py') and filename != '__init__.py': 
            module_name = f'bot.cogs.{filename[:-3]}'
            try:
                await bot.load_extension(module_name)
                print(f"✅ Cog chargé : {module_name}")
            except Exception as e:
                print(f"❌ Échec du chargement du Cog {module_name}. Erreur : {type(e).__name__}: {e}")


@bot.event
async def on_ready():
    await load_cogs()
    print(f'{bot.user.name} est prêt !')

if __name__ == "__main__":
    bot.run(BOT_TOKEN)