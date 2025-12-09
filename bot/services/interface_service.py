import discord
from bot.services.yfinance_service import yahoo_search
from database.db import add_asset, add_portfolio

# ---------------------------------------------------------
# Stockage temporaire du processus de sélection par utilisateur
# ---------------------------------------------------------
user_selection_state = {}  
# user_id: {"remaining": int, "portfolio_id": int}


# ---------------------------------------------------------
#   MODAL POUR DEMANDER LE NOMBRE DE TICKERS
# ---------------------------------------------------------
class SelectCountModal(discord.ui.Modal, title="Nombre d'actifs à choisir"):
    count = discord.ui.TextInput(
        label="Nombre d'actifs à choisir (max 10)",  # <= 45 caractères
        placeholder="Ex : 3",
        required=True
    )


    def __init__(self, interaction, pool):
        super().__init__()
        self.interaction = interaction
        self.pool = pool

    async def on_submit(self, modal_interaction: discord.Interaction):
        try:
            n = int(self.count.value)
            if n < 1 or n > 10:
                return await modal_interaction.response.send_message(
                    "❌ Le nombre doit être entre **1 et 10**.",
                    ephemeral=True,
                )
        except:
            return await modal_interaction.response.send_message(
                "❌ Merci d'entrer un **nombre valide**.",
                ephemeral=True,
            )

        user_id = modal_interaction.user.id

        # Créer un portfolio (un par session)
        portfolio_id = await add_portfolio(self.pool, user_id, "Portfolio auto")

        # Stocker l'état de sélection
        user_selection_state[user_id] = {
            "remaining": n,
            "portfolio_id": portfolio_id
        }

        # Lancer la sélection
        view = UnifiedSearch(self.pool, user_id)
        await modal_interaction.response.send_message(
            f"🟢 Tu vas pouvoir sélectionner **{n} actifs**.\n"
            "Commence par une recherche 👇",
            view=view,
            ephemeral=True
        )



# ---------------------------------------------------------
#     MODAL DE RECHERCHE
# ---------------------------------------------------------
class SearchModal(discord.ui.Modal, title="Recherche d'actif"):
    query = discord.ui.TextInput(label="Nom ou ticker", placeholder="Ex: NVDA, AAPL, ORA")

    def __init__(self, parent_view, interaction):
        super().__init__()
        self.parent_view = parent_view
        self.interaction = interaction

    async def on_submit(self, modal_interaction: discord.Interaction):
        q = self.query.value.strip()

        results = await yahoo_search(q)

        if not results:
            return await modal_interaction.response.send_message(
                f"❌ Aucun actif trouvé pour **{q}**.",
                ephemeral=True,
            )

        new_view = UnifiedSearch(self.parent_view.pool, self.parent_view.user_id)
        new_view.clear_items()

        new_view.add_item(new_view.SearchButton(new_view))
        new_view.add_item(new_view.CancelButton(new_view))
        new_view.add_item(AssetDropdown(results, new_view))

        await self.interaction.edit_original_response(
            embed=new_view.build_embed(q),
            view=new_view,
        )

        await modal_interaction.response.send_message(
            f"Résultats pour **{q}** mis à jour 👌",
            ephemeral=True,
        )



