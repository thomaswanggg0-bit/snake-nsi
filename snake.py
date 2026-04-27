import pygame, sys
from pygame.locals import *
import snakeToolBox

pygame.init()

# --- Constantes ---
Xmax = 30
Ymax = 21
RAYON = 10
LARGEUR = Xmax * 2 * RAYON   # 600 pixels
HAUTEUR = Ymax * 2 * RAYON   # 420 pixels

NOIR         = (0, 0, 0)
BLANC        = (255, 255, 255)
ROUGE        = (255, 0, 0)
VERT         = (0, 200, 0)
BLEU         = (0, 0, 255)
ROSE         = (255, 0, 255)

COULEUR_FOND    = NOIR
COUL_TETE       = ROUGE
COUL_CORPS      = VERT
COUL_QUEUE      = BLEU
COUL_NOURRITURE = ROSE

IPS = 10

# --- Création de la fenêtre ---
ipsHorloge = pygame.time.Clock()
surface_affichage = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption('Snake')

# --- Boucle qui permet de rejouer ---
jouer = True
while jouer:

    # Initialisation du serpent et des variables du jeu
    snake = {'tête': [0, 0], 'corps': [[0, 1]], 'queue': [0, 2]}
    mvt = ''
    score = 0
    boule = snakeToolBox.creerBoule(snake, Xmax, Ymax)

    # --- Boucle principale du jeu ---
    perdu = False
    while not perdu:
        surface_affichage.fill(COULEUR_FOND)

        # Gestion des événements
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_RIGHT:
                    mvt = snakeToolBox.filtrer_mouvement(mvt, 'droite')
                elif event.key == K_LEFT:
                    mvt = snakeToolBox.filtrer_mouvement(mvt, 'gauche')
                elif event.key == K_UP:
                    mvt = snakeToolBox.filtrer_mouvement(mvt, 'haut')
                elif event.key == K_DOWN:
                    mvt = snakeToolBox.filtrer_mouvement(mvt, 'bas')

        # Déplacement du serpent ou avalement de la boule de nourriture
        snake, bouleExiste, perdu = snakeToolBox.avaleBoule(
            snake, mvt, boule[0], boule[1], Xmax, Ymax
        )

        # Si la boule a été avalée, on crée une nouvelle boule et on augmente le score
        if not bouleExiste:
            score += 1
            pygame.display.set_caption('Snake - Score : ' + str(score))
            boule = snakeToolBox.creerBoule(snake, Xmax, Ymax)

        # Dessin du serpent et de la boule de nourriture
        snakeToolBox.dessinerSnake(snake, RAYON, surface_affichage,
                                   COUL_TETE, COUL_CORPS, COUL_QUEUE)
        snakeToolBox.dessinerBoule(boule, RAYON, surface_affichage, COUL_NOURRITURE)

        # Mise à jour de l'affichage
        pygame.display.update()
        ipsHorloge.tick(IPS)

    # --- Écran de résultat ---
    surface_affichage.fill(NOIR)
    police = pygame.font.SysFont(None, 64)

    texte_perdu   = police.render('PERDU !', True, ROUGE)
    texte_score   = police.render('Score : ' + str(score), True, BLANC)
    texte_rejouer = police.render('ESPACE = Rejouer    ECHAP = Quitter', True, BLANC)

    surface_affichage.blit(texte_perdu,
        (LARGEUR // 2 - texte_perdu.get_width() // 2, HAUTEUR // 2 - 80))
    surface_affichage.blit(texte_score,
        (LARGEUR // 2 - texte_score.get_width() // 2, HAUTEUR // 2 - 10))
    surface_affichage.blit(texte_rejouer,
        (LARGEUR // 2 - texte_rejouer.get_width() // 2, HAUTEUR // 2 + 60))

    pygame.display.update()

    # On attend le choix du joueur
    choix_fait = False
    while not choix_fait:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    choix_fait = True
                    jouer = True
                elif event.key == K_ESCAPE:
                    choix_fait = True
                    jouer = False

pygame.quit()
sys.exit()
