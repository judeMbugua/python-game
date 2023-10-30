import pygame
import os
pygame.font.init()
pygame.mixer.init()


WIDTH,HEIGHT = 900,500

WINDOW = pygame.display.set_mode((WIDTH,HEIGHT)) #sets the size of the pygame window
pygame.display.set_caption("A Fun Game By Jude")

#creating own user events for collision and health updates
YELLOW_HIT = pygame.USEREVENT + 1  #the numbers are some sort of a unique event id
RED_HIT = pygame.USEREVENT + 2     

HEALTH_FONT = pygame.font.SysFont('comicsans',40) #creating a font object
WINNER_FONT = pygame.font.SysFont('comicsans',100)


BLACK = (0,0,0)
WHITE = (255,255,255) #rgb values for color white
RED = (255,0,0)
YELLOW = (255,255,0)


BULLET_DAMAGE = 3
FPS = 60 #setting the game's framerate so that it constant on all computers
VEL = 5 #the players moving velocity
BORDER = pygame.Rect(WIDTH/2 - 5,0,10,HEIGHT) #the x of the the border is the width of the whole window divided by two for it to be in the middle,then minus half the width of the border itself

BULLET_VEL = 7 #the velocity of the bullets
MAX_BULLETS = 3 #the maximum number of bullets the user can fire?

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets','spaceship_yellow.png')) #joins to the path of the png
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets','spaceship_red.png'))

YELLOW_SPACESHIP =pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE,(55,40)), 90) #changing the size of the images(sprites) and rotating them
RED_SPACESHIP =pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE,(55,40)),270)
SPACE_BG = pygame.transform.scale(pygame.image.load(os.path.join('Assets','space.png')),(WIDTH,HEIGHT))

SHOOT_SOUND = pygame.mixer.Sound(os.path.join('Assets','Gun+Silencer.mp3'))


