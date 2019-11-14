#! /usr/bin/python
import pygame, sys
import mastermind as mm
import numpy as np


screen = pygame.display.set_mode((480, 720))

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            sys.exit(0)
