import os
from dotenv import load_dotenv
from pathlib import Path

# Charger les variables d'environnement
load_dotenv()

class Settings:
    """Configuration globale du bot de trading"""
    
    # Discord
    BOT_TOKEN: str = os.getenv('BOT_TOKEN', '')
    COMMAND_PREFIX: str = os.getenv('COMMAND_PREFIX', '/')
    
    # Bot Configuration
    DEBUG_MODE: bool = os.getenv('DEBUG_MODE', 'False').lower() == 'true'
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    
    # Trading Settings
    DEFAULT_STRATEGY: str = os.getenv('DEFAULT_STRATEGY', 'trend_following')
    SIMULATION_MODE: bool = os.getenv('SIMULATION_MODE', 'True').lower() == 'true'
    
    # Risk Management
    DEFAULT_RISK_PERCENT: float = float(os.getenv('DEFAULT_RISK_PERCENT', '1.0'))
    MAX_POSITIONS: int = int(os.getenv('MAX_POSITIONS', '5'))
    
    # Indicateurs par défaut
    RSI_PERIOD: int = 14
    RSI_OVERBOUGHT: int = 70
    RSI_OVERSOLD: int = 30
    
    EMA_FAST: int = 20
    EMA_SLOW: int = 50
    EMA_LONG: int = 200
    
    MACD_FAST: int = 12
    MACD_SLOW: int = 26
    MACD_SIGNAL: int = 9
    
    BOLLINGER_PERIOD: int = 20
    BOLLINGER_STD: int = 2
    
    ATR_PERIOD: int = 14
    ATR_MULTIPLIER: float = 1.5
    
    # API Keys (optionnel)
    ALPHA_VANTAGE_KEY: str = os.getenv('ALPHA_VANTAGE_KEY', '')
    BINANCE_API_KEY: str = os.getenv('BINANCE_API_KEY', '')
    BINANCE_SECRET_KEY: str = os.getenv('BINANCE_SECRET_KEY', '')
    
    # Paths
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    LOGS_DIR: Path = BASE_DIR / 'logs'
    DATA_DIR: Path = BASE_DIR / 'data'
    
    def __init__(self):
        """Créer les dossiers nécessaires"""
        self.LOGS_DIR.mkdir(exist_ok=True)
        self.DATA_DIR.mkdir(exist_ok=True)
        
        # Validation du token
        if not self.BOT_TOKEN:
            raise ValueError("BOT_TOKEN manquant dans le fichier .env")
    
    def get_indicator_params(self) -> dict:
        """Retourne les paramètres des indicateurs sous forme de dictionnaire"""
        return {
            'rsi': {
                'period': self.RSI_PERIOD,
                'overbought': self.RSI_OVERBOUGHT,
                'oversold': self.RSI_OVERSOLD
            },
            'ema': {
                'fast': self.EMA_FAST,
                'slow': self.EMA_SLOW,
                'long': self.EMA_LONG
            },
            'macd': {
                'fast': self.MACD_FAST,
                'slow': self.MACD_SLOW,
                'signal': self.MACD_SIGNAL
            },
            'bollinger': {
                'period': self.BOLLINGER_PERIOD,
                'std': self.BOLLINGER_STD
            },
            'atr': {
                'period': self.ATR_PERIOD,
                'multiplier': self.ATR_MULTIPLIER
            }
        }

# Instance globale
settings = Settings()
