'''Mining for Asteroids Game'''
#Import all necessary libraries
import random
import sys
import json
import pygame

# Initialize Pygame
pygame.init()

# Screen settings
# set the width and height of the game screen
WIDTH, HEIGHT = 1000, 800
#create a window for the game display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
#get the rectangle object of the screen
screen_rect = screen.get_rect()
# setting the game name
pygame.display.set_caption("Spaceship Game")
#Define fonts
title = pygame.font.SysFont('agencyfb',72)
buttons = pygame.font.SysFont('agencyfb',60)
text_box = pygame.font.SysFont('agencyfb',20)

#load background image
background_image = pygame.image.load("background3.png").convert()
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

#sounds
countdown_sound = pygame.mixer.Sound("Menu_Sound_1.wav")
shoot_sound = pygame.mixer.Sound("Player_Shoot_Sound1.wav")
crash_effect = pygame.mixer.Sound("crash.wav")
impact_effect = pygame.mixer.Sound("impact.wav")
material_effect = pygame.mixer.Sound("material_get.wav")
countdown_sound.set_volume(0.5)
shoot_sound.set_volume(0.25)
crash_effect.set_volume(0.25)
impact_effect.set_volume(0.25)


#adding a main theme to the game
in_game = pygame.mixer.music.load("Soundtrack.wav")

#Get the json file of high scores
try:
    with open("high_scores.json","r",encoding="ascii") as hs:
        scores = json.load(hs)
except FileNotFoundError:
    print("File not found!")
    pygame.quit()
    sys.exit()

# Colors
WHITE = (255, 255, 255)

# Game settings
# setting the frame rate for the game
FPS = 60
# setting the asteroid spawn time in miliseconds
ASTEROID_SPAWN_TIME = 800
# initialize the score to 0
#score = 0


class Spaceship(pygame.sprite.Sprite):
    '''space ship controlled by the player'''
    def __init__(self, x_coord, y_coord):
        super().__init__()
        # load the spaceship image
        self.image = pygame.image.load("spaceship.png").convert_alpha()
        # getting the rectangle of the spaceship
        self.rect = self.image.get_rect()
        # setting the initial x coordinate of the spaceship
        self.rect.x = x_coord
        # setting the initial y coordinate of the spaceship
        self.rect.y = y_coord
        # setting the speed of the spaceship
        self.speed = 5

    def update(self):
        '''this function is called every frame to update
            the spaceship's position based in user's input'''
        # getting the pressed keys
        keys = pygame.key.get_pressed()
        # checking if the left arrow key is pressed
        if keys[pygame.K_LEFT]:
            # moving the spaceship to the left
            self.rect.x -= self.speed
        # checking is the right arrow key is pressed
        if keys[pygame.K_RIGHT]:
            # moving the spaceship to the right
            self.rect.x += self.speed
        # checking is the up arrow key is pressed
        if keys[pygame.K_UP]:
            # moving the spaceship upwards
            self.rect.y -= self.speed
        # checking if the down arrow key is pressed
        if keys[pygame.K_DOWN]:
            #moving the spaceship downwards
            self.rect.y += self.speed


class Asteroid(pygame.sprite.Sprite):
    '''this class will represent the asteroid'''
    def __init__(self, x_coord, y_coord, speed):
        super().__init__()
        # load the asteroid image
        self.image = pygame.image.load("asteroid.png").convert_alpha()
        # getting the rectangle of the asteroid
        self.rect = self.image.get_rect()
        # getting the initial x coordinate of the asteroid
        self.rect.x = x_coord
        # getting the initial y coordinate of the asteroid
        self.rect.y = y_coord
        # set the speed of the asteroid
        self.speed = speed

    def update(self):
        '''this function is called every frame to update the position of the asteroid'''
        # moving the asteroid downwards
        self.rect.y += self.speed
        # checking if the asteroid has gone below the screen
        if self.rect.y > HEIGHT:
            #remove the asteroid
            self.kill()


