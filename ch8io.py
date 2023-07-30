from typing import Optional
import pygame
from pygame.locals import *

SCREEN_FACTOR = 20
BLACK = (0, 0, 0)
WHITE = (0xFF, 0xFF, 0xFF)

KEYMAP = {
    0x0: K_x,
    0x1: K_1,
    0x2: K_2,
    0x3: K_3,
    0x4: K_q,
    0x5: K_w,
    0x6: K_e,
    0x7: K_a,
    0x8: K_s,
    0x9: K_d,
    0xA: K_z,
    0xB: K_c,
    0xC: K_4,
    0xD: K_r,
    0xE: K_f,
    0xF: K_v,
}

display: Optional[pygame.Surface] = None

def display_clear():
    display.fill(BLACK)
    pygame.display.flip()

def display_init():
    global display
    display = pygame.display.set_mode((64*SCREEN_FACTOR, 32*SCREEN_FACTOR))
    display_clear()

def display_draw(x, y, group):
    for i in range(8):
        rect = pygame.Rect((x + i)* SCREEN_FACTOR, y * SCREEN_FACTOR, SCREEN_FACTOR, SCREEN_FACTOR)
        color = WHITE if group & 0x80 else BLACK
        group <<= 1
        pygame.draw.rect(display, color, rect)
    pygame.display.flip()

def keyboard_check(key, cond):
    return pygame.key.get_pressed()[KEYMAP[key]] == cond

def keyboard_wait(key):
    pygame.event.clear()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key in KEYMAP.values():
                return [key for key in KEYMAP if KEYMAP[key]==event.key][0]

if __name__ == '__main__':
    pygame.init()
    display_init()
    display_draw(0,0, 0xAF)
    display_draw(1,1, 0xF0)
    display_draw(2,3, 0xA5)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
