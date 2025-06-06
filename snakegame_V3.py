import pygame
import time 
import random 
import os

#Initialize Pygame and mixer
pygame.init()
pygame.mixer.init()

#sound effects
eat_sound = pygame.mixer.Sound("eat.wav") #Add a "eat.wav" file in the same folder
eat_sound.set_volume(0.3)
game_over_sound = pygame.mixer.Sound("gameover.wav") #Add a "gameover.wav" file
game_over_sound.set_volume(0.1)

#Screen setup
width, height = 600, 400
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("🐍 Snake Game")

#Colors
white = (255, 255, 255)
green = (0, 255, 0)
black = (0, 0, 0)
red = (255, 0, 0)

#Snake settings
snake_block = 10
clock = pygame.time.Clock()
font = pygame.font.SysFont("comicsansms", 28)

# Load high score
def load_high_score():
    if os.path.exists("highscore.txt"):
        with open("highscore.txt", "r") as f:
            return int(f.read())
    return 0
#Save high score
def save_high_score(score):
    with open("highscore.txt", "w") as f:
        f.write(str(score))

# Draw snake
def draw_snake(snake_list):
    for x in snake_list:
        pygame.draw.rect(win, green, [x[0], x[1], snake_block, snake_block])

# Display score
def show_score(score, high_score):
    value = font.render(f"Score: {score} High Score: {high_score}", True, white)
    win.blit(value, [10, 10])

# Game Over Screen
def game_over_screen(score, high_score):
    win.fill(black)
    game_over_sound.stop()
    game_over_sound.play()
    message1 = font.render("💀 Game Over!", True, red)
    message2 = font.render(f"Your Score: {score}", True, white)
    message3 = font.render("Press C to Play Again or Q to quit", True, white)
    win.blit(message1, [width // 3, height // 4])
    win.blit(message2, [width // 3, height // 3])
    win.blit(message3, [width // 8, height // 2])
    pygame.display.update()

# Difficulty menu
def difficulty_menu():
    selecting = True
    while selecting:
        win.fill(black)
        title = font.render("Select Difficulty", True, green)
        easy = font.render("1. Easy 🐢", True, white)
        medium = font.render("2. Medium 🐍", True, green)
        hard = font.render("3. Hard 🐉", True, red)
        win.blit(title, [width //4, height // 6])
        win.blit(easy, [width // 3, height // 3])
        win.blit(medium, [width // 3, height // 2.5])
        win.blit(hard, [width // 3, height // 2])
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 10
                elif event.key == pygame.K_2:
                    return 15
                elif event.key == pygame.K_3:
                    return 25
                
# Main game loop
def game_loop(snake_speed):
    game_over = False
    game_close = False
    paused = False

    x = width / 2
    y = height / 2
    x_change = 0
    y_change = 0

    snake_list = []
    length = 1
    score = 0
    high_score = load_high_score()

    food_x = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
    food_y = round(random.randrange(0, height - snake_block) / 10.0) * 10.0

    while not game_over:
        while game_close:
            if score > high_score:
                save_high_score(score)
                high_score = score
            game_over_screen(score, high_score)

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.k_q:
                        game_over = True
                        game_close = False
                    elif event.key == pygame.K_c:
                        return game_loop(snake_speed)
                    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x_change == 0:
                    x_change = -snake_block
                    y_change = 0
                elif event.key ==  pygame.K_RIGHT and x_change == 0:
                    x_change = snake_block
                    y_change = 0
                elif event.key == pygame.K_UP and y_change == 0:
                    y_change = -snake_block
                    x_change = 0
                elif event.key == pygame.K_DOWN and y_change == 0:
                    y_change = snake_block
                    x_change = 0
                elif event.key == pygame.K_p:
                    paused = not paused
        
        if paused:
            continue

        x += x_change
        y += y_change 

        if x >= width or x < 0 or y >= height or y < 0:
            game_close = True

        win.fill(black)
        pygame.draw.rect(win, red, [food_x, food_y, snake_block, snake_block])

        snake_head = [x, y]
        snake_list.append(snake_head)
        if len(snake_list) > length:
            del snake_list[0]
        
        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_close = True

        draw_snake(snake_list)
        show_score(score, high_score)
        pygame.display.update()

        if x == food_x and y == food_y:
            eat_sound.play()
            food_x = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
            food_y = round(random.randrange(0, height - snake_block) / 10.0) * 10.0
            length += 1
            score += 10

        clock.tick(snake_speed)

    pygame.quit()
    quit()

# Run game
def main():
    while True:
        snake_speed = difficulty_menu()
        game_loop(snake_speed)

main()