import pygame
from pygame.locals import *
from math import *
import re

pygame.init()

display_width = 1000
display_height = 720

display = pygame.display.set_mode((display_width, display_height))

clock = pygame.time.Clock()
fps = 30

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

MODIFIERS = ("alt", "ctrl", "escape", "meta", "shift", "tab", "windows")

font = pygame.font.Font(None, 20)


def main():
    func = ""
    scale = 10
    holding = set()
    origin = [display_width / 2, display_height / 2]

    while True:

        # keyboard controls
        for event in pygame.event.get():
            if event.type == QUIT:
                quit_all()
            if event.type == KEYDOWN:
                # holding down the modifier keys
                key_name = pygame.key.name(event.key)
                for modifier in MODIFIERS:
                    if modifier in key_name:
                        holding.add(modifier)
                        break
                else:
                    # special operations
                    if "meta" in holding:
                        if event.key == K_q:
                            quit_all()
                        elif event.key == K_MINUS:
                            scale *= 2
                        elif event.key == K_EQUALS:
                            scale /= 2
                        elif event.key == K_BACKSPACE:
                            func = ""
                    elif "shift" in holding:
                        if event.key == K_6:
                            func += '**'
                        elif event.key == K_8:
                            func += '*'
                        elif event.key == K_9:
                            func += '('
                        elif event.key == K_0:
                            func += ')'
                        elif event.key == K_EQUALS:
                            func += '+'
                    elif event.key == K_BACKSPACE:
                        if func:
                            func = func[:-1]
                    elif event.key == K_SPACE:
                        func += ' '
                    else:
                        func += key_name
            if event.type == KEYUP:
                # releasing the modifier keys
                key_name = pygame.key.name(event.key)
                for modifier in MODIFIERS:
                    if modifier in key_name:
                        holding.remove(modifier)
                        break
                else:
                    pass

        # display
        display.fill(WHITE)

        bitmap = font.render("y = " + func, True, BLACK)
        display.blit(bitmap, (10, 10))

        pygame.draw.line(display,
                         RED,
                         (0, origin[1]),
                         (display_width, origin[1]))
        pygame.draw.line(display,
                         RED,
                         (origin[0], 0),
                         (origin[0], display_height))

        # draw graph of function
        old_pos = (0, 0)
        drawability = display_width
        for pixel_x in range(0, display_width):
            try:
                x = (pixel_x - display_width / 2) / scale
                y = eval(func)
                pixel_y = int(display_height / 2 - y * scale)
                if pixel_x - old_pos[0] == 1 and 0 < old_pos[1] < display_height:
                    pygame.draw.line(display,
                                     BLACK,
                                     old_pos,
                                     (pixel_x, pixel_y))
                old_pos = (pixel_x, pixel_y)
            except:
                drawability -= 1
        # display drawability message
        if not drawability:
            bitmap = font.render("this function not drawable", True, BLACK)
            display.blit(bitmap, (10, 30))
        elif drawability != display_width:
            bitmap = font.render("this function not consistant", True, BLACK)
            display.blit(bitmap, (10, 30))

        pygame.display.flip()

        clock.tick(fps)


def quit_all():
    pygame.quit()
    quit()

def error():
    pass

try:
    main()
except:
    error()
