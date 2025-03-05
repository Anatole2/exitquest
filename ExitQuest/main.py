import pygame
import numpy as np
from agent import HybridAgent
from carteGenerateur import carteGenerateur

# Paramètres de la carte
GRID_SIZE = 10  # Taille de la grille (10x10)
CELL_SIZE = 50  # Taille d'une cellule (50 pixels)
WINDOW_SIZE = GRID_SIZE * CELL_SIZE

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Génération de la grille
def generate_grid(size):
    grid = np.zeros((size, size), dtype=int)
    for _ in range(size * 2):  # Ajout d'obstacles
        x, y = np.random.randint(0, size, size=2)
        if (x, y) != (0, 0) and (x, y) != (size - 1, size - 1):
            grid[x, y] = 1
    return grid

# Initialisation de Pygame
pygame.init()
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("ExitQuest")

def draw_grid(grid, agent_position, goal):
    """Dessine la grille dans la fenêtre Pygame."""
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            rect = pygame.Rect(y * CELL_SIZE, x * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if grid[x, y] == 1:  # Obstacle
                pygame.draw.rect(screen, BLACK, rect)
            elif (x, y) == goal:  # Sortie
                pygame.draw.rect(screen, GREEN, rect)
            elif (x, y) == agent_position:  # Position de l'agent
                pygame.draw.rect(screen, BLUE, rect)
            else:  # Cellule vide
                pygame.draw.rect(screen, WHITE, rect, 1)

def main():
    # Crée une instance de générateur de cartes
    generator = carteGenerateur(size=10, output_dir="cartes_csv")
    # Générer la grille
    grid = generate_grid(GRID_SIZE)
    goal = (GRID_SIZE - 1, GRID_SIZE - 1)  # Sortie en bas à droite
    grid[goal] = 3  # Identifier la sortie dans la grille

    # Sauvegarde la grille dans un fichier CSV
    generator.save_grid_to_csv(grid, filename="grille_aleatoire.csv")

    # Initialisation de l'agent
    agent = HybridAgent(grid, goal)
    
    print("Début de l'entraînement de l'agent...")
    agent.train(episodes=1500)  # Ajustez le nombre d'épisodes si nécessaire
    print("Entraînement terminé.\n")

    running = True
    clock = pygame.time.Clock()

    while running:
        screen.fill(WHITE)
        draw_grid(grid, agent.position, goal)
        pygame.display.flip()
        pygame.time.delay(500)  # Pause pour observer les mouvements

        # Vérifier si l'agent est à la sortie
        if agent.position == goal:
            print("L'agent a atteint la sortie!")
            running = False
            continue

        # Action choisie par l'agent
        action = agent.actionChoisie(*agent.position)
        if action is None:  # Aucun chemin viable
            print("Aucun chemin viable trouvé. Affichage de la carte pendant 5 secondes.")
            pygame.time.wait(5000)
            running = False
            continue

        # Effectuer une étape
        next_state, reward, done = agent.step(agent.position, action)
        agent.position = next_state

        # Gestion des événements Pygame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()

if __name__ == "__main__":
    main()
