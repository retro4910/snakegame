import pygame 
import time
import random

pygame.init()

# screen dimensions
width, height = 600, 400
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game with Obstacles")

# Colors
white = (255, 255, 255)
green = (0, 255, 0)
black = (0, 0, 0)
red = (255, 0, 0)

# Snake settings
snake_block = 10
snake_speed = 15
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 35)

#Show score
def show_score(score):
    value = font.render(f"Score: {score}", True, white)
    win.blit(value, [10, 10])

# Draw snake
def draw_snake(snake_list):
    for x in snake_list:
        pygame.draw.rect(win, green, [x[0], x[1], snake_block, snake_block])

# Message disply
def message(msg, color):
    text = font.render(msg, True, color)
    win.blit(text, [width / 3, height / 3])

def game_loop():
    game_over = False
    game_close = False
    score = 0

    x = width / 2
    y = height / 2
    x_change = 0
    y_change = 0

    snake_list = []
    length = 1

    food_x = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
    food_y = round(random.randrange(0, height - snake_block) / 10.0) * 10.0

    #Generate obstacles
    obstacle_count = 5
    obstacles = []
    for _ in range(obstacle_count):
        obs_x = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
        obs_y = round(random.randrange(0, height - snake_block) / 10.0) * 10.0
        obstacles.append([obs_x, obs_y])

    while not game_over:
        while game_close:
            win.fill(white)
            message("Yout Lost! Press Q to Quit or C to Play Again", red)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
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
        
        x += x_change
        y += y_change

        if x >= width or x < 0 or y >= height or y < 0:
            game_close = True

        win.fill(black)

        #Draw Food
        pygame.draw.rect(win, red, [food_x, food_y, snake_block, snake_block])

        #Draw obstacles
        for obs in obstacles:
            pygame.draw.rect(win, white, [obs[0],obs[1], snake_block, snake_block])

        # Update snake bode
        snake_head = [x, y]
        snake_list.append(snake_head)

        if len(snake_list) > length:
            del snake_list[0]

        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_close = True
        
        #Check collision with obstacles
        for obs in obstacles:
            if x == obs[0] and y == obs[1]:
                game_close = True
        
        draw_snake(snake_list)
        show_score(score)
        pygame.display.update()

        if x == food_x and y == food_y:
            food_x = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
            food_y = round(random.randrange(0, height - snake_block) / 10.0) * 10.0
            length += 1
            score += 10

        clock.tick(snake_speed)

    pygame.quit()
    quit()

# Start the game
game_loop()

