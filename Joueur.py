from FeuilleScore import FeuilleScore  # Supposons que la classe FeuilleScore soit définie dans un fichier séparé

class Joueur:
    def __init__(self, nom: str):
        self.nom = nom  # Nom du joueur
        self.score = {}  # Dictionnaire pour stocker les scores par figure
        self.feuille_score = FeuilleScore()  # Feuille de score associée au joueur