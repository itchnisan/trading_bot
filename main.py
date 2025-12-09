import os
import dotenv
from discord.ext import commands
import discord
from database.db import init_db

dotenv.load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="$", intents=intents)
bot.pool = None

# Charger les cogs proprement
async def load_cogs():
    for filename in os.listdir('./bot/cogs'):
        if filename.endswith('.py') and filename != '__init__.py':
            module_name = f'bot.cogs.{filename[:-3]}'
            await bot.load_extension(module_name)
            print(f"✅ Cog chargé : {module_name}")

GUILD_ID = 1440323642796937328  # remplace par ton serveur

@bot.event
async def on_ready():
    bot.pool = await init_db()
    await load_cogs()

    guild = discord.Object(id=GUILD_ID)
    synced = await bot.tree.sync(guild=guild)

    print(f"[DEBUG] Commands sync → {len(synced)} commandes")
    print(f"{bot.user} prêt !")


bot.run(BOT_TOKEN)
