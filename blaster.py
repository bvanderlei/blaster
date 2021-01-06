# -*- coding: utf-8 -*-
"""
Created on Thurs Oct 15 21:12:35 2020

@author: Ben Vanderlei
"""
import pygame
import blaster_utils as bu
import random, sys

#             R    G    B
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (200,   0,   0)
GREEN     = (  0, 200,   0)
YELLOW    = (255, 255,   0)
DARKGREEN = (  0, 155,   0)
DARKGRAY  = ( 40,  40,  40)
BGCOLOR = BLACK

## Game parameters
NUM_ROCKS = 50
NUM_STARS = 100
MAX_STAR_RADIUS = 3
SPEED = 2
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600


def main():
    global SCREEN, GAMEFONT
    global joystick_count, my_joystick
    pygame.init()
    SCREEN = pygame.display.set_mode([SCREEN_WIDTH,SCREEN_HEIGHT])
    pygame.display.set_caption("Rock Blaster")
    GAMEFONT = pygame.font.SysFont('Calibri',25,True,False)

    joystick_count = pygame.joystick.get_count()
    if joystick_count == 0:
        print("Joystick not detected!")
        terminate()
    else:
        my_joystick = pygame.joystick.Joystick(0)
        my_joystick.init()

    showStartScreen()
    while True:
        runGame()
        showGameOver()
        
def runGame():

    status_msg = GAMEFONT.render("STATUS",True,WHITE)
    status_bar = pygame.Rect(96,16+4,54,10)
    shoot_sound = pygame.mixer.Sound("sounds/laser.ogg")
    collision_sound = pygame.mixer.Sound("sounds/collision_sound.ogg")
    ship_sound = pygame.mixer.music.load("sounds/ship_sound.ogg")
    pygame.mixer.music.set_endevent(pygame.USEREVENT)

    pygame.mixer.music.play(loops = -1)
    
    rock_list = pygame.sprite.Group()
    bullet_list = pygame.sprite.Group()
    all_sprites_list = pygame.sprite.Group()
    star_list = []
    
    rock_sheet = bu.SpriteSheet("images/rock_ani.png")
    #rock_image = rock_sheet.get_image(0,0,16,16)

    for i in range(NUM_ROCKS):
        rock = bu.Rock(rock_sheet)
        rock.rect.x = random.randrange(8,SCREEN_WIDTH-8)
        rock.rect.y = random.randrange(0,SCREEN_HEIGHT-100)

        rock_list.add(rock)
        all_sprites_list.add(rock)

    for i in range(NUM_STARS):
        x = random.randrange(0,SCREEN_WIDTH)
        y = random.randrange(0,SCREEN_HEIGHT)
        size = random.randrange(1,MAX_STAR_RADIUS)
        random_brightness = random.randrange(50,200)
        color = (random_brightness,random_brightness,random.randrange(50,200))
        new_star = bu.Star(x,y,size,color)
        star_list.append(new_star)
        
        
    ship_sheet = bu.SpriteSheet("images/Blaster_Ship.png")

    player = bu.Ship(ship_sheet)
    all_sprites_list.add(player)

    clock  = pygame.time.Clock()
    score = 0
    health = 5
    player.rect.x = 100
    player.rect.y = SCREEN_HEIGHT-100

    while True:

        ###############################################################        
        # HANDLE EVENTS
        ###############################################################        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.JOYBUTTONDOWN:
                if my_joystick.get_button(2):
                    bullet = bu.Bullet()
                    bullet.rect.x = player.rect.x+14
                    bullet.rect.y = player.rect.y
                    all_sprites_list.add(bullet)
                    bullet_list.add(bullet)
                    shoot_sound.play()
                    player.blast = True

        if(joystick_count != 0):
            horiz_axis_pos = my_joystick.get_axis(0)
            vert_axis_pos = my_joystick.get_axis(1)

            # Add restrictions here to limit player on SCREEN
            if player.rect.x > 3 and horiz_axis_pos < 0:
                player.rect.x += int(horiz_axis_pos*5)
            if player.rect.x < SCREEN_WIDTH - 32 and horiz_axis_pos > 0:
                player.rect.x += int(horiz_axis_pos*5)
            if player.rect.y < SCREEN_HEIGHT - 36 and vert_axis_pos > 0:
                player.rect.y += int(vert_axis_pos*5)
            if player.rect.y > SCREEN_HEIGHT - 100 and vert_axis_pos < 0:
                player.rect.y += int(vert_axis_pos*5)
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    player.vy = SPEED
                if event.key == pygame.K_UP:
                    player.vy = -SPEED
                if event.key == pygame.K_LEFT:
                    player.vx = -SPEED
                if event.key == pygame.K_RIGHT:
                    player.vx = SPEED
                if event.key == pygame.K_SPACE:
                    bullet = bu.Bullet()
                    bullet.rect.x = player.rect.x+14
                    bullet.rect.y = player.rect.y

                    all_sprites_list.add(bullet)
                    bullet_list.add(bullet)

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    player.vy = 0
                if event.key == pygame.K_UP:
                    player.vy = 0
                if event.key == pygame.K_LEFT:
                    player.vx = 0
                if event.key == pygame.K_RIGHT:
                    player.vx = 0

        ###############################################################        
        # UPDATE GAME STATUS
        ###############################################################        

        # Update the bullets:
        for bullet in bullet_list:
            bullet.rect.y -= 3
            # Check for hits
            hit_list = pygame.sprite.spritecollide(bullet,rock_list,True)

            for rock in hit_list:
                bullet_list.remove(bullet)
                all_sprites_list.remove(bullet)
                all_sprites_list.remove(rock)
                score += 1
                #Create a new rock
                new_rock = bu.Rock(rock_sheet)
                new_rock.rect.x = random.randrange(8,SCREEN_WIDTH-8)
                new_rock.rect.y = -16

                rock_list.add(new_rock)
                all_sprites_list.add(new_rock)


            if bullet.rect.y < -10:
                bullet_list.remove(bullet)
                all_sprites_list.remove(bullet)

        ship_hit_list = pygame.sprite.spritecollide(player,rock_list,True)
        for rock in ship_hit_list:
            all_sprites_list.remove(rock)
            health -= 1
            collision_sound.play()
            if health == 0:
                pygame.mixer.music.stop()
                return
            #Create a new rock
            new_rock = bu.Rock(rock_sheet)
            new_rock.rect.x = random.randrange(8,SCREEN_WIDTH-8)
            new_rock.rect.y = -16

        player.update(SCREEN_WIDTH,SCREEN_HEIGHT)

        for rock in rock_list:
            rock.update(SCREEN_WIDTH,SCREEN_HEIGHT)
            if rock.rect.y > SCREEN_HEIGHT:
                rock_list.remove(rock)
                all_sprites_list.remove(rock)
                #Create a new rock
                new_rock = bu.Rock(rock_sheet)
                new_rock.rect.x = random.randrange(8,SCREEN_WIDTH-8)
                new_rock.rect.y = -16

                rock_list.add(new_rock)
                all_sprites_list.add(new_rock)

        ###############################################################        
        # DRAW NEW FRAME 
        ###############################################################        

        SCREEN.fill(BLACK)

        new_stars_needed = []
        for star in star_list:
            pygame.draw.circle(SCREEN,star.color,[star.x,star.y],star.size)
            star.update()
            ## Reset star when it reaches bottom of screen
            if star.y > SCREEN_HEIGHT:
                new_stars_needed.append(star)

        for star in new_stars_needed:
            star_list.remove(star)
        for star in new_stars_needed:
            brightness = random.randrange(50,200)
            x = random.randrange(0,SCREEN_WIDTH)
            y = 0
            size = random.randrange(1,MAX_STAR_RADIUS)
            color = (brightness,brightness,random.randrange(50,200))
            new_star = bu.Star(x,y,size,color)
            star_list.append(new_star)
            
        all_sprites_list.draw(SCREEN)

        score_msg = GAMEFONT.render("SCORE  "+str(score),True,WHITE)
        SCREEN.blit(score_msg,[16,38])         
        health_bar = pygame.Rect(98,16+6,health*2,6)
        SCREEN.blit(status_msg,[16,16])

        pygame.draw.rect(SCREEN,WHITE,status_bar)
        pygame.draw.rect(SCREEN,RED,health_bar)

        if (player.blast):
            pygame.draw.circle(SCREEN,YELLOW,[player.rect.x+16,player.rect.y],10)
            player.blast = False

        clock.tick(60)    
        pygame.display.flip()