class Bullet(pygame.sprite.Sprite):
    '''this class represent the bullets fired by the space ship'''
    def __init__(self, x_coord, y_coord):
        super().__init__()
        # create a surface for the bullet
        self.image = pygame.Surface((2, 5))
        # setting the color of the bullet
        self.image.fill(WHITE)
        # getting the rectangle of the bullet
        self.rect = self.image.get_rect()
        # setting the initial x coordinate of the bullet
        self.rect.x = x_coord
        # setting the initial y coordinate of the bullet
        self.rect.y = y_coord
        # setting the speed of the bullet
        self.speed = -10

    def update(self):
        '''this function is called every frame to update the position of the bullet'''
        #moving the bullet upwards
        self.rect.y += self.speed
        # checking if the bullet has gone above the screen
        if self.rect.y < 0:
            # remove the bullet
            self.kill()

class Material(pygame.sprite.Sprite):
    '''this class represents the material dropped after the asteroid be destoyed'''
    def __init__(self, x_coord, y_coord):
        super().__init__()
        self.factor = 1
        self.factor = random.randint(1,3)
        # load the material image
        self.image = pygame.image.load("material.png").convert_alpha()

        # setting the speed of the material
        self.speed = 1/self.factor + 1

        self.scale = (0,0)
        self.scale_x = 25
        self.scale_x = int(self.scale_x * self.factor)
        self.scale_y = 25
        self.scale_y = int(self.scale_y * self.factor)
        self.scale = (self.scale_x, self.scale_y)
        # set the size of the material
        self.image = pygame.transform.scale(self.image, self.scale)
        # getting the rectangle of the material
        self.rect = self.image.get_rect()
        # setting the initial x-coordinate of the material
        self.rect.x = x_coord
        # setting the initial y-coordinate of the material
        self.rect.y = y_coord
        # set the number of points earned upon pickup
        self.price = 1*self.factor

    def update(self):
        '''this function is called every frame to update the position of the material'''
        # moving the material downwards
        self.rect.y += self.speed
        # checking if the meterial has gone below the screen
        if self.rect.y > HEIGHT:
            # remove the material
            self.kill()


def start_screen():
    '''create the start screen for the game'''
    #Make the game music stop
    pygame.mixer.music.stop()
    #Create the game title for the screen
    game_title = title.render('Mining for Asteroids',True,WHITE)
    #Create the background for the title screen
    screen.blit(background_image,(0,0))
    #Create a last of buttons for the start screen
    button_list = ["Start Game","High Score","Game Instructions","Quit"]
    #List to hold the coordinates of each button
    button_look = []
    #Create a list of button colors
    colors = [(205,30,18),(250,223,0),(0,126,58)]
    #Create flag to let us know when a button has been
    #pressed
    loop = True
    #Place the title on the screen
    game_title_rect = game_title.get_rect()
    game_title_rect.centerx = screen_rect.centerx
    game_title_rect.centery = 100
    screen.blit(game_title,game_title_rect)
    #Create the buttons
    button_look = create_buttons(colors[-1],"Start Game","High Score","Game Instructions","Quit")
    #Get the clock
    clk = pygame.time.Clock()
    #Variable to hold the color changing time
    color_change = 0
    #Variable to hold index of color list
    index = 0
    #Check if the user exited the screen
    while loop:
        #Get the ticks
        ticks = clk.tick()
        #Add this to the color change time
        color_change += ticks
        #If it has been greater than 2 seconds, change to next color in list
        if color_change >= 500:
            button_look = create_buttons(colors[index],"Start Game","High Score","Game Instructions","Quit")
            #Change to next index
            index += 1
            #Check we are not out of bounds
            if index > len(colors) - 1:
                index = 0
            #Reset color_change so we can change colors again
            color_change = 0
        #Look through each pygame event
        for event in pygame.event.get():
            #If it is the quit event, quit the game
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            #If the user clicked the mouse
            if event.type == pygame.MOUSEBUTTONUP:
                #Play a sound
                pygame.mixer.Sound.play(shoot_sound)
                #See if the user clicked a button
                #Call the proper function if so
                if (button_look[0][0] < event.pos[0] < button_look[0][1] and
                button_look[0][2] < event.pos[1] < button_look[0][3]) :
                    loop = not loop
                    gameloop()
                if (button_look[1][0] < event.pos[0] < button_look[1][1] and
                button_look[1][2] < event.pos[1] < button_look[1][3]):
                    loop = not loop
                    high_scores()
                if (button_look[2][0] < event.pos[0] < button_look[2][1] and
                button_look[2][2] < event.pos[1] < button_look[2][3]):
                    loop = not loop
                    game_instructions()
                if (button_look[3][0] < event.pos[0] < button_look[3][1] and
                button_look[3][2] < event.pos[1] < button_look[3][3]):
                    pygame.quit()
                    sys.exit()

