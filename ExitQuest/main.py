""" L'agent trouve la sortie dans un labyrinthe :
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
from environment import Environment
from agent import HybridAgent

# Initialisation Pygame
pygame.init()

# Paramètres
GRID_SIZE = 10
CELL_SIZE = 50
WINDOW_SIZE = GRID_SIZE * CELL_SIZE
FPS = 10

# Départ et arrivée
start, end = (1, 1), (9, 9)

# Génération labyrinthe
maze = generate_maze(GRID_SIZE, start=start, end=end)
maze[start] = 2
maze[end] = 3

# Environnement visuel
env = Environment(maze, CELL_SIZE)

# Initialisation agent
agent = HybridAgent(grid=maze, goal=end)

# Entrainement rapide
agent.train(episodes=50)

# Position initiale agent
state = start
running = True

# Boucle principale
while running:
    pygame.event.pump()

    # Effacer traces (aucune trace visible)
    maze[maze == 4] = 0

    # Affichage position actuelle
    print(f"Position actuelle agent : {state}")

    # Rendu graphique
    env.render()

    # Affichage agent (en jaune)
    x, y = state
    pygame.draw.rect(env.window, (255, 255, 0), 
                     (y * CELL_SIZE, x * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.display.flip()

    # Vérifier arrivée à la sortie
    if state == end:
        print("✅ Agent a atteint la sortie !")
        running = False
        continue

    # Action suivante
    next_action = agent.actionChoisie(*state)
    if next_action is None:
        print("❌ Agent bloqué, aucun chemin disponible.")
        break

    # Mise à jour position
    state = next_action

    pygame.time.wait(200)

# Fin de simulation
print("Simulation terminée. Fermeture dans 1 seconde.")
pygame.time.wait(1000)
pygame.quit()