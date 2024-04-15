import pygame
import random


# Initialize the game
pygame.init()


# Creating the screen
screenWidth,screenHeight = 800,600
screen = pygame.display.set_mode((screenWidth,screenHeight))


# Loading Images
gameIconImage = pygame.image.load('./images/logo.png')  # Game Icon
playerImg = pygame.image.load('./images/spaceship.png') # Player
enemyImg = pygame.image.load('./images/ufo.png') # Enemy
bulletImg = pygame.image.load('./images/bullet.png') # Bullet


# Displaying the objects
def player(x,y): screen.blit(playerImg,(x,y))   # Player
def enemy(x,y): screen.blit(enemyImg,(x,y))     # Enemy
def bullet(x,y): screen.blit(bulletImg,(x,y))   # Bullet


# Checking if the bullet collided with the enemy
def isCollision(x1,y1,x2,y2):

    x2+=16
    y2+=16

    x1+=32
    y1+=32

    if ((x1-x2)**2+(y1-y2)**2)**(0.5)<=40:
        return True
    return False

# Title and Icon
pygame.display.set_caption("Space Shooter")
pygame.display.set_icon(gameIconImage) # Game Icon

num_enemies = 6


# Image Dimensions
playerImgX,playerImgY = 64,64
enemyImgX,enemyImgY = 64,64


# Placing player and enemy
playerX,playerY = 400 - (playerImgX//2),480

enemyXs,enemyYs = [],[]
for i in range(num_enemies):
    enemyXs.append(random.randint(50 , 750))
    enemyYs.append(random.randint(20 , 150))

bulletX,bulletY = 0,0


# Direction Variables
movePlayerX,movePlayerY = 0,0
moveEnemyXs,moveEnemyYs = [],[]
for i in range(num_enemies):
    moveEnemyXs.append(1)
    moveEnemyYs.append(1)

moveBulletX,moveBulletY = 0,-1


# Speeds
playerSpeed = 0.5
enemySpeed = 0.5
bulletSpeed = 1


# Bullet state
bulletFired = False

# Score
playerScore = 0
font = pygame.font.Font('freesansbold.ttf',32)

textX = 10
textY = 10

def show_score():
    scoreText = font.render("Score: "+str(playerScore),True,(255,255,255))
    screen.blit(scoreText,(textX,textY))

def show_gameOver():
    gameOverText = font.render("GAME OVER!",True,(255,255,255))
    screen.blit(gameOverText,((screenWidth//2) - 32*4, screenHeight//2))

# Game loop
running = True

# Game Over?
gameOver = False

while running:

    for event in pygame.event.get():
        # For quitting game on pressing colour
        if event.type == pygame.QUIT: running = False

        # For moving the spaceship
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT: movePlayerX = -1
            elif event.key == pygame.K_RIGHT: movePlayerX = 1
            elif event.key == pygame.K_SPACE and bulletFired==False:
                bulletFired = True
                bulletX = playerX+16

        # For stopping the spaceship
        elif event.type == pygame.KEYUP:
            if (event.key == pygame.K_LEFT and movePlayerX==-1) or (event.key == pygame.K_RIGHT and movePlayerX==1): movePlayerX = 0

    # Background Colour
    screen.fill((0,0,50))
    
    # Moving the player
    if (playerX<=screenWidth-playerImgX and movePlayerX==1) or (playerX>=0 and movePlayerX==-1): playerX += movePlayerX*playerSpeed

    # Moving the Enemy
    for i in range(num_enemies):
        print(enemyYs)
        if enemyYs[i]>=440:
            gameOver = True
            break

        if bulletFired and isCollision(enemyXs[i],enemyYs[i],bulletX,bulletY):
            bulletFired = False
            bulletY = playerY-10
            enemyXs[i],enemyYs[i] = random.randint(50 , 750),random.randint(20 , 150)
            playerScore += 1

        elif (enemyXs[i] >= screenWidth - enemyImgX) or (enemyXs[i]<=0):
            enemyYs[i] += 25
            moveEnemyXs[i] *= -1

        enemyXs[i] += moveEnemyXs[i]*enemySpeed
        enemy(enemyXs[i],enemyYs[i])

    # Moving the bullet
    if bulletFired:
        bulletY += moveBulletY*bulletSpeed
        bullet(bulletX,bulletY)
        if (bulletY<=0):
            bulletFired = False
            bulletY = playerY-10

    player(playerX,playerY)

    show_score()
    # For updating the display

    if gameOver == True:
        screen.fill((0,0,0))
        show_gameOver()

    pygame.display.update()