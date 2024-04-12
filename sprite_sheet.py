# loop through a list

import pygame as pg

clock = pg.time.Clock()
frames = ["frame1", "frame2", "frame3", "frame4"]

# print(len(frames))


frames_length = len(frames)
# print(frames[frames_length-1])

# current_frame = 0
# print(current_frame%frames_length)
# current_frame += 1
# print(current_frame%frames_length)
# current_frame += 1
# print(current_frame%frames_length)
# current_frame += 1
# print(current_frame%frames_length)
# current_frame += 1
# print(current_frame%frames_length)
FPS = 30
then = 0
current_frame = 0

while True:
    # current_frame +=1
    # frames = ["frame1", "frame2", "frame3", "frame4"]
    # frames_length = len(frames)
    # print(current_frame%frames_length)
    now = pg.time.get_ticks()
    clock.tick(FPS)
    if now - then > 250:
        print(now)
        then = now
        current_frame += 1
        print(frames[current_frame%frames_length])

#write a loop that prints in terminal for each frame