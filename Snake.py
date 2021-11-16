# import libraries
import pygame
import random
import os
import numpy as np

# Intilize music
pygame.mixer.init()

# Initilize pygame
pygame.init()

# Define color
White = (255,255,255)
Red = (255,0,0)
Black = (0,0,0)
Blam = (210,214,217)
Reddish =(159,2,81)
Sun =(213,117,0)
Green = (0,66,54)
Sweet = (207,0,99)
Blue = (0,65,89)

# snake color list
snk_col_list=[White,Red,Black,Reddish,Sun,Green,Sweet,Blue]

# creating game window
screen_width = 900
screen_height = 700
GameWindow = pygame.display.set_mode((screen_width,screen_height))

# creating title
pygame.display.set_caption("Snake-Game")
pygame.display.update()# To see changes

# Home screen & Game image

bgimg = pygame.image.load("snakeHome.jpg")
bgimg = pygame.transform.scale(bgimg,(screen_width,screen_height)).convert_alpha()

gameimg = pygame.image.load("gameimage.jpeg")
gameimg = pygame.transform.scale(gameimg,(screen_width,screen_height)).convert_alpha()

GameOver = pygame.image.load("GameOver.jpeg")
GameOver = pygame.transform.scale(GameOver,(screen_width,screen_height)).convert_alpha()

# Creating a clock
clock = pygame.time.Clock()
fps = 30 # frame per second

# Creating a fxn to print text on screen
font = pygame.font.SysFont(None,35)
def text_on_screen(text,color,x,y):
    screen_text = font.render(text,True,color)
    # update on screen
    GameWindow.blit(screen_text,[x,y])

# Ploting snake on screen at (x,y)
def plot_snake(GameWnidow,color,snk_list,snake_size):
    count = 0
    for x,y in snk_list:
        pygame.draw.rect(GameWnidow, color, [x, y, snake_size, snake_size])
# welcome screen
def Welcome_screen():
    game_exit = False

    while not game_exit:
        GameWindow.fill(Blue)
        GameWindow.blit(bgimg,(0,0))
        # text_on_screen("\t\tWelcome To Snake-Game\t\t",White,250,280)
        text_on_screen("\t\tEnter space to continue\t\t", White, 260, 590)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True
            if event.type ==pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    GameLoop()
        pygame.display.update()
        clock.tick(fps)

# creating game-loop
def GameLoop():
    # creating game-variables
    game_exit = False
    game_over = False

    ''' Snake'''
    snake_x = 80
    snake_y = 80
    snake_size = 40
    velocity_x = 0
    velocity_y = 0
    init_velocity = 4

    ''' Food'''
    food_x = random.randint(80, screen_width / 2)
    food_y = random.randint(80, screen_height / 2)
    food_size = 40

    ''' Score'''
    score = 0

    ''' High score'''
    # check if file not exit
    if(not os.path.exists("highscore.txt")):
        with open("highscore.txt","w") as file:
            file.write("0")
    with open("highscore.txt","r") as file:
        his_score=file.read()

    # To change length of snake
    snk_list = []
    snk_length = 1
    while not game_exit:
        if game_over:
            #  File kholker usme update ker rhaai hai score
            with open("highscore.txt","w") as file:
                file.write(str(his_score))

            GameWindow.fill(Green)
            GameWindow.blit(GameOver,(0,0))
            text_on_screen("Game over!",Reddish,350,270)
            text_on_screen("Press Enter to continue", Sun, 290, 320)

            # To restart
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_exit = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        GameLoop()
        else:
            # For every event on screen
            for event in pygame.event.get():
                # By clicking on X if we want to exit
                if event.type == pygame.QUIT:
                    game_exit = True
                # If user enter any key
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_LEFT:
                        velocity_x = -init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_UP:
                        velocity_y = -init_velocity
                        velocity_x = 0
                    if event.key == pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0

            snake_x = snake_x + velocity_x
            snake_y = snake_y + velocity_y

            # Reploting food and update score
            if abs(snake_x-food_x)<15 and abs(snake_y-food_y)<15:
                score += 10
                # change position of food
                food_x = random.randint(80, screen_width / 2)
                food_y = random.randint(80, screen_height / 2)

                snk_length += 5
                if score>int(his_score):
                    his_score =score
                pygame.mixer.music.load("Swoosh.mp3")
                pygame.mixer.music.play()
            # Screen related stuff
            GameWindow.fill(Green)
            GameWindow.blit(gameimg,(0,0))
            # To show score
            text_on_screen("Score =>  " + str(score)+" " +str("\t "*25)+"High-Score =>  "+str(his_score)+"  ", Blam, 16, 16)

            # To update cordinate
            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            # After a particuler length del head
            if len(snk_list)>snk_length:
                del snk_list[0]

            # Bpoundries
            if snake_x<70 or snake_x>screen_width-110 or snake_y<70 or snake_y>screen_height-110:
                game_over = True
                pygame.mixer.music.load("Gamover.mp3")
                pygame.mixer.music.play()
            if head in snk_list[:-1]:
                game_over = True
                pygame.mixer.music.load("Gamover.mp3")
                pygame.mixer.music.play()

            # To Draw rectangle for snake
            plot_snake(GameWindow,Black,snk_list,snake_size)

            # To Draw rectangle for food
            pygame.draw.rect(GameWindow,Sweet,[food_x,food_y,food_size,food_size])

            # To see changes
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()
Welcome_screen()
