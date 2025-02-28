import numpy as np
import csv
import os

class carteGenerateur:
    def __init__(self, size=10, output_dir="cartes_csv"):
        self.size = size
        self.output_dir = output_dir

        # Crée le dossier de sortie s'il n'existe pas
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def generate_grid(self):
        grid = np.zeros((self.size, self.size), dtype=int)
        for _ in range(self.size * 2):  # Ajouter des obstacles
            x, y = np.random.randint(0, self.size, 2)
            if (x, y) not in [(0, 0), (self.size - 1, self.size - 1)]:
                grid[x, y] = 1  # 1 = obstacle
        grid[0, 0] = 2  # Départ
        grid[-1, -1] = 3  # Sortie
        return grid

    def save_grid_to_csv(self, grid, filename="grid.csv"):
        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            for row in grid:
                writer.writerow(row)
        print(f"Grille sauvegardée dans : {filepath}")