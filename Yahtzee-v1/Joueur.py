from FeuilleScore import FeuilleScore


class Joueur:
    # -------------------------------------------------------------------
    # Classe représentant un joueur dans une partie de Yahtzee.
    #
    # Attributs :
    # - nom : Nom du joueur.
    # - score : Dictionnaire contenant les scores du joueur par figure.
    # - feuille_score : Feuille de score associée au joueur.
    # -------------------------------------------------------------------

    def __init__(self, nom: str):
        # -------------------------------------------------------------------
        # Initialise un joueur avec un nom, un dictionnaire de scores vide,
        # et une feuille de score.
        #
        # :param nom: Nom du joueur.
        # -------------------------------------------------------------------
        self.nom = nom  # Nom du joueur
        self.score = {}  # Dictionnaire pour stocker les scores par figure
        self.feuille_score = FeuilleScore()  # Feuille de score associée au joueur
