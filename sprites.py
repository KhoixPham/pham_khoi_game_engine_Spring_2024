# This file was created by: Khoi Pham

# import modules
import pygame as pg
from pygame.sprite import Group, Sprite
from settings import *
import math
from os import path

SPRITESHEET = "theBell.png"
game_folder = path.dirname(__file__)
img_folder = path.join(game_folder, 'images')
# create a player class
bosses = []

class Spritesheet:
    # utility class for loading and parsing spritesheets
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        # grab an image out of a larger spritesheet
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        # image = pg.transform.scale(image, (width, height))
        image = pg.transform.scale(image, (width * 1, height * 1))
        return image

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        # init super class
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        # self.image = pg.Surface((TILESIZE, TILESIZE))
        # added player image to sprite from the game class
        #self.image = game.player_img
        # self.image.fill(YELLOW)
        self.spritesheet = Spritesheet(path.join(img_folder, SPRITESHEET))
        self.load_images()
        self.image = self.standing_frames[0]
        self.rect = self.image.get_rect(center=(x,y))
        self.vx, self.vy = 0, 0
        self.current_frame = 0
        self.last_update = 0
        self.material = True
        self.jumping = False
        # needed for animated sprite
        self.walking = False
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.hitpoints = 500 #use this later
        self.bullets = pg.sprite.Group()
        self.rect.center = (x,y)
        self.powerup = PowerUp
        self.status = ""
        self.powerup_timer = None #allows the player to have access to these variables
        self.triple_timer = None

    def load_images(self):
        self.standing_frames = [self.spritesheet.get_image(0,0, 32, 32), 
                                self.spritesheet.get_image(32,0, 32, 32)]

    def animate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 350:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
            bottom = self.rect.bottom
            self.image = self.standing_frames[self.current_frame]
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom

    # def load_images(self):
    #     self.standing_frames = [self.spritesheet.get_image(0, 0, 32, 32),
    #                             self.spritesheet.get_image(32, 0, 32, 32)]
    #     for frame in self.standing_frames:
    #         frame.set_colorkey(BLACK)
    #     self.walk_frames_r = [self.spritesheet.get_image(678, 860, 120, 201),
    #                           self.spritesheet.get_image(692, 1458, 120, 207)]
    #     self.walk_frames_l = []
    #     for frame in self.walk_frames_r:
    #         frame.set_colorkey(BLACK)
    #         self.walk_frames_l.append(pg.transform.flip(frame, True, False))
    #     self.jump_frame = self.spritesheet.get_image(256, 0, 128, 128)
    #     self.jump_frame.set_colorkey(BLACK)

    # def events(self):
    #     for event in pg.event.get():
    #         if event.type == pg.MOUSEBUTTONDOWN:
    #             x,y = pg.mouse.get_pos()
    #             bullet = Bullet(self.game, self.rect.centerx, self.rect.centery, 'right')  # Adjust direction as needed
    #             self.game.all_sprites.add(bullet)
    #             self.bullets.add(bullet)
    #             bullets.append(bullet)
    #             pg.time.set_timer(pg.USEREVENT+1)

        

    # def shoot(self):
    #     if pg.MOUSEBUTTONDOWN:
    #         bullet = Bullet(self.game, self.rect.centerx, self.rect.centery, 'right')  # Adjust direction as needed
    #         self.game.all_sprites.add(bullet)
    #         self.bullets.add(bullet)
    #         bullets.append(bullet)
        #shoot with mouse

        #shoot in the direction Player is facing
        
        # keys = pg.key.get_pressed()
        # if keys [pg.K_SPACE]:
        #     if self.vx > 0:
        #         bullet = Bullet(self.game, self.rect.centerx, self.rect.centery, 'right')  # Adjust direction as needed
        #         self.game.all_sprites.add(bullet)
        #         self.bullets.add(bullet)
        #     if self.vx < 0:
        #         bullet = Bullet(self.game, self.rect.centerx, self.rect.centery, 'left')  
        #         self.game.all_sprites.add(bullet)
        #         self.bullets.add(bullet)
        #     if self.vy > 0:
        #         bullet = Bullet(self.game, self.rect.centerx, self.rect.centery, 'down')  
        #         self.game.all_sprites.add(bullet)
        #         self.bullets.add(bullet)
        #     if self.vy < 0:
        #         bullet = Bullet(self.game, self.rect.centerx, self.rect.centery, 'up')  
        #         self.game.all_sprites.add(bullet)
        #         self.bullets.add(bullet)
        #         bullets.append(bullet)
            
            


    # def move(self, dx=0, dy = 0):
    # self.x += dx
        #self. y +=dy
    
    # MOVEMENT with WASD and get Mouse Position
    def get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vx = -PLAYER_SPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vx = PLAYER_SPEED
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vy = -PLAYER_SPEED
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vy = PLAYER_SPEED
        if self.vx != 0 and self.vy !=0:
            self.vx *= 0.7071
            self.vy *= 0.7071

    

    # COLLISION       
    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y

