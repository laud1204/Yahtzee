from CalculateurDeScore import CalculateurDeScore
from Tableau import Tableau


class FeuilleScore:
    def __init__(self):
        # Initialisation des scores avec None, ce qui signifie que la figure n'a pas encore été remplie
        self.scores = {
            '1': None,
            '2': None,
            '3': None,
            '4': None,
            '5': None,
            '6': None,
            'Brelan': None,
            'Carré': None,
            'Full': None,
            'Petite Suite': None,
            'Grande Suite': None,
            'Yahtzee': None,
            'Chance': None,
            'Bonus Section Supérieure': 0  # Bonus initialisé à 0
        }
        self.remplissage = {key: False for key in self.scores}  # Pour savoir si la figure est remplie ou non
        self.des = []  # Liste des valeurs des dés actuels

    def noter_score(self, figure: str, valeur: int) -> None:
        """
        Note le score pour une figure donnée. Si la figure appartient à la section supérieure,
        vérifie si le bonus de la section supérieure est atteint.
        """
        if figure in self.scores and self.scores[figure] is None:
            self.scores[figure] = valeur
            self.remplissage[figure] = True
            print(f"Score de {valeur} noté pour la figure {figure}")

            # Vérifie si la figure est dans la section supérieure
            if figure in ['1', '2', '3', '4', '5', '6']:
                if self.verifier_bonus_section_superieure():
                    print("Félicitations ! Vous avez atteint le bonus de la section supérieure (+35 points)")
        else:
            print(f"Figure {figure} déjà remplie ou inexistante")

    def afficher_score(self, des: list[int]) -> None:
        """
        Affiche le tableau des scores réalisés et des scores théoriques en utilisant la classe Tableau.
        """
        self.des = des  # Met à jour les dés actuels

        # Exclut "Bonus Section Supérieure" des figures pour le calcul des scores théoriques
        scores_theoriques = {
            figure: self.calculer_score(figure, des)
            for figure in self.scores.keys()
            if figure != "Bonus Section Supérieure"
        }

        # Calcul du score global réalisé
        total_score = sum(score for score in self.scores.values() if score is not None)

        # Prépare les données pour le tableau
        figures_tableau = [
            (
                figure,
                self.scores[figure] if self.scores[figure] is not None else "Non réalisée",
                scores_theoriques.get(figure, "N/A")  # Valeur par défaut si pas de score théorique
            )
            for figure in self.scores.keys()
        ]

        # Utilise la classe Tableau pour afficher les scores
        tableau = Tableau(headers=["Figure", "Score réalisé", "Score théorique"], data=figures_tableau)
        print("\nTableau des scores :")
        tableau.afficher()

        # Affiche le score global réalisé
        print(f"Score global réalisé : {total_score}")

    def verifier_bonus_section_superieure(self) -> bool:
        # Vérifie si le joueur a atteint le bonus de la section supérieure
        section_sup_score = sum(self.scores[str(i)] for i in range(1, 7) if self.scores[str(i)] is not None)
        if section_sup_score >= 63:
            self.scores['Bonus section supérieure'] = 35
            return True
        return False

    def calculer_score(self, figure: str, des: list[int]) -> int:
        calculateur = CalculateurDeScore()
        if figure == '1':
            return calculateur.calculer_un(des)
        elif figure == '2':
            return calculateur.calculer_deux(des)
        elif figure == '3':
            return calculateur.calculer_trois(des)
        elif figure == '4':
            return calculateur.calculer_quatre(des)
        elif figure == '5':
            return calculateur.calculer_cinq(des)
        elif figure == '6':
            return calculateur.calculer_six(des)
        elif figure == 'Brelan':
            return calculateur.calculer_brelan(des)
        elif figure == 'Carré':
            return calculateur.calculer_carre(des)
        elif figure == 'Full':
            return calculateur.calculer_full(des)
        elif figure == 'Petite Suite':
            return calculateur.calculer_petite_suite(des)
        elif figure == 'Grande Suite':
            return calculateur.calculer_grande_suite(des)
        elif figure == 'Yahtzee':
            return calculateur.calculer_yahtzee(des)
        elif figure == 'Chance':
            return calculateur.calculer_chance(des)
        else:
            raise ValueError(f"Figure inconnue : {figure}")