def showGameOver():
    SCREEN.fill(BLACK)
    gameOverFont = pygame.font.Font('freesansbold.ttf', 50)
    gameSurf = gameOverFont.render('Game', True, WHITE)
    overSurf = gameOverFont.render('Over', True, WHITE)
    restartFont = pygame.font.Font('freesansbold.ttf', 25)
    restartSurf = restartFont.render('Press START to play again.', True, WHITE)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    restartRect = restartSurf.get_rect()
    gameRect.midtop = (SCREEN_WIDTH / 2, 200)
    overRect.midtop = (SCREEN_WIDTH / 2, gameRect.height + 200 + 25)
    restartRect.midtop = (SCREEN_WIDTH / 2, 2*gameRect.height + 200 + 50)    

    SCREEN.blit(gameSurf, gameRect)
    SCREEN.blit(overSurf, overRect)
    SCREEN.blit(restartSurf, restartRect)    

    pygame.display.flip()
    pygame.time.wait(500)

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.JOYBUTTONDOWN:
                if my_joystick.get_button(7):
                    return

def showStartScreen():
    SCREEN.fill(BLACK)
    gameOverFont = pygame.font.Font('freesansbold.ttf', 50)
    gameSurf = gameOverFont.render('Rock', True, WHITE)
    overSurf = gameOverFont.render('Blaster', True, WHITE)
    restartFont = pygame.font.Font('freesansbold.ttf', 25)
    restartSurf = restartFont.render('Press START', True, WHITE)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    restartRect = restartSurf.get_rect()
    gameRect.midtop = (SCREEN_WIDTH / 2, 200)
    overRect.midtop = (SCREEN_WIDTH / 2, gameRect.height + 200 + 25)
    restartRect.midtop = (SCREEN_WIDTH / 2, 2*gameRect.height + 200 + 50)    

    SCREEN.blit(gameSurf, gameRect)
    SCREEN.blit(overSurf, overRect)
    SCREEN.blit(restartSurf, restartRect)    

    pygame.display.flip()
    pygame.time.wait(500)

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.JOYBUTTONDOWN:
                if my_joystick.get_button(7):
                    return

def terminate():
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
