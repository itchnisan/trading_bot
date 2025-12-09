python -m venv venv
source venv/Scripts/activate
pip install requirement.txt


si tu rajoute des biblio 
pip freeze ->  requirements.txt


statégie SWING TRADE :

## Indicateurs nécessaires (3 à 4 max)

EMA 50
→ Tendance moyen terme fiable

EMA 200
→ Filtre ultime pour éviter un mauvais marché

RSI (14)
→ Momentum simple mais très efficace

OBV (On-Balance Volume)
→ Confirmation du mouvement (indicateur défensif par excellence)

Chaque indicateur doit avoir un rôle différent :

Rôle	Indicateur	Pourquoi ?
Tendance	EMA 50	Tendance claire et rapide
Macro-tendance	EMA 200	Filtre les marchés trop risqués
Momentum	RSI	Détecte fin de baisse / surachat
Volume	OBV	Valide si le mouvement est réel

Ajouter plus = faire doublon → affaiblit le bot.


### RÈGLES —  Défensive 
## Achat (Long)

Prix au-dessus de l’EMA 200
→ marché « safe »

EMA 50 ≥ EMA 200
→ tendance haussière stable

RSI sort de la survente (remonte au-dessus de 35)
→ momentum positif

OBV monte depuis au moins 3–5 périodes
→ accumulation → mouvement crédible

Quand ces 4 signaux sont alignés → entrée propre et défensive.


## Vente (Sortie)

Sortir si un seul arrive :

RSI > 70

EMA 50 casse EMA 200 à la baisse

OBV diverge (prix monte mais OBV baisse)

## A ajouter après 
Stop-loss ATR touché


## Algo 

INITIALISATION :
    - Charger données OHLC (open, high, low, close, volume)
    - Calculer :
        EMA50 = moyenne mobile exponentielle 50 périodes
        EMA200 = moyenne mobile exponentielle 200 périodes
        RSI = Relative Strength Index sur 14 périodes
        OBV = On-Balance Volume
    - Position = AUCUNE

BOUCLE PRINCIPALE (à chaque nouvelle bougie) :

------------------------------------------------
### CONDITIONS D'ACHAT (SIGNAL LONG)
------------------------------------------------

SI Position == AUCUNE :

    SI  Prix > EMA200                        // marché sain
        ET EMA50 >= EMA200                   // tendance haussière stable
        ET RSI > 35                          // momentum revient
        ET OBV en augmentation sur 3-5 périodes :
        
            ALORS :
                - Entrée en position LONG
                - PrixEntrée = prix actuel
                - StopLoss = PrixEntrée - (1.5 * ATR)   // optionnel mais conseillé
                - TakeProfit = PrixEntrée + (2.5 * ATR) // ratio défensif
                - Position = LONG


------------------------------------------------
### CONDITIONS DE SORTIE (FERMETURE)
------------------------------------------------

SI Position == LONG :

    SI RSI > 70                               // surachat : prendre les gains
        OU EMA50 < EMA200                     // tendance cassée
        OU OBV baisse sur 3 périodes          // divergence
        OU Prix <= StopLoss                   // si SL activé
        OU Prix >= TakeProfit                 // TP atteint

        ALORS :
            - Fermer la position
            - Position = AUCUNE


------------------------------------------------
### FIN DE BOUCLE
------------------------------------------------
LOGIQUE RÉSUMÉE 
Tu achètes seulement quand :
→ le marché est haussier (EMA50 > EMA200, prix > EMA200)
→ le momentum revient (RSI > 35)
→ le volume valide le mouvement (OBV monte)

Et tu sors au moindre signal de faiblesse.