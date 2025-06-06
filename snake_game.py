import pygame
import time
import random

# Adding the scoring system
def show_score(score):
    value = font.render(f"Score: {score}", True, white)
    win.blit(value, [10, 10])

# initialize the pygame library
pygame.init()

#Screen Setup
width, height = 600, 400
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

#Define Colors using RGB values
white = (255, 255, 255)
green = (0, 255, 0)
black = (0, 0, 0)
red = (255, 0, 0)

#Snake settings
snake_block= 10 #size of the snake block
snake_speed = 15 # how fast the snake moves
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 35) # font for text

#Function to draw the snake
def draw_snake(snake_list):
    for x in snake_list:
        pygame.draw.rect(win, green, [x[0], x[1], snake_block, snake_block])

#Function to show the message on the screen
def message(msg, color):
    text = font.render(msg, True, color)
    win.blit(text, [width / 3, height / 3])

# main game loop
def game_loop():
    game_over = False
    game_close = False

    score = 0
    
    # initial position of the snake
    x = width / 2
    y = height / 2

    # Movement variable
    x_change = 0
    y_change = 0

    # Snake body and length
    snake_list = []
    length = 1

    # Randon positon of food
    food_x = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
    food_y = round(random.randrange(0, height - snake_block) / 10.0) * 10.0



    # Main game loop
    while not game_over:
        
        # Handle game over state
        while game_close:
            win.fill(white)
            message("You Lost! Press Q to Quit or C to Play Again", red)
            pygame.display.update()

            # Listen for key press after losing
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q: # Quit
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c: #restart Game
                        game_loop()

        # Handle events like key press
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                # Change directions based on arrow keys
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
            
         # Update snke position
        x += x_change
        y += y_change

        # End game if snake hits walls
        if x >= width or x < 0 or y >= height or y < 0:
            game_close = True

        # Fill background
        win.fill(black)

        # Draw food
        pygame.draw.rect(win, red, [food_x, food_y, snake_block, snake_block])

        #update snake body
        snake_head = [x, y]
        snake_list.append(snake_head)

        #keep the snake length consistent
        if len(snake_list) > length:
            del snake_list[0]

        # check for self-collision
        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_close = True

        #Draw the snake
        draw_snake(snake_list)
        
        show_score(score)

        # Update the screen
        pygame.display.update()

        #check if the snake eats the food
        if x == food_x and y == food_y:
            food_x = round(random.randrange(0,  width - snake_block) / 10.0) * 10.0
            food_y = round(random.randrange(0, height - snake_block) / 10.0) * 10.0
            length += 1 # Grow the snake
            score += 10 # add points

        # Control the game speed
        clock.tick(snake_speed)

    #quit the game 
    pygame.quit()
    quit()
#main menu
def main_menu():
    in_menu = True
    while in_menu:
        win.fill(black)
        title = font.render("Welcome to Snake Game", True, green)
        prompt = font.render("Press SPACE to start or Q to Quit", True, white)
        win.blit(title, [width // 6, height // 3])
        win.blit(prompt, [width // 6, height // 2])
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    in_menu = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()
# Start the game 
main_menu()
game_loop()
