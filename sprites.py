# This file was created by: Khoi Pham

# import modules
import pygame as pg
from pygame.sprite import Group, Sprite
from settings import *

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
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.hitpoints = 100 #use this later
        self.bullets = pg.sprite.Group()

    def shoot(self):
        keys = pg.key.get_pressed()
        if keys [pg.K_SPACE]:
            bullet = Bullet(self.game, self.rect.centerx, self.rect.centery, 'up')  # Adjust direction as needed
            self.game.all_sprites.add(bullet)
            self.bullets.add(bullet)
            print("shot's fired")


    # def move(self, dx=0, dy = 0):
    # self.x += dx
        #self. y +=dy
    
    # MOVEMENT with WASD
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
            print("sobad")

    def shoot_bullet(self):
    #     # draw bullets when click space
        pass     

 

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
        self.shoot()
        

# create a wall class

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
        # self.collide_with_walls('x')
        # self.collide_with_walls('y')
        # self.collide_with_eachother(self.game.enemy, 'enemy')
        


# def collide_with_enemy(self, group, kill, desc):
#         hits = pg.sprite.spritecollide(self, group, kill)
#         if hits and desc == "enemy":
#             self.rect == self.image.get_rect()
   

#Making bullets
class Bullet(Sprite):
    def __init__(self, game, x, y , direction):
        super().__init__() # super allows access to methods and properties of a parent or sibling class
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill((YELLOW))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 5
        self.direction = direction #gives direction
        
    

    def update(self):
        if self.direction == 'up':
            self.rect.y -= self.speed
        elif self.direction == 'down':
            self.rect.y += self.speed
        elif self.direction == 'left':
            self.rect.x -= self.speed
        elif self.direction == 'right':
            self.rect.x += self.speed