# FROM MR. COZORT's CODE
    def collide_with_powerup(self, group, kill, desc):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits and desc == "powerup":
            self.status = "Infinite Bullets" 
            self.start_powerup_timer() #Powerup timer is from AI
            #sets a different player status | similar to creative mode / survival / adventure
        if self.status == "Infinite Bullets":
            #print("okay")
            x,y = pg.mouse.get_pos()
                #print (x,y)
            bullet = Bullet(self.game, self.rect.centerx, self.rect.centery, x, y, 5)  # Adjust direction as needed
            self.game.all_sprites.add(bullet)
            self.bullets.add(bullet)
            bullets.append(bullet)
    
    def collide_with_triple (self, group, kill, desc):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits and desc == "triple":
            self.status = "Infinite Bullets x3"
            self.start_triple_timer()
        if self.status == "Infinite Bullets x3":
            x,y = pg.mouse.get_pos()
            bullet = Bullet(self.game, self.rect.centerx, self.rect.centery, x, y, 5)  # Adjust direction as needed
            self.game.all_sprites.add(bullet)
            self.bullets.add(bullet)
            bullets.append(bullet)
            bullet = Bullet2(self.game, self.rect.centerx, self.rect.centery, x, y, 5)  # Adjust direction as needed
            self.game.all_sprites.add(bullet)
            self.bullets.add(bullet)
            bullets.append(bullet)
            bullet = Bullet3(self.game, self.rect.centerx, self.rect.centery, x, y, 5)  # Adjust direction as needed
            self.game.all_sprites.add(bullet)
            self.bullets.add(bullet)
            bullets.append(bullet)


    def start_powerup_timer(self):
        #AI
         # Set powerup timer 
        self.powerup_timer = pg.time.get_ticks()
            # if str(hits[0].__class__.__name__) == "powerup": 
            #     print("oadjfa")

        
        #if hits and desc == "coin":
            #self.rect = self.image.get_rect()
    
    def start_triple_timer(self):
        self.triple_timer = pg.time.get_ticks()

    def collide_with_enemy(self, group, kill, desc):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits and desc == "enemy":
            pass
    
    def collide_with_bosses(self, group, desc):
        hits = pg.sprite.spritecollide(self, group, False)
        if hits and desc == "bosses":
            self.hitpoints -= 1
        if self.hitpoints == 0:
            self.kill()

    def update(self):
        #self.rect.x = self.vx * TILESIZE
        #self.rect.y = self.vy * TILESIZE
        self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        #ADD X COLLISION
        self.collide_with_walls('x')
        self.rect.y = self.y
        #ADD Y COLLISION
        self.collide_with_walls ('y')
        self.collide_with_powerup(self.game.powerup, True, "powerup")
        self.collide_with_bosses(self.game.boss, "bosses")
        self.rect.width = self.rect.width
        self.rect.height = self.rect.height
        self.collide_with_enemy(self.game.enemy, True, "enemy")
        self.collide_with_triple(self.game.triple, True, "triple")
        self.animate()
        self.get_keys()
        if self.powerup_timer is not None and pg.time.get_ticks() - self.powerup_timer >= 5000: #5 Seconds
            self.status = "Triple Shot"
            self.powerup_timer = None  # Reset the timer
        if self.triple_timer is not None and pg.time.get_ticks() - self.triple_timer >= 3000:
            self.status = "Infinite Bullets" #After 3, switches to "Infinite Bullets"
            self.start_powerup_timer() #Starts the infinite timer powerup
            self.triple_timer = None # Reset the timer

            #Goes from 3 to infinite to normal triple shot
            

        
#------------------------------------------------------------------------
    # CREATE A WALL CLASS

