import random

class De:
    # -------------------------------------------------------------------
    # Classe représentant un dé avec une valeur aléatoire entre 1 et 6.
    # -------------------------------------------------------------------

    def __init__(self):
        # -------------------------------------------------------------------
        # Initialise un dé avec une valeur aléatoire entre 1 et 6.
        #
        # Attributs :
        # - valeur : La valeur actuelle du dé (entre 1 et 6).
        # -------------------------------------------------------------------
        self.valeur = random.randint(1, 6)
