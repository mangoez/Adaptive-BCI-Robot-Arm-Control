import pygame
from random import seed
import random
from random import randint
import numpy as np
from argparse import ArgumentParser
from datetime import datetime
import matplotlib.pyplot as plt
from datetime import datetime
from pygame.locals import *
import pandas as pd
import socket

localIP = "127.0.0.1"
localPort = 12345
bufferSize  = 1024

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
print("UDP server up")

# set up stuff
y = []
colour = (102, 0, 204)

# Pygame stuff
def redraw_bg(surface):
    surface.fill((0, 0, 0))
    pygame.draw.circle(surface, (160, 160, 160), (840,525), 50)

def draw_black(surface):
    surface.fill((0,0,0))

def draw_stimuli(surface, direction):
    draw_black(surface)
    x = 525
    y = 250
    direction = int(direction)
    if (direction == 1):
        print('Right')
        #surface.blit(right, (x,y))
    #     pygame.draw.polygon(surface, (160, 160, 160), ((400, 500), (400, 550), (1300, 550), (1300, 625), (1400, 530), (1300, 430), (1300, 500)))
    #     y.append(1)
    elif (direction == -1):
        print('Left')
        #surface.blit(left, (x,y))
    #     pygame.draw.polygon(surface, (160, 160, 160), ((400, 500), (400, 430), (300, 525), (399, 620), (400, 550), (1300, 550), (1300, 500)))
    #     y.append(-1)
    else:
        print('TOO MANY CLASSES')
        None

def countdown(surface, sec):
    x = 750
    y = 300
    surface.fill((0, 0, 0))
    myfont = pygame.font.SysFont('Comic Sans MS', 300)

    for i in range(sec, 0, -1):
        surface.fill((0, 0, 0))
        text = myfont.render(str(i), False, (160, 160, 160))
        surface.blit(text,(x, y))
        pygame.display.update()
        pygame.time.delay(1000)

def accept_direction(surface, event):
    draw_black(surface)
    myfont = pygame.font.SysFont('Comic Sans MS', 300)

    if event == 0:
        text = myfont.render('Rest', False, colour)
    elif event == -1:
        text = myfont.render('Left', False, colour)
    else:
        text = myfont.render('Right', False, colour)

    surface.blit(text,(500, 300))
    pygame.display.update()
    pygame.time.delay(3500)
    

    pygame.event.clear()
    key_not_pressed = True
    answer = 0
    # while key_not_pressed:
    #     for event in pygame.event.get():
    #         if event.type == QUIT:
    #             pygame.quit()
    #             sys.exit()
    #         if event.type == KEYDOWN:
    #             key_not_pressed = False

    return None

def record_now():
    # Initialise shit
    n_trials = 50
    # directions = [1]*n_trials + [-1]*n_trials
    directions_first = [(((i%2)*2) - 1) for i in list(range(n_trials))]
    directions_second = directions_first.copy()
    random.shuffle(directions_second)

    directions = directions_first + directions_second 
    print("ALL DIRECTIONS: ", directions)
    np.savetxt('DIY_EEG/all_directions.csv', directions, delimiter=',')

    
    # Initialise Pygame
    pygame.init()
    win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    # win = pygame.display.set_mode((1620, 800))

    pygame.display.set_caption("MI stimulation")


    countdown(win, 2)
    for direct in directions:
        draw_black(win)
        print("DIRECTION: ", direct)
        pygame.display.update()
        
        # Motor imagery for 3.5 seconds
        accept_direction(win, direct) # Receive input from user
        pygame.display.update()

        # Rest for 2.5 seconds
        draw_black(win)
        pygame.display.update()
        pygame.time.delay(2500)

        # Now EEG can take the 7 second window
        bytesToSend = str.encode(str(direct))
        UDPServerSocket.sendto(bytesToSend, (localIP, localPort))

        # Add random rest
        pygame.time.delay(randint(500, 1000))
        
        draw_black(win)
        pygame.display.update()

    # Finish
    bytesToSend = str.encode(str(0))
    UDPServerSocket.sendto(bytesToSend, (localIP, localPort))

if __name__ == "__main__":
    # Start recording stuff
    record_now()
    pygame.quit()