# ---------------------------------------------------------
# MODAL POUR DEMANDER LA QUANTITÉ APRÈS SÉLECTION D'ACTIF
# ---------------------------------------------------------
class AmountModal(discord.ui.Modal, title="Quantité de l'actif"):
    amount = discord.ui.TextInput(
        label="Quantité (0 possible)",
        placeholder="Ex: 3 ou 0",
        required=True
    )

    def __init__(self, parent_view, ticker, name, type_, exchange):
        super().__init__()
        self.parent_view = parent_view
        self.ticker = ticker
        self.name = name
        self.type_ = type_
        self.exchange = exchange

    async def on_submit(self, modal_interaction: discord.Interaction):
        try:
            amt = float(self.amount.value)
            if amt < 0:
                raise ValueError()
        except:
            return await modal_interaction.response.send_message(
                "❌ La quantité doit être un nombre >= 0.",
                ephemeral=True
            )

        user_id = modal_interaction.user.id
        state = user_selection_state.get(user_id)
        if not state:
            return await modal_interaction.response.send_message(
                "❌ Pas de processus de sélection en cours.",
                ephemeral=True
            )

        portfolio_id = state["portfolio_id"]

        # Ajouter l'actif avec quantité
        await add_asset(
            self.parent_view.pool,
            portfolio_id,
            self.ticker,
            self.name,
            self.type_,
            self.exchange,
            amount=amt
        )

        # Mise à jour du compteur
        state["remaining"] -= 1

        # Si terminé
        if state["remaining"] <= 0:
            del user_selection_state[user_id]
            return await modal_interaction.response.edit_message(
                content="🎉 Tu as sélectionné tous tes actifs !",
                embed=None,
                view=None
            )

        # Sinon → proposer un autre choix
        new_view = UnifiedSearch(self.parent_view.pool, user_id)
        await modal_interaction.response.edit_message(
            content=f"📈 Tu as ajouté **{self.ticker}** avec quantité **{amt}**.\n"
                    f"Encore **{state['remaining']}** à choisir.",
            embed=new_view.build_embed(),
            view=new_view
        )

# ---------------------------------------------------------
# DROPDOWN D'ACTIFS
# ---------------------------------------------------------
class AssetDropdown(discord.ui.Select):
    def __init__(self, results, parent_view):
        self.parent_view = parent_view
        self.asset_map = {r["symbol"]: r for r in results[:25]}  # <- map pour retrouver les infos

        options = [
            discord.SelectOption(
                label=r["symbol"],
                description=f"{r.get('name','')} — {r.get('exchange','')}"[:100],
            )
            for r in results[:25]
        ]

        super().__init__(
            placeholder="Sélectionne un actif…",
            options=options,
            min_values=1,
            max_values=1,
        )
        
        
    async def callback(self, interaction: discord.Interaction):
        ticker = self.values[0]
        asset = self.asset_map[ticker]
        name = asset.get("name", "")
        type_ = asset.get("type", "stock")
        exchange = asset.get("exchange", "")

        # Lancer le modal pour saisir la quantité
        modal = AmountModal(self.parent_view, ticker, name, type_, exchange)
        await interaction.response.send_modal(modal)

# ---------------------------------------------------------
# VIEW PRINCIPALE
# ---------------------------------------------------------
class UnifiedSearch(discord.ui.View):
    def __init__(self, pool, user_id):
        super().__init__(timeout=120)
        self.pool = pool
        self.user_id = user_id

        self.add_item(self.SearchButton(self))
        self.add_item(self.CancelButton(self))

    def build_embed(self, query=None):
        embed = discord.Embed(
            title="🔎 Recherche d’actifs financiers",
            description="Tape un **ticker** (NVDA) ou un **nom**.",
            color=0x2ECC71,
        )

        if query:
            embed.add_field(name="Dernière recherche :", value=f"**{query}**", inline=False)

        return embed

    # CANCEL BUTTON
    class CancelButton(discord.ui.Button):
        def __init__(self, parent_view):
            self.parent_view = parent_view
            super().__init__(
                label="❌ Annuler",
                style=discord.ButtonStyle.danger,
            )

        async def callback(self, interaction: discord.Interaction):
            user_id = interaction.user.id
            if user_id in user_selection_state:
                del user_selection_state[user_id]

            await interaction.response.edit_message(
                content="❌ Sélection annulée.",
                embed=None,
                view=None,
            )

    # SEARCH BUTTON
    class SearchButton(discord.ui.Button):
        def __init__(self, parent_view):
            self.parent_view = parent_view
            super().__init__(
                label="🔍 Rechercher",
                style=discord.ButtonStyle.success,
            )

        async def callback(self, interaction: discord.Interaction):
            modal = SearchModal(self.parent_view, interaction)
            await interaction.response.send_modal(modal)
