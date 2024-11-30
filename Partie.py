from Joueur import Joueur
from Jeu import Jeu


class Partie:
    # -------------------------------------------------------------------
    # Classe représentant une partie complète de Yahtzee.
    #
    # Attributs :
    # - joueurs : Liste des joueurs participant à la partie.
    # - jeu : Instance de la classe Jeu gérant le déroulement des tours.
    # -------------------------------------------------------------------

    def __init__(self):
        # -------------------------------------------------------------------
        # Initialise une nouvelle partie en demandant le nombre de joueurs
        # et leurs noms. Chaque joueur est associé à une feuille de score.
        # -------------------------------------------------------------------
        while True:
            try:
                # Demande le nombre de joueurs
                nombre_joueurs = int(input("Combien de joueurs participent à la partie ? "))
                if nombre_joueurs > 0:
                    break
                else:
                    print("Veuillez entrer un nombre supérieur à 0.")
            except ValueError:
                print("Entrée invalide. Veuillez entrer un nombre valide de joueurs.")

        # Création de la liste des joueurs
        self.joueurs = [Joueur(input(f"Nom du joueur {i + 1}: ")) for i in range(nombre_joueurs)]
        # Initialisation du jeu avec les joueurs
        self.jeu = Jeu(self.joueurs)

    def lancer_partie(self):
        # -------------------------------------------------------------------
        # Gère le déroulement complet de la partie, composée de 13 tours.
        #
        # Chaque tour est géré par l'objet Jeu, et les scores finaux sont
        # affichés à la fin de la partie.
        # -------------------------------------------------------------------
        for _ in range(13):  # Une partie de Yahtzee dure 13 tours
            print(f"\nTour {_ + 1} sur 13")
            # Appelle la méthode tour de la classe Jeu pour gérer le tour
            self.jeu.tour()

        # Affiche les scores finaux des joueurs
        self.jeu.afficher_scores()
        print("\nPartie terminée !")


# Point d'entrée principal de l'application
if __name__ == "__main__":
    # -------------------------------------------------------------------
    # Initialise et lance une partie de Yahtzee.
    # -------------------------------------------------------------------
    partie = Partie()
    partie.lancer_partie()
