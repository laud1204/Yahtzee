class Tableau:
    def __init__(self, headers, data):
        self.headers = headers  # Liste des en-têtes
        self.data = data        # Liste des données (liste de tuples)

    def afficher(self):
        # Calcul de la largeur de chaque colonne en fonction des données et des en-têtes
        col_widths = [max(len(str(item)) for item in col) for col in zip(self.headers, *self.data)]

        # Génère la ligne de séparation
        ligne_separation = "+".join("-" * (width + 2) for width in col_widths)

        # Génère la ligne des en-têtes
        ligne_headers = "|".join(f" {self.headers[i].ljust(col_widths[i])} " for i in range(len(self.headers)))

        # Génère les lignes des données
        lignes_data = [
            "|".join(f" {str(row[i]).ljust(col_widths[i])} " for i in range(len(row)))
            for row in self.data
        ]

        # Affichage du tableau
        print(f"+{ligne_separation}+")
        print(f"|{ligne_headers}|")
        print(f"+{ligne_separation}+")
        for ligne in lignes_data:
            print(f"|{ligne}|")
        print(f"+{ligne_separation}+")
