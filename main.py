"""
Trading Bot Discord - Point d'entrée principal
Bot d'analyse de marché et de trading algorithmique
"""

import sys
from bot.bot import TradingBot
from monitoring.logger import setup_logger

def main():
    """Point d'entrée principal du bot"""
    logger = setup_logger('Main')
    
    logger.info("=" * 50)
    logger.info("📊 TRADING BOT DISCORD")
    logger.info("=" * 50)
    
    try:
        # Créer et lancer le bot
        bot = TradingBot()
        bot.run_bot()
        
    except KeyboardInterrupt:
        logger.info("\n⏹️  Arrêt du bot demandé par l'utilisateur")
        sys.exit(0)
    except Exception as e:
        logger.error(f"❌ Erreur fatale: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
