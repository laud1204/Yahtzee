from Joueur import Joueur
from Jeu import Jeu


class Partie:
    def __init__(self):
        # Initialisation de la partie avec des joueurs définis par l'utilisateur
        while True:
            try:
                nombre_joueurs = int(input("Combien de joueurs participent à la partie ? "))
                if nombre_joueurs > 0:
                    break
                else:
                    print("Veuillez entrer un nombre supérieur à 0.")
            except ValueError:
                print("Entrée invalide. Veuillez entrer un nombre valide de joueurs.")
        self.joueurs = [Joueur(input(f"Nom du joueur {i + 1}: ")) for i in range(nombre_joueurs)]
        self.jeu = Jeu(self.joueurs)

    def lancer_partie(self):
        for _ in range(13):  # Une partie de Yahtzee dure 13 tours
            print(f"\nTour {_ + 1} sur 13")
            self.jeu.tour()  # Délègue la gestion du tour complet à la classe Jeu

        # Affiche les scores finaux
        self.jeu.afficher_scores()
        print("\nPartie terminée !")

if __name__ == "__main__":
    partie = Partie()
    partie.lancer_partie()