def create_buttons(color,*button_list):
    '''Create the buttons for the screen'''
    #List to hold button positions
    button_look = []
    #Counter to output buttons
    counter = 300
    #Place each button on the screen
    for button in button_list:
        #Render the choice
        choice = buttons.render(button,True,color)
        #Get the rectangle of the button
        choice_rect = choice.get_rect()
        #Set the centerx and centery values for the rectangle
        choice_rect.centerx = WIDTH/2
        choice_rect.centery = counter
        #Blit the button to the screen
        screen.blit(choice,choice_rect)
        #Add the coordinates to the list so we can see which button was pressed
        button_look.append((choice_rect.left,choice_rect.right,choice_rect.top,choice_rect.bottom))
        #Update the counter
        counter += 100
    #Update the screen
    pygame.display.flip()
    #Return the list of button positions
    return button_look

def countdown(duration):
    '''count down before the game start'''
    #initialize the font and font size
    font = pygame.font.Font(None, 72)
    #set the count down color
    countdown_color = (255, 255, 255)

    pygame.mixer.Sound.play(countdown_sound)

    #iterate through the duration of the countdown
    for i in range(duration, 0, -1):
        #fill the screen with a black background
        screen.fill((0,0,0))
        countdown_text = font.render(str(i), True, countdown_color)
        # set the position of the countdown at the center of the screen
        text_rect = countdown_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

        screen.blit(countdown_text, text_rect)
        pygame.display.flip()
        pygame.time.wait(1000)

def high_scores():
    '''Show the high scores screen'''
    #Open the high scores file
    loop = True
    screen.blit(background_image,(0,0))
    #Create the title for the high scores page
    page_title = title.render("High Scores",True,WHITE)
    page_title_rect = page_title.get_rect()
    page_title_rect.centerx = screen_rect.centerx
    page_title_rect.centery = 100
    screen.blit(page_title,page_title_rect)
    #Create all the high score rows
    counter = 200
    for x_num in range(5):
        #Get the name of the scorer
        score_l = buttons.render(scores["names"][x_num],True,WHITE)
        score_rect = score_l.get_rect()
        #Set the x and y values
        score_rect.centerx = WIDTH // 4
        score_rect.centery = counter
        #Get the score of the scorer
        number = buttons.render(str(scores["scores"][x_num]),True,WHITE)
        number_rect = number.get_rect()
        #Set the x and y values
        number_rect.centerx = 3 * WIDTH // 4
        number_rect.centery = counter
        screen.blit(score_l,score_rect)
        screen.blit(number,number_rect)
        #Increment the counter for the y placement
        counter+= 100
    #Create the back button
    back = buttons.render("Main Screen",True,WHITE)
    back_rect = back.get_rect()
    back_rect.centerx = WIDTH // 2
    back_rect.centery = counter
    screen.blit(back,back_rect)
    #Update the screen
    pygame.display.flip()
    while loop:
        #Check all events
        #If the user clicked the main
        #screen button, create the start screen again
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                if (back_rect.left < event.pos[0] < back_rect.right
                    and back_rect.top < event.pos[1] < back_rect.bottom):
                    loop = not loop
                    start_screen()

