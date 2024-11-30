from De import De
from Joueur import Joueur

class Jeu:

    FIGURES_VALIDES = ['Brelan', 'Carré', 'Full', 'Petite Suite', 'Grande Suite', 'Yahtzee', 'Chance', '1', '2', '3', '4', '5', '6']

    def __init__(self, joueurs: list):
        self.joueurs = joueurs  # Liste des joueurs participant au jeu
        self.des = [De() for _ in range(5)]  # Initialisation des dés
        self.tour_actuel = 0  # Tour actuel du jeu

    def lancer_des(self, des_a_relancer: list[int]) -> list[int]:
        """Lance les dés spécifiés par leurs indices."""
        for i in des_a_relancer:
            if 0 <= i < len(self.des):
                self.des[i].__init__()
        return [de.valeur for de in self.des]

    def effectuer_premier_lancer(self):
        """Effectue le premier lancer avec tous les dés."""
        return self.lancer_des(list(range(5)))

    def effectuer_relancers(self) -> list[int]:
        """Permet au joueur de relancer les dés s'il le souhaite."""
        lancers_restants = 2
        while lancers_restants > 0:
            choix = input("Voulez-vous relancer des dés ? (oui/non) ").strip().lower()
            if choix == 'non':
                break
            elif choix == 'oui':
                des_a_relancer = self.demander_des_a_relancer()
                self.lancer_des([i - 1 for i in des_a_relancer])
                print(f"Résultat des dés: {[de.valeur for de in self.des]}")
                lancers_restants -= 1
            else:
                print("Veuillez répondre par 'oui' ou 'non'.")
        return [de.valeur for de in self.des]

    def demander_des_a_relancer(self) -> list[int]:
        """Demande au joueur quels dés relancer."""
        while True:
            try:
                des_a_relancer = [int(i) for i in input(
                    "Quels dés voulez-vous relancer (1-5, séparés par des espaces) ? ").split()]
                if all(1 <= i <= 5 for i in des_a_relancer):
                    return list(set(des_a_relancer))  # Supprime les doublons
                else:
                    print("Veuillez entrer des indices valides entre 1 et 5.")
            except ValueError:
                print("Entrée invalide. Veuillez entrer des numéros de dés valides (1-5, séparés par des espaces).")

    def choisir_figure(self, joueur: Joueur, des_actuels: list[int]):
        """Permet au joueur de choisir une figure à remplir ou rayer."""
        while True:
            figure = input("Quelle figure voulez-vous remplir ou rayer ? ").strip()
            if figure in self.FIGURES_VALIDES:
                if joueur.feuille_score.scores[figure] is None:
                    score = joueur.feuille_score.calculer_score(figure, des_actuels)
                    joueur.feuille_score.noter_score(figure, score)
                    joueur.feuille_score.afficher_score(des_actuels)
                    break
                else:
                    print("Cette figure est déjà remplie. Veuillez en choisir une autre.")
            else:
                print(f"Figure invalide : {figure}. Veuillez entrer une figure valide.")

    def gerer_tour_joueur(self, joueur: Joueur):
        """Gère un tour complet pour un joueur."""
        print(f"\nTour de {joueur.nom}")
        des_actuels = self.effectuer_premier_lancer()
        print(f"Résultat des dés: {des_actuels}")
        des_actuels = self.effectuer_relancers()
        print(f"Résultat final des dés: {des_actuels}")
        joueur.feuille_score.afficher_score(des_actuels)
        self.choisir_figure(joueur, des_actuels)

    def tour(self):
        """Gère un tour complet pour tous les joueurs."""
        for joueur in self.joueurs:
            self.gerer_tour_joueur(joueur)
        self.tour_actuel += 1

    def afficher_scores(self):
        """Affiche les scores de tous les joueurs."""
        print("\nScores actuels des joueurs :")
        for joueur in self.joueurs:
            score_total = sum(score for score in joueur.feuille_score.scores.values() if score is not None)
            print(f"{joueur.nom} : {score_total}")