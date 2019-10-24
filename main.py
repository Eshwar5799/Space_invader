import pygame
import random
import math
from pygame import mixer

# Initialization
pygame.init()

# Background
background = pygame.image.load("background.png")

# Screen
screen = pygame.display.set_mode((800, 600))
# Background music
mixer.music.load('background.wav')
mixer.music.play(-1)
# title and icon
pygame.display.set_caption("Space invaders")
icon = pygame.image.load("player.png")
pygame.display.set_icon(icon)
# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# Game_over font
over_font = pygame.font.Font('freesansbold.ttf', 64)


# Show the score
def show(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


# Game over
def game_over_text(x, y):
    over_score = font.render("GAME OVER,FINAL SCORE :" + str(score_value), True, (255, 255, 255))
    screen.blit(over_score, (x, y))


# Player
playerImg = pygame.image.load("player.png")
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(0, 800))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(2)
    enemyY_change.append(40)

# Bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bullet_state = 'ready'
bulletX_change = 0
bulletY_change = 10


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, a):
    screen.blit(enemyImg[a], (x, y))


def is_collision(x1, y1, x2, y2):
    distance = math.sqrt((math.pow(x1 - x2, 2)) + (math.pow(y1 - y2, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                # print("left arrow pressed")
                playerX_change = -2
            if event.key == pygame.K_RIGHT:
                # print("right arrow pressed")
                playerX_change = 2
            if event.key == pygame.K_UP:
                # print("up arrow is pressed")
                playerY_change = -2
            if event.key == pygame.K_DOWN:
                # print("down arrow is pressed")
                playerY_change = 2

            if event.key == pygame.K_SPACE:
                # print("space is pressed")
                bullet_sound = mixer.Sound('laser.wav')
                bullet_sound.play()
                if bullet_state == 'ready':
                    bulletX = playerX
                    fire_bullet(playerX, playerY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or \
                    event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                # print("Keystroke arrow released!!")
                playerX_change = 0  # otherwise it will keep moving along X-coordinates
                playerY_change = 0  # otherwise it will keep moving along y-coordinates

    screen.fill((0, 0, 0))  # RGB
    screen.blit(background, (0, 0))
    # Boundary restrictions for X-coordinate
    if playerX <= 0:
        playerX = 0
    elif playerX >= 720:
        playerX = 720

    # Boundary restrictions for Y-coordinate
    if playerY <= 300:
        playerY = 300
    elif playerY >= 500:
        playerY = 500

    if bulletY <= 0:
        bulletY = 480
        bulletY_state = "ready"

    if bullet_state is "fire":
        fire_bullet(playerX, bulletY)
        bulletY -= bulletY_change
    playerX += playerX_change  # changes will be reflected in playerX coordinates
    playerY += playerY_change  # changes will be reflected in playerY coordinates
    # enemy movement
    for i in range(num_of_enemies):
        if enemyY[i] > 430:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text(200, 200)
            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 2
            enemyY[i] += enemyY_change[i]
        if enemyX[i] >= 720:
            enemyX_change[i] = -2
            enemyY[i] += enemyY_change[i]

        collision = is_collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = 'ready'
            score_value += 1
            print(score_value)
            enemyX[i] = random.randint(0, 800)
            enemyY[i] = random.randint(50, 135)

        enemy(enemyX[i], enemyY[i], i)

    player(playerX, playerY)
    show(textX, textY)
    pygame.display.update()
