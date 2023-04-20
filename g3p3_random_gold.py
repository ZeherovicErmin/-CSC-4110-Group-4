import pygame
import random
import sys

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


# Colors
WHITE = (255, 255, 255)

# Game settings
# setting the frame rate for the game
FPS = 60
# setting the asteroid spawn time in miliseconds
ASTEROID_SPAWN_TIME = 800
# initialize the score to 0
score = 0


class Spaceship(pygame.sprite.Sprite):
    '''space ship controlled by the player'''
    def __init__(self, x, y):
        super().__init__()
        # load the spaceship image
        self.image = pygame.image.load("spaceship.png").convert_alpha()
        # getting the rectangle of the spaceship
        self.rect = self.image.get_rect()
        # setting the initial x coordinate of the spaceship
        self.rect.x = x
        # setting the initial y coordinate of the spaceship
        self.rect.y = y
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
    def __init__(self, x, y, speed):
        super().__init__()
        # load the asteroid image
        self.image = pygame.image.load("asteroid.png").convert_alpha()
        # getting the rectangle of the asteroid
        self.rect = self.image.get_rect()
        # getting the initial x coordinate of the asteroid
        self.rect.x = x
        # getting the initial y coordinate of the asteroid
        self.rect.y = y
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
    def __init__(self, x, y):
        super().__init__()
        # create a surface for the bullet
        self.image = pygame.Surface((2, 5))
        # setting the color of the bullet
        self.image.fill(WHITE)
        # getting the rectangle of the bullet
        self.rect = self.image.get_rect() 
        # setting the initial x coordinate of the bullet
        self.rect.x = x
        # setting the initial y coordinate of the bullet
        self.rect.y = y
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
    def __init__(self, x, y):
        super().__init__()
        self.factor = 1;
        self.factor = random.randint(1,3);
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
        self.rect.x = x
        # setting the initial y-coordinate of the material
        self.rect.y = y
        # set the number of points earned upon pickup
        self.price = 1*self.factor;

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
    #Create the game title for the screen
    game_title = title.render('Mining for Asteroids',True,WHITE)
    #Create the background for the title screen
    screen.blit(background_image,(0,0))
    #Create a last of buttons for the start screen
    button_list = ["Start Game","Quit"]
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
    button_look = create_buttons(button_list,colors[-1])
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
            button_look = create_buttons(button_list,colors[index])
            #Change to next index
            index += 1
            #Check we are not out of bounds
            if index > len(colors) - 1:
                index = 0
            #Reset color_change so we can change colors again
            color_change = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                if button_look[0][0] < event.pos[0] < button_look[0][1] and button_look[0][2] < event.pos[1] < button_look[0][3] :
                    loop = not loop
                    gameloop()
                if button_look[1][0] < event.pos[0] < button_look[1][1] and button_look[1][2] < event.pos[1] < button_look[1][3]:
                    pygame.quit()
                    sys.exit()

def create_buttons(button_list,color):
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

def game_over_screen(score):
    font = pygame.font.Font(None, 72)
    game_over_color = (255, 255, 255)

    game_over_text = font.render("Game Over", True, game_over_color)
    game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))

    score_text = font.render(f"Your Score: {score}", True, game_over_color)
    score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    screen.blit(game_over_text, game_over_rect)
    screen.blit(score_text, score_rect)
    pygame.display.flip()

    pygame.time.wait(3000)

def gameloop():
    global score
    pygame.mixer.music.play(-1)
    clock = pygame.time.Clock()
    all_sprites = pygame.sprite.Group()
    spaceship = Spaceship(WIDTH // 2 - 25, HEIGHT - 75)
    all_sprites.add(spaceship)

    asteroids = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    materials = pygame.sprite.Group()

    asteroid_spawn_timer = pygame.time.get_ticks()

    font = pygame.font.Font(None, 36)
    score_color = (255, 255, 255)

    countdown_duration = 3
    countdown(countdown_duration)

    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullet = Bullet(spaceship.rect.x + 23, spaceship.rect.y)
                    all_sprites.add(bullet)
                    bullets.add(bullet)
                    #play sound effect when player presses SPACE
                    pygame.mixer.Sound.play(shoot_sound)


        if pygame.time.get_ticks() - asteroid_spawn_timer > ASTEROID_SPAWN_TIME:
            asteroid = Asteroid(random.randint(0, WIDTH - 50), 0, random.randint(1, 3))
            all_sprites.add(asteroid)
            asteroids.add(asteroid)
            asteroid_spawn_timer = pygame.time.get_ticks()

        # Update sprites
        all_sprites.update()

        # Check for collisions
        asteroid_bullet_collisions = pygame.sprite.groupcollide(asteroids, bullets, True, True)

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

    game_over_screen(score)

    pygame.quit()
    sys.exit()

def main():
    '''Main function for the game'''
    #Create the start screen
    start_screen()

if __name__ == "__main__":
    main()