#draws on the window
def draw_window(yellowRect,redRect,red_bullets,yellow_bullets,red_health,yellow_health):
    WINDOW.blit(SPACE_BG,(0,0)) #drawing the background

    #creating text objects using the HEALTH_FONT want created earlier
    red_health_text = HEALTH_FONT.render('Health: ' + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render('Health: ' + str(yellow_health), 1, WHITE)

                                #below,making sure we get the correct coordinates
    WINDOW.blit(red_health_text,(WIDTH - red_health_text.get_width() - 10,10)) #drawing the red health text object
    WINDOW.blit(yellow_health_text,(10,10))
    pygame.draw.rect(WINDOW,BLACK,BORDER) #drawing the border rect on the screen
    WINDOW.blit(YELLOW_SPACESHIP,(yellowRect.x,yellowRect.y)) #function is used to draws surfaces onto the window takes object screen position
    WINDOW.blit(RED_SPACESHIP,(redRect.x,redRect.y))

    #looping thru the bullets lists and drawing each bullet on the screen
    for bullet in red_bullets:
        pygame.draw.rect(WINDOW,RED,bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WINDOW,YELLOW,bullet)

    pygame.display.update()


#moving the yellow spaceship
def yellow_handle_movement(keys_pressed,yellowRect):
        #using wasd for movement
        #used if statements instead of elifs to enable double key pressing
        if keys_pressed[pygame.K_a] and yellowRect.x - VEL > 0: #restricting the player within the game window
            yellowRect.x -= VEL
        if keys_pressed[pygame.K_d]and yellowRect.x + VEL + yellowRect.width < BORDER.x:
            yellowRect.x += VEL
        if keys_pressed[pygame.K_w] and yellowRect.y - VEL > 0: 
            yellowRect.y -= VEL
        if keys_pressed[pygame.K_s] and yellowRect.y + VEL + yellowRect.height < HEIGHT: 
            yellowRect.y += VEL




#moving the red spaceship
def red_handle_movement(keys_pressed,redRect):
        #using wasd for movement
        #used if statements instead of elifs to enable double key pressing
        if keys_pressed[pygame.K_LEFT] and redRect.x - VEL > BORDER.x + BORDER.width: 
            redRect.x -= VEL
        if keys_pressed[pygame.K_RIGHT] and redRect.x + VEL + redRect.width < WIDTH:   
            redRect.x += VEL
        if keys_pressed[pygame.K_UP]  and redRect.y - VEL > 0: 
            redRect.y -= VEL
        if keys_pressed[pygame.K_DOWN]  and redRect.y + VEL + redRect.height < HEIGHT: 
            redRect.y += VEL




#handles bullets and collision
def bullet_handle(yellows_bullets,reds_bullets,yellowPlayer,redPlayer):

    #checking whether whether any of yellows bullets hit the red player
    for bullet in yellows_bullets:
        bullet.x += BULLET_VEL
        if redPlayer.colliderect(bullet):  #if the rec of bullet collided with the rect of redPlayer   
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellows_bullets.remove(bullet)
        elif bullet.x > WIDTH:           #checking whether the bullet is off the screen
            yellows_bullets.remove(bullet)

    #checking whether whether any of reds bullets hit the yellow player 
    for bullet in reds_bullets:
        bullet.x -= BULLET_VEL
        if yellowPlayer.colliderect(bullet): #if the rec of bullet collided with the rect of yellowPlayer  
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            reds_bullets.remove(bullet)
        elif bullet.x < 0:
            reds_bullets.remove(bullet)



#displaying the winner
def display_winner(text):
    draw_text = WINNER_FONT.render(text,1 ,WHITE)
    WINDOW.blit(draw_text,(WIDTH//2 - draw_text.get_width()/2,HEIGHT//2 - draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000)



def main(): #this is the games mainloop
    redRect = pygame.Rect(700,200,55,40) #this rects are used to move the players
    yellowRect = pygame.Rect(300,200,55,40)

    #stores bullets for the players since they don't have an infinite amount of bullets
    red_bullets = []
    yellow_bullets = []

    #the players heath
    red_health = 10
    yellow_health = 10

    clock = pygame.time.Clock() #contains the function used to set the framerate

    run = True

    while run:
        clock.tick(FPS) #setting the framerate

        for event in pygame.event.get(): #returns all the pygame events
            if event.type == pygame.QUIT: #checks whether the close button on window is clicked and ends the loop
                run = False
                pygame.quit()
            #checking for keydowns to fire,using this method to ensure that the key can only be pressed once per frame
            if event.type == pygame.KEYDOWN:
                 if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS :
                    bullet = pygame.Rect(yellowRect.x + yellowRect.width,yellowRect.y + yellowRect.height//2, 10, 5) #spawned in the player middle
                    yellow_bullets.append(bullet)
                    SHOOT_SOUND.play()
                    

                 if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(redRect.x,redRect.y + redRect.height//2, 10, 5) 
                    red_bullets.append(bullet)
                    SHOOT_SOUND.play()
            
            #checking for collision using our user defined events
            if event.type == RED_HIT:
                red_health -= BULLET_DAMAGE
            if event.type == YELLOW_HIT:
                yellow_health -= BULLET_DAMAGE
        winner_text = ''
        if red_health <= 0:
            winner_text = 'Yellow wins!'
        if yellow_health <= 0:
            winner_text = 'Red wins!'

        if winner_text != '':
            display_winner(text=winner_text)
            break

        draw_window(yellowRect,redRect,red_bullets=red_bullets,yellow_bullets=yellow_bullets,red_health=red_health,yellow_health=yellow_health) #passing the Rect objects as arguments
        keys_pressed = pygame.key.get_pressed() #returns all keys that are currently pressed
        yellow_handle_movement(keys_pressed=keys_pressed,yellowRect=yellowRect) #passing the required arguments for the movement function
        red_handle_movement(keys_pressed=keys_pressed,redRect=redRect)
        bullet_handle(reds_bullets=red_bullets,yellows_bullets=yellow_bullets,redPlayer=redRect,yellowPlayer=yellowRect)
    

    main()


main()