import pygame
import time
import random

# Initialize the Pygame library
pygame.init()

# Screen dimensions
width, height = 600, 400
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

# Define colors using RGB values
white = (255, 255, 255)
green = (0, 255, 0)
black = (0, 0, 0)
red = (255, 0, 0)

# Snake settings
snake_block = 10  # size of the snake block (square)
snake_speed = 15  # how fast the snake moves
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 35)  # font for text

# Function to draw the snake
def draw_snake(snake_list):
    for x in snake_list:
        pygame.draw.rect(win, green, [x[0], x[1], snake_block, snake_block])

# Function to show a message on the screen
def message(msg, color):
    text = font.render(msg, True, color)
    win.blit(text, [width / 3, height / 3])

# Main game loop
def game_loop():
    game_over = False
    game_close = False

    # Initial position of the snake
    x = width / 2
    y = height / 2

    # Movement variables
    x_change = 0
    y_change = 0

    # Snake body and length
    snake_list = []
    length = 1

    # Random position for the food
    food_x = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
    food_y = round(random.randrange(0, height - snake_block) / 10.0) * 10.0

    # Main game loop
    while not game_over:

        # Handle game over state
        while game_close:
            win.fill(white)
            message("You Lost! Press Q to Quit or C to Play Again", red)
            pygame.display.update()

            # Listen for key presses after losing
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:  # Quit
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:  # Restart game
                        game_loop()

        # Handle events like key presses
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                # Change direction based on arrow keys
                if event.key == pygame.K_LEFT:
                    x_change = -snake_block
                    y_change = 0
                elif event.key == pygame.K_RIGHT:
                    x_change = snake_block
                    y_change = 0
                elif event.key == pygame.K_UP:
                    y_change = -snake_block
                    x_change = 0
                elif event.key == pygame.K_DOWN:
                    y_change = snake_block
                    x_change = 0

        # Update snake position
        x += x_change
        y += y_change

        # End game if snake hits wall
        if x >= width or x < 0 or y >= height or y < 0:
            game_close = True

        # Fill background
        win.fill(black)

        # Draw food
        pygame.draw.rect(win, red, [food_x, food_y, snake_block, snake_block])

        # Update snake body
        snake_head = [x, y]
        snake_list.append(snake_head)

        # Keep the snake length consistent
        if len(snake_list) > length:
            del snake_list[0]

        # Check for self-collision
        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_close = True

        # Draw the snake
        draw_snake(snake_list)

        # Update the screen
        pygame.display.update()

        # Check if snake eats the food
        if x == food_x and y == food_y:
            food_x = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
            food_y = round(random.randrange(0, height - snake_block) / 10.0) * 10.0
            length += 1  # Grow the snake

        # Control the game speed
        clock.tick(snake_speed)

    # Quit the game
    pygame.quit()
    quit()

# Start the game
game_loop()
