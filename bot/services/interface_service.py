# bot/services/interface_service.py
import discord
from bot.services.yfinance_service import yahoo_search


class SearchModal(discord.ui.Modal, title="Recherche d'actif"):
    query = discord.ui.TextInput(label="Nom ou ticker", placeholder="Ex: AAPL")

    def __init__(self, parent_view, interaction):
        super().__init__()
        self.parent_view = parent_view
        # on garde l'interaction du bouton pour pouvoir éditer le message original
        self.interaction = interaction

    async def on_submit(self, modal_interaction: discord.Interaction):
        q = self.query.value.strip()
        formatted = q if q.isupper() else q.lower()

        results = await yahoo_search(formatted)

        if not results:
            return await modal_interaction.response.send_message(
                "❌ Aucun résultat.",
                ephemeral=True
            )

        # Remplacement du bouton par le dropdown
        new_view = UnifiedSearch()
        new_view.clear_items()
        new_view.add_item(AssetDropdown(results))

        # on édite le message original lié au bouton (celui qui contient la view)
        await self.interaction.edit_original_response(
            embed=new_view.build_embed(formatted),
            view=new_view
        )

        # petit retour éphémère pour fermer le modal proprement
        await modal_interaction.response.send_message(
            "Résultats mis à jour 👌",
            ephemeral=True
        )


class AssetDropdown(discord.ui.Select):
    def __init__(self, results):
        options = [
            discord.SelectOption(
                label=r["symbol"],
                description=f"{r.get('shortname','')} — {r.get('exchange','')} ({r.get('type','')})"[:100]
            ) for r in results[:25]
        ]

        super().__init__(
            placeholder="Sélectionne un actif…",
            options=options,
            min_values=1,
            max_values=1
        )

    async def callback(self, interaction: discord.Interaction):
        ticker = self.values[0]

        await interaction.response.edit_message(
            content=f"📈 Tu as sélectionné **{ticker}**",
            embed=None,
            view=None
        )


class UnifiedSearch(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=120)
        # on passe la view courante au bouton (si besoin)
        self.add_item(self.SearchButton(self))

    def build_embed(self, query=None):
        embed = discord.Embed(
            title="🔎 Recherche d’actifs financiers",
            description="Tape un nom / ticker dans la fenêtre.",
            color=0x2ECC71
        )
        if query:
            embed.add_field(
                name="Recherche :",
                value=f"**{query}**",
                inline=False
            )
        return embed

    class SearchButton(discord.ui.Button):
        def __init__(self, parent_view):
            # on stocke dans un attribut non réservé
            self.parent_view = parent_view
            super().__init__(
                label="🔍 Rechercher",
                style=discord.ButtonStyle.primary
            )

        async def callback(self, interaction: discord.Interaction):
            # on ouvre un modal (aucun message public envoyé dans le salon)
            modal = SearchModal(self.parent_view, interaction)
            await interaction.response.send_modal(modal)
