# -*- coding: utf-8 -*-
"""
Created on Thurs Oct 15 21:12:35 2020

@author: Ben Vanderlei
"""
import pygame
import blaster_utils as bu
import random

NUM_ROCKS = 50
SPEED = 2
BLACK = 0,0,0
WHITE = 255,255,255
RED = 200,0,0
YELLOW = 255,255,0

        
pygame.init()

screen_width = 1200
screen_height = 600
screen = pygame.display.set_mode([screen_width,screen_height])
pygame.display.set_caption("Rock Blaster")
font = pygame.font.SysFont('Calibri',25,True,False)

shoot_sound = pygame.mixer.Sound("sounds/laser.ogg")

joystick_count = pygame.joystick.get_count()
if joystick_count == 0:
    print("Joystick not detected!")
else:
    my_joystick = pygame.joystick.Joystick(0)
    my_joystick.init()
        

rock_list = pygame.sprite.Group()
bullet_list = pygame.sprite.Group()
all_sprites_list = pygame.sprite.Group()


rock_sheet = bu.SpriteSheet("images/rock_ani.png")
#rock_image = rock_sheet.get_image(0,0,16,16)

for i in range(NUM_ROCKS):
    rock = bu.Rock(rock_sheet)
    rock.rect.x = random.randrange(8,screen_width-8)
    rock.rect.y = random.randrange(0,screen_height-100)
    
    rock_list.add(rock)
    all_sprites_list.add(rock)

ship_sheet = bu.SpriteSheet("images/Blaster_Ship.png")

player = bu.Ship(ship_sheet)
all_sprites_list.add(player)


done = False
clock  = pygame.time.Clock()
score = 0
player.rect.x = 100
player.rect.y = screen_height-100

while not done:


    ###############################################################        
    # HANDLE EVENTS
    ###############################################################        
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
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

        # Add restrictions here to limit player on screen
        if player.rect.x > 3 and horiz_axis_pos < 0:
            player.rect.x += int(horiz_axis_pos*5)
        if player.rect.x < screen_width - 32 and horiz_axis_pos > 0:
            player.rect.x += int(horiz_axis_pos*5)
        if player.rect.y < screen_height - 36 and vert_axis_pos > 0:
            player.rect.y += int(vert_axis_pos*5)
        if player.rect.y > screen_height - 100 and vert_axis_pos < 0:
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
            new_rock.rect.x = random.randrange(8,screen_width-8)
            new_rock.rect.y = -16
    
            rock_list.add(new_rock)
            all_sprites_list.add(new_rock)
            
            
        if bullet.rect.y < -10:
            bullet_list.remove(bullet)
            all_sprites_list.remove(bullet)
    

                
    player.update(screen_width,screen_height)
    for rock in rock_list:
        rock.update(screen_width,screen_height)
        if rock.rect.y > screen_height:
            rock_list.remove(rock)
            all_sprites_list.remove(rock)
            #Create a new rock
            new_rock = bu.Rock(rock_sheet)
            new_rock.rect.x = random.randrange(8,screen_width-8)
            new_rock.rect.y = -16
    
            rock_list.add(new_rock)
            all_sprites_list.add(new_rock)

    ###############################################################        
    # DRAW NEW FRAME 
    ###############################################################        

    screen.fill(BLACK)
    all_sprites_list.draw(screen)

    score_msg = font.render("SCORE:  "+str(score),True,WHITE)
    screen.blit(score_msg,[16,16])         
    if (player.blast):
        pygame.draw.circle(screen,YELLOW,[player.rect.x+16,player.rect.y],10)
        player.blast = False
        
    clock.tick(60)    
    pygame.display.flip()
    
pygame.quit()
    


