# -*- coding: utf-8 -*-
"""
Created on Thurs Oct 15 21:12:35 2020

@author: Ben Vanderlei
"""
import pygame
import blaster_utils as bu
import random

NUM_TARGETS = 50
BLACK = 0,0,0
WHITE = 255,255,255
RED = 200,0,0
YELLOW = 255,255,0

        
pygame.init()

screen_width = 1200
screen_height = 600
screen = pygame.display.set_mode([screen_width,screen_height])
pygame.display.set_caption("Rock Blaster")

joystick_count = pygame.joystick.get_count()
if joystick_count == 0:
    print("Joystick not detected!")
else:
    my_joystick = pygame.joystick.Joystick(0)
    my_joystick.init()
        

block_list = pygame.sprite.Group()
bullet_list = pygame.sprite.Group()
all_sprites_list = pygame.sprite.Group()


rock_sheet = bu.SpriteSheet("images/rock_ani.png")
rock_image = rock_sheet.get_image(0,0,16,16)

for i in range(NUM_TARGETS):
    target = bu.Block(RED,20,20)
    target.image = rock_image
    target.rect.x = random.randrange(0,screen_width)
    target.rect.y = random.randrange(0,screen_height-50)
    
    block_list.add(target)
    all_sprites_list.add(target)

ship_sheet = bu.SpriteSheet("images/ship_ani.png")

player = bu.Ship(ship_sheet)
all_sprites_list.add(player)

done = False
clock  = pygame.time.Clock()
score = 0
player.rect.x = 100
player.rect.y = screen_height-100

while not done:
    
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

    # Update the bullets:
    for bullet in bullet_list:
        bullet.rect.y -= 3
        # Check for hits
        hit_list = pygame.sprite.spritecollide(bullet,block_list,True)

        for block in hit_list:
            bullet_list.remove(bullet)
            all_sprites_list.remove(bullet)
            score += 1
            print(score)

        if bullet.rect.y < -10:
            bullet_list.remove(bullet)
            all_sprites_list.remove(bullet)
    
                       
    screen.fill(BLACK)
    
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
    

    all_sprites_list.draw(screen)
    
    clock.tick(60)    
    pygame.display.flip()
    
pygame.quit()
    