def get_new_high_score(p_score):
    '''If the user's high score is a new high score, get their username'''
    #Recreate the background
    screen.blit(background_image,(0,0))
    #Create a text box
    rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 20, 200, 40)
    #Create color for when the user has clicked the text box
    clicked = (16,53,172)
    active = False
    loop = True
    given = ''
    #Loop through to get the user input
    while loop:
        #Look at all events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            #If we click in the text box, highlight it
            if event.type == pygame.MOUSEBUTTONDOWN:
                if rect.left < event.pos[0] < rect.right and rect.top < event.pos[1] < rect.bottom:
                    active = True
                else:
                    active = False
            #If a key is pressed, check which one
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                #If backspace, remove last character
                if keys[pygame.K_BACKSPACE]:
                    given = given[:-1]
                #If enter key/return, stop gettng characters
                elif keys[pygame.K_RETURN]:
                    loop = False
                #Otherwise, add the characcter to the username
                else:
                    given += event.unicode
        screen.blit(background_image,(0,0))
        #Check if the text box has been clicked
        if active:
            color = clicked
        else:
            color = WHITE
        #Add page title
        page_title = title.render("Enter Your Username for High Score",True,WHITE)
        page_title_rect = page_title.get_rect()
        page_title_rect.centerx = screen_rect.centerx
        page_title_rect.centery = 100
        screen.blit(page_title,page_title_rect)
        #Add instructions
        page_instr = title.render("Press RETURN when done",True,WHITE)
        page_instr_rect = page_instr.get_rect()
        page_instr_rect.centerx = screen_rect.centerx
        page_instr_rect.centery = 175
        screen.blit(page_instr,page_instr_rect)
        #Draw text box
        pygame.draw.rect(screen,color,rect)
        #Create user input so far
        text = text_box.render(given,True,(0,0,0))
        #Blit on top of text box
        screen.blit(text,(rect.x + 10,rect.y + 10))
        #Update the screen
        pygame.display.flip()
    #Remove the last values from the high scores lists
    scores["names"].pop()
    scores["scores"].pop()
    #Add the new high score and name where they should be
    i = 0
    while p_score <= scores["scores"][i]:
        i+=1
        if i == 4:
            break
    scores["names"].insert(i,given)
    scores["scores"].insert(i,p_score)
    #Save to the json file
    with open("high_scores.json","w",encoding="ascii") as h_s:
        json.dump(scores,h_s)

def game_instructions():
    '''display the game instructions'''

    #List of all instruction texts
    instructions_text = [
        "Welcome to Mining for Asteroids!",
        " ",
        "Instructions:",
        "1. Use the arrow keys to move your spaceship.",
        "2. Press the space key to shoot.",
        " ",
        "Collect resources and avoid enemy ships. Good luck!",
        " ",
        "Press any key to return to the main menu."
    ]
    #Blit the normal background to the screen
    screen.blit(background_image, (0, 0))
    #Variable to hold where we are placing text on the y-axis
    y_offset = 100

    #Go through each line of text
    for line in instructions_text:
        #Render the text
        line_surface = buttons.render(line, True, WHITE)
        line_rect = line_surface.get_rect()
        line_rect.centerx = screen_rect.centerx
        line_rect.centery = y_offset
        screen.blit(line_surface, line_rect)
        #Increment the y offset so the next text
        #is 60 pixels down
        y_offset += 60

    #Update the screen
    pygame.display.flip()

    #Keep checking to see if the user has pressed a key
    #If so go back to the start screen
    instructions_loop = True
    while instructions_loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                instructions_loop = False
    start_screen()

