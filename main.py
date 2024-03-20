# This file was created by: Khoi Pham
# my first source control edit
# Importing libraries
import pygame as pg
import sys
from settings import *
from sprites import *
from os import path
import random

# Three things I want to add:
# Projectiles / bullets
# ENdless survival
# Aim with crosshair

#Add a math function to round down the clock
from math import floor
#test from a different computer!

#Initalize a class
class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(300, 100)
        self.load_data()
        self.wave_counter = 0 #this marks our initial value | allows the 'Game' object to have attribute to wave_counter
        self.enemy_spawned = 0 #game starts with 0 enemies

         # load save game data etc
    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'images')
        self.player_img = pg.image.load(path.join(img_folder, 'saitama.png')).convert_alpha()
        self.enemy_img = pg.image.load(path.join(img_folder, 'garou.png')).convert_alpha()
        self.coin_img = pg.image.load(path.join(img_folder, 'coin.png')).convert_alpha()
        self.map_data = []
        with open(path.join(game_folder, 'map.txt'), 'rt') as f:
            for line in f:
                self.map_data.append(line)
    
# def new_wave is from AI
# My own Comments
    def new_wave(self):
        self.wave_counter += 1 # += operator makes it easier to add a value to an existing variable
        num_enemies_to_spawn = 1 + (self.wave_counter - 1) * 1 # add one extra enemy per wave
        for _ in range(num_enemies_to_spawn): #spawns the enemy
            x = random.randint(0, 64 - TILESIZE)
            y = random.randint(0, 56 - TILESIZE)
            Enemy(self, x, y) # giving x and y the value to the enemy that is spawned
        
 
    def new(self):
            #init all variables, setup groups, instantiate classes
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.enemy = pg.sprite.Group()
        #self.player = Player(self, 10, 10)
        #for x in range(10,20):
               # Wall(self, x, 5)
        for row, tiles in enumerate(self.map_data):
            print(row)
            print(tiles)
            for col, tile, in enumerate(tiles):
                # print(col)
                # print(tiles)
                if tile == '1':
                    Wall(self, col, row)
                if tile == 'P': 
                    self.player = Player(self, col, row,)
                if tile == 'U':
                    Coin(self, col, row)
                if tile == 'E':
                    Enemy(self, col, row)
            
    # DEFINE THE RUN METHOD            
    def run(self):
      self.playing = True
      while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()
            
    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        self.all_sprites.update()
        #AI | My comments
        if len(self.enemy) == 0: #Says to the game to check if every enemy is dead
            self.enemy_spawned += 1 #spawns the enemy
            if self.enemy_spawned >= 1:
                self.new_wave()
        
    #DRAW GRID
    def draw_grid(self):
        for x in range(0,WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))
    
    #Draw text
    def draw_text(self):
        font = pg.font.Font(None, 36)
        wave_text = font.render(f"Wave: {self.wave_counter}", True, YELLOW) # the f is called an f-string | this displays self.wave_counter and its value after evaluation
        self.screen.blit(wave_text, (83,84)) #draws the text at specific coordinate

    #Define the draw method / OUTPUT
    def draw(self):
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        self.draw_text()
        pg.display.flip()

 # User input from keyboard                  
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.MOUSEBUTTONDOWN:
                x,y = pg.mouse.get_pos()
                print (x,y)
                bullet = Bullet(self.player.game, self.player.rect.centerx, self.player.rect.centery, x, y, 5)  # Adjust direction as needed
                self.player.game.all_sprites.add(bullet)
                self.player.bullets.add(bullet)
                bullets.append(bullet) #stores the bullet in a list | a list store multiple items in a single variable
    
                
               
            # if event.type == pg.KEYDOWN:
            #     if event.key == pg.K_LEFT:
            #         self.player.move(dx=-1)
            #     if event.key == pg.K_RIGHT:
            #         self.player.move(dx=1)
            #     if event.key == pg.K_UP:
            #         self.player.move(dy=-1)
            #     if event.key == pg.K_DOWN:
            #         self.player.move (dy=1)
            #     if event.key == pg.K_a:
            #         self.player.move(dx=-1)
            #     if event.key == pg.K_d:
            #         self.player.move(dx=1)
            #     if event.key == pg.K_w:
            #         self.player.move(dy=-1)
            #     if event.key == pg.K_s:
            #         self.player.move (dy=1)
    

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass        
        
# Instantiate the game      
g = Game()

while True:
    g.new()
    g.run()
    

g.run()

#USER INPUT FROM KEYBOARD
# data types: int, string, float, bool,
#g.show_go_screen)