class Wall(Sprite):
    # create init method for Wall
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        Sprite.__init__(self, self.groups)
        self.game = game
        self.hitpoints = 100
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(PURPLE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE

    # def collide_with_bullet(self, group, kill, desc):
    #     hits = pg.sprite.spritecollide(self, group, kill, desc)
    #     if hits and desc == "bullets":
    #         print("hello")
    # killing the bullets

    # def update(self):
    #     self.collide_with_bullet(self.game.bullets, True, bullets)
#------------------------------------------------------------------------
        #CREATE A COIN CLASS

class Coin(Sprite):
    # create init method for Wall
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.coins
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(RED)
        # self.rect = self.image.get_rect()
        self.image = game.coin_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE

#-------------------------------------------------------------------
        #Create an Enemy Class
        
class Enemy(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.enemy
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
      # self.image.fill(PURPLE)
        self.image = game.enemy_img
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.vx = ENEMY_SPEED
        self.vy = ENEMY_SPEED
    
    #Collision with walls
    # def collide_with_walls(self, dir):
    #     if dir == 'x':
    #         hits = pg.sprite.spritecollide(self, self.game.walls, False)
    #         if hits:
    #             if self.vx > 0:
    #                 self.rect.right = hits[0].rect.left
    #             if self.vx < 0:
    #                 self.rect.left = hits[0].rect.right
    #             self.vx = -self.vx  # Reverse the direction
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vy > 0:
                    self.rect.bottom = hits[0].rect.top
                if self.vy < 0:
                    self.rect.top = hits[0].rect.bottom
                self.vy = -self.vy  # Reverse the direction

    def update(self):
        #AI , From Tyler
        # Calculates direction vector to player and makes it follow player's center
        direction = pg.math.Vector2(self.game.player.rect.center) - pg.math.Vector2(self.rect.center)
        # Normalizes the direction vector and scales the enemy by speed
        if direction.length() > 0:
            self.vx, self.vy = direction.normalize() * 300
 
# multiplies velocity by delta time
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        #self.collide_with_walls('x')
        self.rect.y = self.y
        #self.collide_with_walls('y')
        # dies when hitpoints are gone
        # Apply wall collision
        # self.collide_with_walls('x')
        # self.collide_with_walls('y')
        # self.collide_with_eachother(self.game.enemy, 'enemy')
        


# def collide_with_enemy(self, group, kill, desc):
#         hits = pg.sprite.spritecollide(self, group, kill)
#         if hits and desc == "enemy":
#             self.rect == self.image.get_rect()
   
#-------------------------------------------------------------------
        
#Making bullets
#  # https://www.youtube.com/watch?v=3DeW-7vbc50&list=LL&index=2&t=887s
class Bullet(Player):
    def __init__(self, game, x, y, targetx, targety, speed):
        super().__init__(game, x, y) # super allows access to methods and properties of a parent or sibling class
        self.game = game
        self.groups = game.all_sprites, game.bullets
        self.image = pg.Surface((16, 16))
        self.image.fill((YELLOW))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        angle = math.atan2(targety-y, targetx-x) #calculate angle in radians / rise over run (targety-y, targetx-x) | atan = arc tangent
        #print('Angle in degrees:', angle*180/math.pi)
        self.dx = math.cos(angle) * speed
        self.dy = math.sin(angle) * speed
        self.x = x
        self.y = y
    
    #movement with bullet
    def move(self):
        # self.x and self.y are floats (decimals), i get better accuracy
        #IF I change self.x and and then convert them into integers for the rectangle
        self.x = self.x + self.dx
        self.y = self.y + self.dy

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        #print(self.rect.x)

        #Previous
        #self.rect.x = self.rect.x + int(self.dx)
        #self.rect.y = self.rect.x + int(self.dy)

    #Make bullets kill enemies
    def collide_with_enemy(self, group, kill, desc):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits and desc == "enemy":
            self.rect = self.image.get_rect()
    

    # Modified from CoPilot
    def collide_with_boss(self, group, desc):
        hits = pg.sprite.spritecollide(self, group, False)  # Change True to False
        if hits and desc == "bosses":
            # Check if the boss sprite's hit points reach zero
            for boss in hits:
                boss.hitpoints -= 5
                if boss.hitpoints <= 0:
                    # Remove the boss sprite when hit points reach zero
                    boss.kill()



    def update(self):
        # self.rect.x += self.dx
        # self.rect.y += self.dy
        self.move()
        self.collide_with_boss(self.game.boss,'bosses')
        self.collide_with_enemy(self.game.enemy, True, 'enemy')
        if self.rect.x > 1024:
            self.kill()
        if self.rect.y > 768:
            self.kill()
        if self.rect.x < -100:
            self.kill()
        if self.rect.y < -100:
            self.kill()
        
#_____________________________________________________________________________________________________

class Bullet2(Player):
    def __init__(self, game, x, y, targetx, targety, speed):
        super().__init__(game, x, y) # super allows access to methods and properties of a parent or sibling class
        self.game = game
        self.groups = game.all_sprites, game.bullets
        self.image = pg.Surface((16, 16))
        self.image.fill((YELLOW))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        angle = math.atan2(targety-y, targetx-x) #calculate angle in radians / rise over run (targety-y, targetx-x) | atan = arc tangent
        #print('Angle in degrees:', angle*180/math.pi)
        angle2 = angle + 0.2 # For triple shot, goes up when clicked instead of straight
        self.dx = math.cos(angle2) * speed
        self.dy = math.sin(angle2) * speed
        self.x = x
        self.y = y
    #movement with bullet
    def move(self):
        # self.x and self.y are floats (decimals), i get better accuracy
        #IF I change self.x and and then convert them into integers for the rectangle
        self.x = self.x + self.dx
        self.y = self.y + self.dy

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        #print(self.rect.x)

        #Previous
        #self.rect.x = self.rect.x + int(self.dx)
        #self.rect.y = self.rect.x + int(self.dy)

    #Make bullets kill enemies
    def collide_with_enemy(self, group, kill, desc):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits and desc == "enemy":
            self.rect = self.image.get_rect()

    def collide_with_boss(self, group, desc):
        hits = pg.sprite.spritecollide(self, group, False)  # Change True to False
        if hits and desc == "bosses":
            # Check if the boss sprite's hit points reach zero
            for boss in hits:
                boss.hitpoints -= 5
                if boss.hitpoints <= 0:
                    # Remove the boss sprite when hit points reach zero
                    boss.kill()


    def update(self):
        # self.rect.x += self.dx
        # self.rect.y += self.dy
        self.move()
        self.collide_with_enemy(self.game.enemy, True, 'enemy')
        self.collide_with_boss(self.game.boss, 'bosses')
        if self.rect.x > 1024:
            self.kill()
        if self.rect.y > 768:
            self.kill()
        if self.rect.x < -100:
            self.kill()
        if self.rect.y < -100:
            self.kill()

#-----------------------------------------------------------------------------------------------------

class Bullet3(Player):
    def __init__(self, game, x, y, targetx, targety, speed):
        super().__init__(game, x, y) # super allows access to methods and properties of a parent or sibling class
        self.game = game
        self.groups = game.all_sprites, game.bullets
        self.image = pg.Surface((16, 16))
        self.image.fill((YELLOW))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        angle = math.atan2(targety-y, targetx-x) #calculate angle in radians / rise over run (targety-y, targetx-x) | atan = arc tangent
        #print('Angle in degrees:', angle*180/math.pi)
        angle3 = angle - 0.2 #For triple shot, the bullet goes towards the downward direction when clicked
        self.dx = math.cos(angle3) * speed
        self.dy = math.sin(angle3) * speed
        self.x = x
        self.y = y

    #movement with bullet
    def move(self):
        # self.x and self.y are floats (decimals), i get better accuracy
        #IF I change self.x and and then convert them into integers for the rectangle
        self.x = self.x + self.dx 
        self.y = self.y + self.dy

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        #print(self.rect.x)

        #Previous
        #self.rect.x = self.rect.x + int(self.dx)
        #self.rect.y = self.rect.x + int(self.dy)

    #Make bullets kill enemies
    def collide_with_enemy(self, group, kill, desc):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits and desc == "enemy":
            self.rect = self.image.get_rect()
    
    def collide_with_boss(self, group, desc):
        hits = pg.sprite.spritecollide(self, group, False)  # Change True to False
        if hits and desc == "bosses":
            # Check if the boss sprite's hit points reach zero
            for boss in hits:
                boss.hitpoints -= 5
                if boss.hitpoints <= 0:
                    # Remove the boss sprite when hit points reach zero
                    boss.kill()
    def update(self):
        # self.rect.x += self.dx
        # self.rect.y += self.dy
        self.move()
        self.collide_with_boss(self.game.boss, 'boss')
        self.collide_with_enemy(self.game.enemy, True, 'enemy')
        if self.rect.x > 1024:
            self.kill()
        if self.rect.y > 768:
            self.kill()
        if self.rect.x < -100:
            self.kill()
        if self.rect.y < -100:
            self.kill()

#-----------------------------------------------------------------------------------------------------

class PowerUp(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.powerup
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE

class TriplePowerup(Sprite):
    def __init__(self,game,x,y):
        self.groups = game.all_sprites, game.triple
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(PINK)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE

#-------------------------------------------------------------------------------------------------------------------

class Boss(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.boss
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((128, 128))
      # self.image.fill(PURPLE)
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.vx = 200
        self.vy = 200
        self.hitpoints = 50000
        self.status = ''
        self.cd = 5000

    def update(self):
        #AI , From Tyler
        # Calculates direction vector to player and makes it follow player's center
        direction = pg.math.Vector2(self.game.player.rect.center) - pg.math.Vector2(self.rect.center)
        # Normalizes the direction vector and scales the enemy by speed
    
        if direction.length() > 0 and not self.cd > pg.time.get_ticks():
            self.vx, self.vy = direction.normalize() * 150 # From James
        if self.cd < pg.time.get_ticks():
            self.vx, self.vy = direction.normalize()* 500
            self.cd = pg.time.get_ticks() + 1000
# multiplies velocity by delta time
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        #self.collide_with_walls('x')
        self.rect.y = self.y