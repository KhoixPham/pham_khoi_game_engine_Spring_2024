# This file was created by: Khoi Pham

# import modules
import pygame as pg
from pygame.sprite import Group, Sprite
from settings import *
import math

# create a player class

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        # init super class
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        # self.image = pg.Surface((TILESIZE, TILESIZE))
        # added player image to sprite from the game class
        self.image = game.player_img
        # self.image.fill(YELLOW)
        self.rect = self.image.get_rect(center=(x,y))
        self.vx, self.vy = 0, 0
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.hitpoints = 100 #use this later
        self.bullets = pg.sprite.Group()
        self.rect.center = (x,y)

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
    def collide_with_obj(self, group, kill, desc):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            if str(hits[0].__class__.__name__) == "Coin": 
                print("I got a coin")


            #if hits
        
        #if hits and desc == "coin":
            #self.rect = self.image.get_rect()

    def collide_with_enemy(self, group, kill, desc):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits and desc == "enemy":
            self.rect = self.image.get_rect()


 

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
        self.collide_with_obj(self.game.coins, True, "coin")
        self.rect.width = self.rect.width
        self.rect.height = self.rect.height
        self.collide_with_enemy(self.game.enemy, True, "enemy")
        
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
    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vx > 0:
                    self.rect.right = hits[0].rect.left
                if self.vx < 0:
                    self.rect.left = hits[0].rect.right
                self.vx = -self.vx  # Reverse the direction
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vy > 0:
                    self.rect.bottom = hits[0].rect.top
                if self.vy < 0:
                    self.rect.top = hits[0].rect.bottom
                self.vy = -self.vy  # Reverse the direction

    def update(self):
        # Store the current position (rect)
        current_rect = self.rect.copy()

        # Update position based on velocity
        self.rect.x += self.vx * self.game.dt
        self.rect.y += self.vy * self.game.dt

        # Check for collision with other enemies
        enemy_collisions = pg.sprite.spritecollide(self, self.groups[1], False)
        for enemy in enemy_collisions:
            if enemy != self:
                # Revert to previous position
                self.rect = current_rect
                self.vx = -self.vx
                self.vy = -self.vy

        # Follow player | Mr. Cozort
        if self.rect.x < self.game.player.rect.x:
            self.vx = ENEMY_SPEED
        elif self.rect.x > self.game.player.rect.x:
            self.vx = -ENEMY_SPEED
        else:
            self.vx = 0

        if self.rect.y < self.game.player.rect.y:
            self.vy = ENEMY_SPEED
        elif self.rect.y > self.game.player.rect.y:
            self.vy = -ENEMY_SPEED
        else:
            self.vy = 0

        # Apply wall collision
        self.collide_with_walls('x')
        self.collide_with_walls('y')
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
        self.image = pg.Surface((16, 16))
        self.image.fill((YELLOW))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        angle = math.atan2(targety-y, targetx-x) #calculate angle in radians / rise over run (targety-y, targetx-x)
        print('Angle in degrees:', angle*180/math.pi)
        self.dx = math.cos(angle) * speed
        self.dy = math.sin(angle) * speed
        self.x = x
        self.y = y
    
    #movement with bullet
    def move(self):
        # self.x and self.y are floats (decimals), i get better accuracy
        self.x = self.x + self.dx
        self.y = self.y + self.dy

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)


    #Make bullets kill enemies
    def collide_with_enemy(self, group, kill, desc):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits and desc == "enemy":
            self.rect = self.image.get_rect()
    

    def update(self):
        # self.rect.x += self.dx
        # self.rect.y += self.dy
        self.move()
        self.collide_with_enemy(self.game.enemy, True, 'enemy')