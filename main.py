'''
This is the trash game. This game will have the user move their character around the screen to collect pieces of trash. 
There is a constant loop that refreshes the character based on which arrow key is pressed. This will use the pygame
library, random library, and the os library. There will be trash sprites and a single player sprite. When the objects
collide, the trash sprite should disappear and 1 should be added to the users score. When there are no sprites left
the user should be presented with their score for the level or game. 
JACOB MARTIN
'''
import pygame
import random
import os

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'img')

WIDTH = 800  # width of our game window
HEIGHT = 600 # height of our game window
FPS = 60 # frames per second

#Define color
BLACK = (0, 0, 0)

#define the player sprite and attributes
class Player(pygame.sprite.Sprite):
    def __init__(self): #initialize the player sprite
        pygame.sprite.Sprite.__init__(self)
        self.image = right_img # make the player the player image
        self.image.set_colorkey(BLACK) #ignore black pixels of player image
        self.rect = self.image.get_rect() 
        self.rect.center = (WIDTH / 2, HEIGHT / 2) # set the sprite initial position
    
    #checks the state of the key board and adjusts the sprite according
    def update(self, direction):
        if pressed[pygame.K_UP]: #up key pressed
            self.rect.y -= 8
        elif pressed[pygame.K_DOWN]: #down key pressed
            self.rect.y += 8
        elif pressed[pygame.K_LEFT]: #left key pressed
            self.image = left_img
            self.image.set_colorkey(BLACK) #ignore black pixels 
            self.rect.x -= 8
        elif pressed[pygame.K_RIGHT]: #right key pressed
            self.image = right_img
            self.image.set_colorkey(BLACK) #ignore black pixels 
            self.rect.x += 8
        if self.rect.left > WIDTH: #if it goes off the right side return on left
            self.rect.right = 0
        elif self.rect.right < 0:    #if it goes off the left side reutrn on right
            self.rect.left = WIDTH 
        elif self.rect.top > HEIGHT: #goes off the bottom return on the top
            self.rect.bottom = 0
        elif self.rect.bottom < 0: #goes off the top return on the bottom
            self.rect.top = HEIGHT

#make the trash sprite
class bottle(pygame.sprite.Sprite):
    def __init__(self): #initialize all of the attributes for the trash sprite
        pygame.sprite.Sprite.__init__(self) #super init
        self.image = bottle_img # make the trash the trash image
        self.image.set_colorkey(BLACK) #ignore black pixels of trash image
        self.rect = self.image.get_rect() 
        self.rect.center = (random.randint(1, WIDTH - 9),random.randint(1, HEIGHT - 49)) #randomly place the bottle on the screen
#make the can sprite
class can(pygame.sprite.Sprite):
    def __init__(self): #initialize all of the attributes for the trash sprite
        pygame.sprite.Sprite.__init__(self) #super init
        self.image = can_img # make the can the can image
        self.image.set_colorkey(BLACK) #ignore black pixels of can image
        self.rect = self.image.get_rect() 
        self.rect.center = (random.randint(1, WIDTH - 9),random.randint(1, HEIGHT - 49)) #randomly place the can on the screen

# initialize pygame and create window
pygame.init()
pygame.mixer.init()  # for sound
screen = pygame.display.set_mode((WIDTH, HEIGHT)) #create the display
pygame.display.set_caption("Trash Game") #set caption
clock = pygame.time.Clock() 
#load the player and trash sprites into variables
right_img = pygame.image.load(os.path.join(img_folder, 'right.png')).convert()
left_img = pygame.image.load(os.path.join(img_folder, 'left.png')).convert()
bottle_img = pygame.image.load(os.path.join(img_folder, 'bottle.png')).convert()
can_img = pygame.image.load(os.path.join(img_folder, 'can.png')).convert()
background_img = pygame.image.load(os.path.join(img_folder, 'background.png')).convert()
win_img = pygame.image.load(os.path.join(img_folder, 'winner.png')).convert()


# start screen for beginning and end of game
def start_screen():
    screen.blit(background_img, [0, 0]) #put background on the screen
    pygame.display.flip() #must flip every display
    start = True #used to see if user has started the game
    while start:
        clock.tick(FPS) # run the start up a the right speed
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #if user exits the window
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONUP: #after the user lets go of clicking
                start = False # will leave the while loop, goes back to the program
#similar to the start screen but it puts the score on the screen
def win_screen(usrScore):
    screen.blit(win_img, [0, 0]) #puts winner background on the screen
    font_name = pygame.font.match_font('arial') #gets the arial font 
    font = pygame.font.Font(font_name, 64) #sets the font to arial size 64
    text_surface = font.render("Score = " + str(usrScore), True, BLACK) #surface object for text to go on
    text_rect = text_surface.get_rect() #makes it a rectangular object for the screen
    text_rect.midtop = (WIDTH / 2, HEIGHT / 4) #position the rect on the screen
    screen.blit(text_surface, text_rect) #put the rect on the screen and put the text on the rect
    pygame.display.flip() #must flip the display after stuff is put on it
    start = True #used to see when the window should close
    while start: #one time loop, stays on the screen for 5 seconds though
        clock.tick(FPS) #run the screen at the proper speed
        for event in pygame.event.get():# user can exit while win screen displays
            if event.type == pygame.QUIT:
                pygame.quit()
        pygame.time.wait(5000) #stays a the screen for 5 seconds
        start = False # done with the screen and can return

lvlOneMaxScore = 6 #max user score for level 1

# Game Loop
game_finish = True #assume game is over to make sure we get the start screen
running = True
while running:
    if game_finish: #start or restart the game
        start_screen() #bring up the start screen
        game_finish = False #game has started so it cant be finished
        playerSprites = pygame.sprite.Group() #group of player sprites could be 2 player eventually
        trashSprites = pygame.sprite.Group() #group of all bottlr sprites
        player = Player() #make a new player sprite
        playerSprites.add(player) #add the player to the player sprites group
        numTrash = 6 #remove later and set for each level
        #add half bottles and half cans to the trash group
        for i in range(numTrash):
            if (i < numTrash/2):
                trash = bottle()
                trashSprites.add(trash)
            else:
                trash = can()
                trashSprites.add(trash)
        #initialize the users score
        score = 0
    # Keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # Check for closing window
        if event.type == pygame.QUIT:
            running = False
    # Update
    pressed = pygame.key.get_pressed()
    playerSprites.update(pressed)
    #if the player collides with a trash sprite remove the trash from the screen
    if (pygame.sprite.spritecollide(player, trashSprites, True)):
        #add to score for collision
        score += 1
        if (score == lvlOneMaxScore):#collected all the trash go to win screen
            win_screen(score)
            game_finish = True

    # Render (draw)
    screen.fill(BLACK)
    playerSprites.draw(screen)
    trashSprites.draw(screen)
    # After drawing everything, flip the display
    pygame.display.flip()

pygame.quit()