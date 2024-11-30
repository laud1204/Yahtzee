class Tableau:
    # -------------------------------------------------------------------
    # Classe représentant un tableau affichable en console avec des en-têtes
    # et des données, formaté avec des bordures utilisant `|` et `-`.
    #
    # Attributs :
    # - headers : Liste des en-têtes du tableau.
    # - data : Liste de tuples représentant les lignes du tableau.
    # -------------------------------------------------------------------

    def __init__(self, headers, data):
        # -------------------------------------------------------------------
        # Initialise un tableau avec ses en-têtes et ses données.
        #
        # :param headers: Liste des en-têtes du tableau.
        # :param data: Liste de tuples représentant les données du tableau.
        # -------------------------------------------------------------------
        self.headers = headers  # Liste des en-têtes
        self.data = data        # Liste des données (liste de tuples)

    def afficher(self):
        # -------------------------------------------------------------------
        # Affiche le tableau formaté en console avec des bordures et un
        # alignement automatique basé sur la largeur maximale de chaque colonne.
        # -------------------------------------------------------------------

        # Calcul de la largeur maximale pour chaque colonne
        col_widths = [max(len(str(item)) for item in col) for col in zip(self.headers, *self.data)]

        # Génération de la ligne de séparation (horizontale)
        ligne_separation = "+".join("-" * (width + 2) for width in col_widths)

        # Génération de la ligne contenant les en-têtes
        ligne_headers = "|".join(f" {self.headers[i].ljust(col_widths[i])} " for i in range(len(self.headers)))

        # Génération des lignes contenant les données
        lignes_data = [
            "|".join(f" {str(row[i]).ljust(col_widths[i])} " for i in range(len(row)))
            for row in self.data
        ]

        # Affichage complet du tableau
        print(f"+{ligne_separation}+")         # Ligne de séparation supérieure
        print(f"|{ligne_headers}|")            # Ligne des en-têtes
        print(f"+{ligne_separation}+")         # Ligne de séparation entre en-têtes et données
        for ligne in lignes_data:
            print(f"|{ligne}|")                # Lignes des données
        print(f"+{ligne_separation}+")         # Ligne de séparation inférieure
