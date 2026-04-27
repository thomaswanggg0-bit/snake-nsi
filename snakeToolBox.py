import pygame
import random


def deplacer(snake, mvt, Xmax, Ymax):
    # On copie les positions actuelles pour ne pas modifier l'original
    tete = snake['tête'][:]
    corps = [boule[:] for boule in snake['corps']]
    queue = snake['queue'][:]

    # Calcul de la nouvelle position de la tête
    if mvt == 'droite':
        new_tete = [tete[0] + 1, tete[1]]
    elif mvt == 'gauche':
        new_tete = [tete[0] - 1, tete[1]]
    elif mvt == 'haut':
        new_tete = [tete[0], tete[1] - 1]
    elif mvt == 'bas':
        new_tete = [tete[0], tete[1] + 1]
    else:
        return (snake, False)  # pas de mouvement

    # Vérification si le joueur a perdu
    perdu = False
    if new_tete[0] < 0 or new_tete[0] >= Xmax:
        perdu = True
    elif new_tete[1] < 0 or new_tete[1] >= Ymax:
        perdu = True
    elif new_tete in corps:
        perdu = True
    elif new_tete == queue:
        perdu = True

    if perdu:
        return (snake, True)

    # Déplacement : chaque boule prend la place de la précédente
    new_queue = corps[-1][:]
    new_corps = [tete[:]] + [corps[i][:] for i in range(len(corps) - 1)]
    new_snake = {'tête': new_tete, 'corps': new_corps, 'queue': new_queue}

    return (new_snake, False)


def filtrer_mouvement(ancien_mvt, mvt):
    # Dictionnaire des directions opposées
    opposes = {'haut': 'bas', 'bas': 'haut', 'gauche': 'droite', 'droite': 'gauche'}
    # Si le nouveau mouvement est l'opposé de l'ancien, on garde l'ancien
    if ancien_mvt in opposes and opposes[ancien_mvt] == mvt:
        return ancien_mvt
    return mvt


def creerBoule(s, Xmax, Ymax):
    # On liste toutes les cases occupées par le serpent
    positions_serpent = [s['tête']] + s['corps'] + [s['queue']]
    # On cherche une case libre au hasard
    while True:
        x = random.randint(0, Xmax - 1)
        y = random.randint(0, Ymax - 1)
        if [x, y] not in positions_serpent:
            return (x, y)


def avaleBoule(snake, mvt, x, y, Xmax, Ymax):
    tete = snake['tête'][:]
    corps = [boule[:] for boule in snake['corps']]
    queue = snake['queue'][:]

    # Calcul de la nouvelle position de la tête
    if mvt == 'droite':
        new_tete = [tete[0] + 1, tete[1]]
    elif mvt == 'gauche':
        new_tete = [tete[0] - 1, tete[1]]
    elif mvt == 'haut':
        new_tete = [tete[0], tete[1] - 1]
    elif mvt == 'bas':
        new_tete = [tete[0], tete[1] + 1]
    else:
        return (snake, True, False)  # pas de mouvement

    if new_tete == [x, y]:
        # Le serpent avale la boule : il grandit
        # L'ancienne tête est ajoutée au début du corps
        new_corps = [tete[:]] + corps
        new_snake = {'tête': new_tete, 'corps': new_corps, 'queue': queue}

        # Vérification si perdu après avoir mangé
        perdu = False
        if new_tete[0] < 0 or new_tete[0] >= Xmax or new_tete[1] < 0 or new_tete[1] >= Ymax:
            perdu = True
        if new_tete in corps or new_tete == queue:
            perdu = True

        return (new_snake, False, perdu)
    else:
        # Déplacement normal sans manger
        new_snake, perdu = deplacer(snake, mvt, Xmax, Ymax)
        return (new_snake, True, perdu)


def dessinerBoule(t, rayon, surface, couleur):
    # Conversion coordonnées de grille → coordonnées pixels
    x_pixels = t[0] * 2 * rayon + rayon
    y_pixels = t[1] * 2 * rayon + rayon
    pygame.draw.circle(surface, couleur, (x_pixels, y_pixels), rayon, 0)


def dessinerSnake(snake, rayon, surface, coul_tete, coul_corps, coul_queue):
    # On dessine le corps
    for boule in snake['corps']:
        dessinerBoule(boule, rayon, surface, coul_corps)
    # On dessine la queue
    dessinerBoule(snake['queue'], rayon, surface, coul_queue)
    # On dessine la tête par-dessus
    dessinerBoule(snake['tête'], rayon, surface, coul_tete)
