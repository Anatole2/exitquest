import random
import numpy as np

def generate_maze(size, start, end):
    """Génère un labyrinthe avec DFS, les chemins sont d'une case de largeur maximum"""
    grid = np.ones((size, size), dtype=int)  # Grille initiale (tout est un mur)
    visited = np.zeros_like(grid)  # Matrice des cases visitées
    
    def carve_path(x, y):
        """Fonction DFS pour creuser le labyrinthe."""
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Droite, Bas, Gauche, Haut
        random.shuffle(directions)  # Mélange pour ajouter de la variété
        visited[x, y] = 1  # Marquer la cellule comme visitée

        for dx, dy in directions:
            nx, ny = x + dx * 2, y + dy * 2  # Aller deux cases plus loin pour laisser des murs
            if 0 <= nx < size and 0 <= ny < size and visited[nx, ny] == 0:
                grid[x + dx, y + dy] = 0  # Creuser un chemin
                grid[nx, ny] = 0  # Creuser la nouvelle cellule
                carve_path(nx, ny)  # Appel récursif pour continuer

    # Commencer à creuser depuis le point de départ
    carve_path(start[0], start[1])
    
    # S'assurer qu'il y a un chemin entre le départ et la sortie
    grid[start] = 0
    grid[end] = 0

    return grid
