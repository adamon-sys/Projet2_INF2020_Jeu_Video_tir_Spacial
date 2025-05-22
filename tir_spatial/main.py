import random
import pygame
import sys

# Initialiser Pygame
pygame.init()

# Dimensions de la fenêtre
LARGEUR = 1300
HAUTEUR = 1000

# Vaisseau
vaisseau_largeur = 50
vaisseau_hauteur = 30

# Ennemis
largeur_ennemi = 40
hauteur_ennemi = 30

etoiles = []

# Créer des étoiles aléatoires
for _ in range(100):
    x = random.randint(0, LARGEUR)
    y = random.randint(0, HAUTEUR)
    rayon = random.randint(1, 3)
    vitesse = random.uniform(0.5, 1.5)
    etoiles.append([x, y, rayon, vitesse])


# Charger les sons
son_tir = pygame.mixer.Sound("tir_spatial/assets/sounds/tir.wav")
son_explosion = pygame.mixer.Sound("tir_spatial/assets/sounds/explosion.wav")

# Couleurs
NOIR = (0, 0, 0)

# Projectiles
projectiles = []
largeur_projectile = 5
hauteur_projectile = 10
vitesse_projectile = 7

# Ennemis
ennemis = []
MAX_ENNEMIS = 3
vitesse_ennemi = 2
frequence_ennemis = 60
frame_count = 0
score = 0
game_over = False
demarrage = True

# Créer la fenêtre
fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Jeu de tir spatial")

# Charger les images (après définition des tailles)

# 👤 Le joueur (le char au sol)
image_char = pygame.image.load("tir_spatial/assets/images/char.png").convert_alpha()

# 👾 Les ennemis (les vaisseaux qui descendent)
image_vaisseau_ennemi = pygame.image.load("tir_spatial/assets/images/vaisseau.png").convert_alpha()

image_char = pygame.transform.scale(image_char, (vaisseau_largeur, vaisseau_hauteur))
image_vaisseau_ennemi = pygame.transform.scale(image_vaisseau_ennemi, (largeur_ennemi, hauteur_ennemi))

# Position initiale du vaisseau
vaisseau_x = LARGEUR // 2 - vaisseau_largeur // 2
vaisseau_y = HAUTEUR - 60
vitesse = 5

# Boucle principale
clock = pygame.time.Clock()
en_cours = True

def reinitialiser_jeu():
    global vaisseau_x, ennemis, projectiles, score, frame_count, game_over
    vaisseau_x = LARGEUR // 2 - vaisseau_largeur // 2
    ennemis = []
    projectiles = []
    score = 0
    frame_count = 0
    game_over = False

while en_cours:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            en_cours = False
        elif event.type == pygame.KEYDOWN:
            if demarrage and event.key == pygame.K_RETURN:
                demarrage = False
            elif game_over and event.key == pygame.K_RETURN:
                reinitialiser_jeu()
                continue

    if demarrage:
        fenetre.fill(NOIR)
        font_accueil = pygame.font.SysFont(None, 72)
        texte_titre = font_accueil.render("JEU DE TIR SPATIAL", True, (0, 200, 255))
        fenetre.blit(texte_titre, (LARGEUR // 2 - 280, HAUTEUR // 2 - 100))

        font_start = pygame.font.SysFont(None, 36)
        texte_start = font_start.render("Appuyez sur ENTRÉE pour commencer", True, (255, 255, 255))
        fenetre.blit(texte_start, (LARGEUR // 2 - 220, HAUTEUR // 2))
        pygame.display.flip()
        continue

    if not game_over:
        frame_count += 1

        # Faire défiler les étoiles
        for e in etoiles:
            e[1] += e[3]
            if e[1] > HAUTEUR:
                e[1] = 0
                e[0] = random.randint(0, LARGEUR)

        # Gérer les touches
        touches = pygame.key.get_pressed()
        if touches[pygame.K_LEFT] and vaisseau_x > 0:
            vaisseau_x -= vitesse
        if touches[pygame.K_RIGHT] and vaisseau_x < LARGEUR - vaisseau_largeur:
            vaisseau_x += vitesse
        if touches[pygame.K_SPACE]:
            projectile_x = vaisseau_x + vaisseau_largeur // 2 - largeur_projectile // 2
            projectile_y = vaisseau_y
            projectiles.append([projectile_x, projectile_y])
            son_tir.play()
        
        # ... (reste inchangé)


        if frame_count % frequence_ennemis == 0 and len(ennemis) < MAX_ENNEMIS:
            ennemi_x = random.randint(0, LARGEUR - largeur_ennemi)
            ennemi_y = -hauteur_ennemi
            ennemi_vitesse = random.randint(1, 3)
            ennemis.append([ennemi_x, ennemi_y, ennemi_vitesse])

        for e in ennemis:
            e[1] += e[2]
            if e[1] + hauteur_ennemi >= HAUTEUR:
                game_over = True

        ennemis = [e for e in ennemis if e[1] < HAUTEUR]

        for p in projectiles:
            p[1] -= vitesse_projectile

        projectiles = [p for p in projectiles if p[1] > 0]

        ennemis_a_supprimer = []
        projectiles_a_supprimer = []
        for e in ennemis:
            ennemi_rect = pygame.Rect(e[0], e[1], largeur_ennemi, hauteur_ennemi)
            for p in projectiles:
                projectile_rect = pygame.Rect(p[0], p[1], largeur_projectile, hauteur_projectile)
                if ennemi_rect.colliderect(projectile_rect):
                    ennemis_a_supprimer.append(e)
                    projectiles_a_supprimer.append(p)
                    score += 1
                    son_explosion.play()

        for e in ennemis_a_supprimer:
            if e in ennemis:
                ennemis.remove(e)
        for p in projectiles_a_supprimer:
            if p in projectiles:
                projectiles.remove(p)

    # Affichage
    fenetre.fill(NOIR)
    for e in etoiles:
        pygame.draw.circle(fenetre, (255, 255, 255), (int(e[0]), int(e[1])), e[2])

    fenetre.blit(image_char, (vaisseau_x, vaisseau_y))

    for p in projectiles:
        pygame.draw.rect(fenetre, (255, 255, 0), (p[0], p[1], largeur_projectile, hauteur_projectile))

    for e in ennemis:
        fenetre.blit(image_vaisseau_ennemi, (e[0], e[1]))

    font = pygame.font.SysFont(None, 36)
    texte_score = font.render(f"Score : {score}", True, (255, 255, 0))
    fenetre.blit(texte_score, (10, 10))

    if game_over:
        font_game_over = pygame.font.SysFont(None, 72)
        texte_game_over = font_game_over.render("GAME OVER", True, (255, 0, 0))
        fenetre.blit(texte_game_over, (LARGEUR // 2 - 180, HAUTEUR // 2 - 60))

        font_rejouer = pygame.font.SysFont(None, 36)
        texte_rejouer = font_rejouer.render("Appuyez sur ENTRÉE pour rejouer", True, (255, 255, 255))
        fenetre.blit(texte_rejouer, (LARGEUR // 2 - 200, HAUTEUR // 2 + 10))

    pygame.display.flip()

# Quitter le jeu
pygame.quit()
sys.exit()
