import pygame
import random
import math
from pygame import mixer

# Initialize the pygame
pygame.init()

# Create screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('background.png')

# Background Sound (-1 = Looped Music)
mixer.music.load('background.wav')
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Player (Remember Image Size)
playerImage = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImage = []
enemyX = []
enemyY = []
enemy_changeX = []
enemy_changeY = []
numOfEnemies = 6

for i in range(numOfEnemies):
    enemyImage.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemy_changeX.append(3)
    enemy_changeY.append(40)

# Laser

# Ready - You can't see the laser on the screen
# Fire - The laser is moving
laserImage = pygame.image.load('laser.png')
laserX = 0
laserY = 480
laser_changeY = 10
laser_state = "ready"

# Score
scoreValue = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# Game Over Text
overFont = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("Score: " + str(scoreValue), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    overText = overFont.render("GAME OVER", True, (255, 255, 255))
    screen.blit(overText, (200, 250))


# Blit = Create/Draw
def player(x, y):
    screen.blit(playerImage, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImage[i], (x, y))


def fire_laser(x, y):
    global laser_state
    laser_state = "fire"
    screen.blit(laserImage, (x + 16, y + 10))


def isCollision(enemyX, enemyY, laserX, laserY):
    distance = math.sqrt((math.pow(enemyX - laserX, 2)) + (math.pow(enemyY - laserY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True
while running:

    # RGB - Red, Green, and Blue
    screen.fill((0, 0, 0))

    # Background Image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # If keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if laser_state == "ready":
                    laserSound = mixer.Sound('laser.wav')
                    laserSound.play()
                    # Get the current x cords of the spaceship
                    laserX = playerX
                    fire_laser(laserX, laserY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    #  5 = 5 + -0.1 -> 5 = 5 - 0.1
    #  5 = 5 + 0.1 -> 5 = 5 + 0.1
    playerX += playerX_change

    # Checking for boundaries of spaceship so it doesn't go out of the screen
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy Movement

    for i in range(numOfEnemies):

        # Game Over
        if enemyY[i] > 440:
            for j in range(numOfEnemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemy_changeX[i]
        if enemyX[i] <= 0:
            enemy_changeX[i] = 3
            enemyY[i] += enemy_changeY[i]
        elif enemyX[i] >= 736:
            enemy_changeX[i] = -3
            enemyY[i] += enemy_changeY[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], laserX, laserY)
        if collision:
            explosionSound = mixer.Sound('explosion.wav')
            explosionSound.play()
            laserY = 480
            laser_state = "ready"
            scoreValue += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet Movement
    if laserY <= 0:
        laserY = 480
        laser_state = "ready"

    if laser_state == "fire":
        fire_laser(laserX, laserY)
        laserY -= laser_changeY

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
