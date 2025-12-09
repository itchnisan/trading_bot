import asyncio
import asyncpg
from datetime import datetime

DATABASE_URL = "postgresql://postgres:admin@localhost:5432/tradingbot"

# -----------------------------
# FONCTIONS DE BASE
# -----------------------------
async def create_tables(pool):
    async with pool.acquire() as conn:
        await conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id BIGINT PRIMARY KEY,
            username VARCHAR(100),
            created_at TIMESTAMP DEFAULT NOW(),
            premium BOOLEAN DEFAULT FALSE
        );
        CREATE TABLE IF NOT EXISTS portfolios (
            id SERIAL PRIMARY KEY,
            user_id BIGINT REFERENCES users(id) ON DELETE CASCADE,
            name VARCHAR(100),
            created_at TIMESTAMP DEFAULT NOW()
        );
        CREATE TABLE IF NOT EXISTS assets (
            id SERIAL PRIMARY KEY,
            portfolio_id INT REFERENCES portfolios(id) ON DELETE CASCADE,
            symbol VARCHAR(20) NOT NULL,
            name VARCHAR(150),
            type VARCHAR(20),
            exchange VARCHAR(50),
            amount FLOAT DEFAULT 0,
            avg_price FLOAT DEFAULT 0,
            last_signal VARCHAR(10),
            last_notif_at TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS signals (
            id SERIAL PRIMARY KEY,
            asset_id INT REFERENCES assets(id) ON DELETE CASCADE,
            strategy VARCHAR(50),
            signal VARCHAR(10),
            price FLOAT,
            generated_at TIMESTAMP DEFAULT NOW(),
            notified BOOLEAN DEFAULT FALSE
        );
        """)

# -----------------------------
# UTILISATEUR & PORTEFEUILLE
# -----------------------------
async def add_user(pool, user_id: int, username: str):
    async with pool.acquire() as conn:
        await conn.execute(
            "INSERT INTO users(id, username) VALUES($1, $2) ON CONFLICT DO NOTHING",
            user_id, username
        )

async def add_portfolio(pool, user_id: int, name: str):
    async with pool.acquire() as conn:
        record = await conn.fetchrow(
            "INSERT INTO portfolios(user_id, name) VALUES($1, $2) RETURNING id",
            user_id, name
        )
        return record["id"]

# -----------------------------
# AJOUT D’UN ACTIF
# -----------------------------
async def add_asset(pool, portfolio_id: int, symbol: str, name: str, type_: str, exchange: str, amount=0, avg_price=0):
    async with pool.acquire() as conn:
        record = await conn.fetchrow("""
            INSERT INTO assets(portfolio_id, symbol, name, type, exchange, amount, avg_price)
            VALUES($1,$2,$3,$4,$5,$6,$7)
            RETURNING id
        """, portfolio_id, symbol, name, type_, exchange, amount, avg_price)
        return record["id"]

# -----------------------------
# GENERATION D’UN SIGNAL
# -----------------------------
async def generate_signal(pool, asset_id: int, strategy: str, signal: str, price: float):
    async with pool.acquire() as conn:
        await conn.execute("""
            INSERT INTO signals(asset_id, strategy, signal, price)
            VALUES($1,$2,$3,$4)
        """, asset_id, strategy, signal, price)

        # Mettre à jour last_signal pour l’actif
        await conn.execute("""
            UPDATE assets SET last_signal=$1, last_notif_at=$2
            WHERE id=$3
        """, signal, datetime.utcnow(), asset_id)

# -----------------------------
# CHECK SIGNALS A NOTIFIER
# -----------------------------
async def get_pending_signals(pool):
    async with pool.acquire() as conn:
        return await conn.fetch("""
            SELECT s.id, s.asset_id, s.strategy, s.signal, s.price, a.symbol, a.last_notif_at
            FROM signals s
            JOIN assets a ON a.id = s.asset_id
            WHERE s.notified = FALSE
        """)

# -----------------------------
# MARQUER COMME NOTIFIE
# -----------------------------
async def mark_signal_notified(pool, signal_id: int):
    async with pool.acquire() as conn:
        await conn.execute("""
            UPDATE signals SET notified=TRUE WHERE id=$1
        """, signal_id)

# -----------------------------
# verifie si le user existe
# -----------------------------
async def ensure_user(pool, discord_id, username):
    async with pool.acquire() as conn:
        await conn.execute("""
            INSERT INTO users (id, username)
            VALUES ($1, $2)
            ON CONFLICT (id) DO NOTHING;
        """, discord_id, username)

async def init_db():
    return await asyncpg.create_pool(
        user="postgres",
        password="admin",
        database="tradingbot",
        host="localhost",
        port=5432
    )


