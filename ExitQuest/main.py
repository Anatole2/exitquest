"""
import pygame
import numpy as np
from agent import HybridAgent
from carteGenerateur import carteGenerateur

# Paramètres de la carte
GRID_SIZE = 11  # Taille de la grille (11x11)
CELL_SIZE = 50  # Taille d'une cellule (50 pixels)
WINDOW_SIZE = GRID_SIZE * CELL_SIZE

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Nouveau labyrinthe
labyrinthe = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1],
    [1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1],
    [1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 0, 1, 1, 1, 3, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# Initialisation de Pygame
pygame.init()
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("ExitQuest")

# Point de départ et de sortie
labyrinthe[1][1] = 2  # Départ
labyrinthe[9][9] = 3  # Sortie

def draw_grid(labyrinthe, agent_position, goal):
    # Dessine la grille dans la fenêtre Pygame.
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if labyrinthe[y][x] == 1:  # Mur
                pygame.draw.rect(screen, BLACK, rect)
            elif labyrinthe[y][x] == 2:  # Départ
                pygame.draw.rect(screen, BLUE, rect)
            elif labyrinthe[y][x] == 3:  # Sortie
                pygame.draw.rect(screen, RED, rect)
            elif (y, x) == agent_position:  # Position de l'agent
                pygame.draw.rect(screen, GREEN, rect)  # Agent en vert
            else:  # Chemin
                pygame.draw.rect(screen, WHITE, rect)

def main():
    # Initialisation de l'agent avec la grille
    agent = HybridAgent(np.array(labyrinthe), (9, 9))  # (9, 9) est la sortie
    agent.position = (1, 1)  # Position de départ (1, 1)

    running = True
    clock = pygame.time.Clock()

    while running:
        screen.fill(WHITE)
        draw_grid(labyrinthe, agent.position, (9, 9))  # Afficher le labyrinthe
        
        pygame.display.flip()  # Mise à jour de l'affichage
        pygame.time.delay(300)  # Ralentir légèrement pour bien voir

        print(f"IA visite la case : {agent.position}")

        # Vérifier si l'agent est à la sortie
        if agent.position == (9, 9):
            print("L'agent a atteint la sortie!")
            running = False
            continue

        # Action choisie par l'agent
        action = agent.actionChoisie(*agent.position)
        if action is None:  # Aucun chemin viable
            print("Aucun chemin viable trouvé.")
            running = False
            continue

        # Effectuer une étape
        next_state, reward, done = agent.step(agent.position, action)
        agent.position = next_state  # Mise à jour de la position de l'agent

        screen.fill(WHITE)
        draw_grid(labyrinthe, agent.position, (9, 9))  
        pygame.display.flip()
        pygame.time.delay(300)

        # Gestion des événements Pygame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        clock.tick(10)  # Limite à 10 FPS pour éviter un déplacement trop rapide

    pygame.quit()

if __name__ == "__main__":
    main()
"""

import pygame
import numpy as np
from maze import generate_maze

# Initialisation de Pygame
pygame.init()

# Paramètres du jeu
GRID_SIZE = 10  # Taille du labyrinthe à 10x10
CELL_SIZE = 30  # Taille de chaque cellule
WINDOW_SIZE = GRID_SIZE * CELL_SIZE  # Taille de la fenêtre de jeu
FPS = 30  # Nombre d'images par seconde

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Initialisation de la fenêtre Pygame
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Labyrinthe")

# Définir les positions de départ et d'arrivée
start = (1, 1)  # Début du labyrinthe
end = (9, 9)  # Fin du labyrinthe (position (9, 9) pour la sortie)

# Générer le labyrinthe
maze = generate_maze(GRID_SIZE, start, end)

# Fonction pour dessiner le labyrinthe dans la fenêtre
def draw_maze():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            color = WHITE if maze[row, col] == 0 else BLACK  # 0 = chemin, 1 = mur
            pygame.draw.rect(screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Boucle principale du jeu
running = True
while running:
    screen.fill(BLACK)  # Remplir l'écran en noir

    # Dessiner le labyrinthe
    draw_maze()

    # Dessiner les positions de départ et d'arrivée
    pygame.draw.rect(screen, GREEN, (start[1] * CELL_SIZE, start[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))  # Départ
    pygame.draw.rect(screen, (255, 0, 0), (end[1] * CELL_SIZE, end[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))  # Arrivée

    pygame.display.flip()  # Mettre à jour l'affichage

    # Gestion des événements (quitter, etc.)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Limiter le taux de rafraîchissement
    pygame.time.Clock().tick(FPS)

# Quitter Pygame
pygame.quit()
