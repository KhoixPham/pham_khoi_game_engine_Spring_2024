# This file was created by Khoi Pham

#Write a function that takes two arguments and multiplies them
# USe a return statement
# Print it

#Write another function that converts the return from the first to a string and prints it out in a statement with concatenation

import pygame as pg


def myfunction(x, y):
    return x*y

def printer(t):
    return str(t) + " I can concatenate"
print(myfunction(10,50,))
print(printer(myfunction(10,50)))
    
i = 0
while True:
    print("this will happen 10 times")
    i += 1
    if i > 10:
        break

j = 0

while j < 10:
    print(printer(myfunction(50,50)))
    j += 1