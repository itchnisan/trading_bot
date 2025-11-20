import discord
from discord.ext import commands
from config.settings import settings
from monitoring.logger import setup_logger

class TradingBot(commands.Bot):
    """Bot Discord principal pour le trading algorithmique"""
    
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True
        
        super().__init__(
            command_prefix=settings.COMMAND_PREFIX,
            intents=intents,
            help_command=None  # Nous créerons notre propre commande help
        )
        
        self.logger = setup_logger('TradingBot')
        self.active_strategies = {}  # {symbol: strategy_instance}
        self.monitored_symbols = set()
        
    async def setup_hook(self):
        """Appelé lors de l'initialisation du bot"""
        self.logger.info("🚀 Initialisation du Trading Bot...")
        
        # Charger les cogs (sera fait dans les prochains jours)
        # await self.load_extension('bot.cogs.analysis')
        # await self.load_extension('bot.cogs.trading')
        # await self.load_extension('bot.cogs.backtest')
        
        self.logger.info("✅ Setup terminé")
    
    async def on_ready(self):
        """Appelé quand le bot est connecté et prêt"""
        self.logger.info(f'✅ Bot connecté en tant que {self.user.name} (ID: {self.user.id})')
        self.logger.info(f'📊 Mode: {"SIMULATION" if settings.SIMULATION_MODE else "RÉEL"}')
        self.logger.info(f'🎯 Stratégie par défaut: {settings.DEFAULT_STRATEGY}')
        self.logger.info(f'🔧 Préfixe des commandes: {settings.COMMAND_PREFIX}')
        self.logger.info('─' * 50)
        
        # Changer le statut du bot
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="les marchés 📈"
            ),
            status=discord.Status.online
        )
    
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        """Gestion des erreurs de commandes"""
        if isinstance(error, commands.CommandNotFound):
            await ctx.send(f"❌ Commande inconnue. Utilisez `{settings.COMMAND_PREFIX}help`")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"❌ Argument manquant: {error.param.name}")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ Vous n'avez pas les permissions nécessaires")
        else:
            self.logger.error(f"Erreur de commande: {error}", exc_info=error)
            await ctx.send(f"❌ Une erreur s'est produite: {str(error)}")
    
    async def on_message(self, message: discord.Message):
        """Appelé pour chaque message"""
        # Ignorer les messages du bot lui-même
        if message.author.bot:
            return
        
        # Log des commandes en mode debug
        if settings.DEBUG_MODE and message.content.startswith(settings.COMMAND_PREFIX):
            self.logger.debug(f"Commande reçue: {message.content} de {message.author}")
        
        # Traiter les commandes
        await self.process_commands(message)
    
    def run_bot(self):
        """Lance le bot"""
        try:
            self.logger.info("🔄 Démarrage du bot...")
            self.run(settings.BOT_TOKEN)
        except discord.LoginFailure:
            self.logger.error("❌ Token Discord invalide. Vérifiez votre fichier .env")
        except Exception as e:
            self.logger.error(f"❌ Erreur critique: {e}", exc_info=True)
