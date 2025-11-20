# 📊 Trading Bot Discord

Bot Discord intelligent pour l'analyse de marché, le calcul d'indicateurs techniques et la génération de signaux de trading algorithmiques.

---

## 🚀 Fonctionnalités prévues

- ✅ **Récupération automatique** des données de marché (actions, crypto, forex)
- 📈 **Indicateurs techniques avancés** (RSI, MACD, Bollinger Bands, EMA, ATR, etc.)
- 🎯 **Signaux d'achat/vente** basés sur des stratégies algorithmiques
- 📊 **Backtesting** avec métriques de performance (ROI, Sharpe ratio, drawdown)
- 🔔 **Notifications Discord** en temps réel
- 🎮 **Commandes Discord** interactives
- 📉 **Graphiques** et visualisations
- 🔄 **Multiples stratégies** configurables

---

## 📋 Prérequis

- Python 3.12.4
- Un compte Discord avec un bot token
- Connexion Internet pour les données de marché

---

## 🛠️ Installation

### 1. Cloner le projet

```bash
...
```

### 2. Créer l'environnement virtuel

```bash
python -m venv venv
```

### 3. Activer l'environnement virtuel

**Windows :**
```bash
source venv/Scripts/activate
```

**Linux/Mac :**
```bash
source venv/bin/activate
```

### 4. Installer les dépendances

```bash
pip install -r requirement.txt
```

### 5. Configurer les variables d'environnement

Créez un fichier `.env` à la racine du projet :

```env
BOT_TOKEN=votre_token_discord_ici
COMMAND_PREFIX=$
DEBUG_MODE=False
```

Pour obtenir un token Discord :
1. Allez sur [Discord Developer Portal](https://discord.com/developers/applications)
2. Créez une nouvelle application
3. Allez dans "Bot" → "Add Bot"
4. Copiez le token

### 6. Lancer le bot

```bash
python main.py
```

---

## 📁 Structure du projet

```
trading_bot/
├── main.py                          # 🚀 Point d'entrée principal
│
├── config/                          # ⚙️ Configuration
│   ├── __init__.py
│   └── settings.py                  # Variables globales, clés API
│
├── core/                            # 🧠 Logique métier
│   ├── __init__.py
│   ├── data_manager.py              # Récupération des données (yfinance, ccxt)
│   ├── indicators.py                # Calcul des indicateurs techniques
│   ├── signal_generator.py          # Génération des signaux de trading
│   └── backtester.py                # Backtesting et simulation
│
├── strategies/                      # 📊 Stratégies de trading
│   ├── __init__.py
│   ├── base_strategy.py             # Classe abstraite
│   ├── trend_following.py           # Suivi de tendance
│   ├── mean_reversion.py            # Retour à la moyenne
│   ├── breakout_trading.py          # Trading de cassure
│   ├── ema_rsi_scalping.py          # Scalping EMA + RSI
│   └── macd_bollinger.py            # MACD + Bollinger Bands
│
├── bot/                             # 🤖 Bot Discord
│   ├── __init__.py
│   ├── bot.py                       # Instance Discord principale
│   ├── embeds.py                    # Formatage des messages
│   └── cogs/                        # Commandes modulaires
│       ├── __init__.py
│       ├── analysis.py              # Commandes d'analyse
│       ├── trading.py               # Commandes de trading
│       └── backtest.py              # Commandes de backtesting
│
├── monitoring/                      # 📡 Monitoring & Logs
│   ├── __init__.py
│   ├── logger.py                    # Système de logs
│   ├── position_tracker.py          # Suivi des positions
│   └── metrics.py                   # Métriques de performance
│
├── .env                             # 🔐 Variables d'environnement (non versionné)
├── .gitignore                       # Fichiers ignorés par Git
├── requirement.txt                  # 📦 Dépendances Python
└── readme.md                        # 📖 Documentation
```

---

## 🔧 Développement

### Ajouter une nouvelle bibliothèque

```bash
pip install nom_de_la_bibliotheque
pip freeze > requirement.txt
```