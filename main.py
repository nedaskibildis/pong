# Import necessary modules
from operator import truediv
from time import sleep
import pygame

# Initialize pygame
pygame.init()

# Set up the screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

# Define colors
white = (255, 255, 255)
black = (0, 0, 0)

# Set up some game parameters
pixel = 64
ballVelocity = 2
playerVelocity = 4
p1Score = 0
p2Score = 0

# Lists to hold the direction of the ball
YDirection = [-1]
XDirection = [-1]

# Set up the game clock
clock = pygame.time.Clock()

# Create the game screen and font
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
font = pygame.font.SysFont("retrogaming", 36)

# Define the initial game state
game_state = "start_menu"

# Function to draw the start menu
def drawStartMenu():
    screen.fill((0, 0, 0))
    font = pygame.font.SysFont('retrogaming', 40)
    title = font.render('PONG', True, white)
    start_button = font.render('Press Space To Start', True, white)
    screen.blit(title, (SCREEN_WIDTH/2 - title.get_width()/2, SCREEN_HEIGHT - 600))
    screen.blit(start_button, (SCREEN_WIDTH/2 - start_button.get_width()/2, SCREEN_WIDTH/2 + start_button.get_height()/3))
    pygame.display.update()

# Function to draw the game over screen
def drawGameOverScreen(p1Score):
    screen.fill((0, 0, 0))
    font = pygame.font.SysFont('retrogaming', 20)
    if p1Score == 7:
        winner = "Player 1"
    else:
        winner = "Player 2"
    title = font.render(f'{winner} Wins!', True, white)
    playAgain = font.render('Press R To Play Again Or Press X To Exit', True, white)
    screen.blit(title, (SCREEN_WIDTH/2 - title.get_width()/2, SCREEN_HEIGHT/2 - title.get_width()/2))
    screen.blit(playAgain, (SCREEN_WIDTH/2 - playAgain.get_width()/2, SCREEN_HEIGHT/2 - playAgain.get_height()/2))

# Functions to move players up and down and check if players are colliding with walls
def checkPlayer1(player):
    key = pygame.key.get_pressed()
    if key[pygame.K_w] == True and player.y > 0:
        player.move_ip(0, -playerVelocity)
    elif key[pygame.K_s] == True and player.y + 50 < SCREEN_HEIGHT:
        player.move_ip(0, playerVelocity)

def checkPlayer2(player):
    key = pygame.key.get_pressed()
    if key[pygame.K_UP] == True and player.y > 0:
        player.move_ip(0, -playerVelocity)
    elif key[pygame.K_DOWN] == True and player.y + 50 < SCREEN_HEIGHT:
        player.move_ip(0, playerVelocity)

# Function to move the ball
def moveBall(ball, ballVelocity, YDirection, XDirection):
    if YDirection[0] == -1 and XDirection[0] == -1:
        ball.y += ballVelocity
        ball.x += ballVelocity
    elif YDirection[0] == -1 and XDirection[0] == 1:
        ball.y += ballVelocity
        ball.x -= ballVelocity
    elif YDirection[0] == 1 and XDirection[0] == -1:
        ball.y -= ballVelocity
        ball.x += ballVelocity
    elif YDirection[0] == 1 and XDirection[0] == 1:
        ball.y -= ballVelocity
        ball.x -= ballVelocity

# Function to reset the game state
def resetGame(ball, player1, player2):
    ball.x = 400
    ball.y = 300
    player1.x = 50
    player1.y = 250
    player2.x = 750
    player2.y = 250

# Function to check collision of the ball with upper and bottom walls
def checkBallBorder(ball, YDirection, p1Score, p2Score):
    if ball.bottom >= SCREEN_HEIGHT or ball.top <= 0:
        YDirection[0] *= -1
    if ball.right >= SCREEN_WIDTH:
        p1Score += 1
        resetGame(ball, player1, player2)
    if ball.left <= 0:
        p2Score += 1
        resetGame(ball, player1, player2)
    return p1Score, p2Score

# Function to check collision of the ball with players
def checkPlayerCollision(ball, player, YDirection, XDirection):
    if ball.colliderect(player):
        YDirection[0] *= -1

# Function to check the winner of the game
def checkWinner(p1Score, p2Score):
    if p1Score == 7:
        return "game_over"
    elif p2Score == 7:
        return "game_over"
    else:
        return "game"

# Create player rectangles
player1 = pygame.Rect((50, 250, 10, 50))
player2 = pygame.Rect((750, 250, 10, 50))
ball = pygame.Rect((400, 300, 10, 10))

# Run the game loop
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    # Clear the screen
    screen.fill(black)

    if game_state == "start_menu":
        # Draw the start menu
        drawStartMenu()
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            game_state = "game"
    
    if game_state == "game":
        # Draw scores
        p1ScoreDisplay = font.render(f'{p1Score}', True, white)
        p2ScoreDisplay = font.render(f'{p2Score}', True, white)
        screen.blit(p1ScoreDisplay, (200, 0)) 
        screen.blit(p2ScoreDisplay, (600, 0)) 

        # Draw players and ball
        pygame.draw.rect(screen, white, player1)
        pygame.draw.rect(screen, white, player2)
        pygame.draw.rect(screen, white, ball)

        # Check ball and player collisions
        p1Score, p2Score = checkBallBorder(ball, YDirection, p1Score, p2Score)
        moveBall(ball, ballVelocity, YDirection, XDirection)
        checkPlayer1(player1)
        checkPlayer2(player2)
        checkPlayerCollision(ball, player1, XDirection, YDirection)
        checkPlayerCollision(ball, player2, XDirection, YDirection)

        # Limit the frame rate
        clock.tick(60)

        # Check for winner
        game_state = checkWinner(p1Score, p2Score)

    if game_state == "game_over":
        # Draw the game over screen
        drawGameOverScreen(p1Score)
        key = pygame.key.get_pressed()
        if key[pygame.K_r]:
            # Reset the game
            game_state = "game"
            p1Score = 0
            p2Score = 0
        elif key[pygame.K_x]:
            # Exit the game
            run = False

    # Update the display
    pygame.display.update()

# Quit the game
pygame.quit()