def game_over_screen(p_score):
    '''Show the game over screen'''
    #Create the font and text color
    font = pygame.font.Font(None, 72)
    game_over_color = (255, 255, 255)

    #Render the game over message, showing the player's score
    game_over_text = font.render("Game Over", True, game_over_color)
    game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))

    score_text = font.render(f"Your Score: {p_score}", True, game_over_color)
    score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    screen.blit(game_over_text, game_over_rect)
    screen.blit(score_text, score_rect)
    pygame.display.flip()

    #Wait 3 seconds
    pygame.time.wait(3000)

    #Check if the user made a high score
    if p_score > scores["scores"][4]:
        get_new_high_score(p_score)

    #Go back to the start screen
    start_screen()

def gameloop():
    '''Function that controls the gameplay'''
    #Score holder
    score = 0
    #Play the music
    pygame.mixer.music.play(-1)
    #Get the clock
    clock = pygame.time.Clock()
    #Make a group to hold all sprites
    all_sprites = pygame.sprite.Group()
    #Create a spacesjip and add it to the group
    spaceship = Spaceship(WIDTH // 2 - 25, HEIGHT - 75)
    all_sprites.add(spaceship)

    #Create groups for asteroids, bullets, and materials
    asteroids = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    materials = pygame.sprite.Group()

    #Creeate a spawn timer
    asteroid_spawn_timer = pygame.time.get_ticks()

    font = pygame.font.Font(None, 36)
    score_color = (255, 255, 255)

    #Countdown the game start
    countdown_duration = 3
    countdown(countdown_duration)

    #Run the game until the user quits or
    #the user "dies"
    running = True
    while running:
        clock.tick(FPS)

        #See if the user quit the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #running = False
                pygame.quit()
                sys.exit()

            #See if the user pressed spacebar to shoot a bullet
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    #Create a bullet
                    bullet = Bullet(spaceship.rect.x + 23, spaceship.rect.y)
                    #Add the bullet to the bullet and all sprites groups
                    all_sprites.add(bullet)
                    bullets.add(bullet)
                    #play sound effect when player presses SPACE
                    pygame.mixer.Sound.play(shoot_sound)

        #Create a new asteroid if the timer states we can
        if pygame.time.get_ticks() - asteroid_spawn_timer > ASTEROID_SPAWN_TIME:
            asteroid = Asteroid(random.randint(0, WIDTH - 50), 0, random.randint(1, 3))
            all_sprites.add(asteroid)
            asteroids.add(asteroid)
            #Update the timer
            asteroid_spawn_timer = pygame.time.get_ticks()

        # Update sprites
        all_sprites.update()

        # Check for collisions
        asteroid_bullet_collisions = pygame.sprite.groupcollide(asteroids, bullets, True, True)

        #Create the material to "mine" if an asteroid has been hit
        for collision in asteroid_bullet_collisions:
            material = Material(collision.rect.x, collision.rect.y)
            all_sprites.add(material)
            materials.add(material)
            # Playing impact noise
            impact_effect.play()

        spaceship_asteroid_collisions = pygame.sprite.spritecollide(spaceship, asteroids, True)
        spaceship_material_collisions = pygame.sprite.spritecollide(spaceship, materials, True)

        for material in spaceship_material_collisions:
             # Playing noise upon gathering material
            material_effect.play()
            score += material.price


        if spaceship_asteroid_collisions:
            running = False
             # Playing crash noise
            crash_effect.play()

        # Clear the screen and draw sprites
        screen.blit(background_image, (0, 0))
        score_text = font.render(f"Score: {score}", True, score_color)
        screen.blit(score_text, (10, 10))

        all_sprites.draw(screen)
        pygame.display.flip()

    #once user gets hit or quits, show game over screen
    game_over_screen(score)

def main():
    '''Main function for the game'''
    #Create the start screen
    start_screen()

if __name__ == "__main__":
    main()
