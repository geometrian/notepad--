#Imports

try:
    from Tkinter import Tk
    from tkFileDialog import askopenfilename
    py = 2
    inp = raw_input
except:
    import tkinter
    from tkinter.filedialog import askopenfilename
    py = 3
    inp = input

import pygame
from pygame.locals import *

import sys, os, traceback

from _helpers import *



#Settings

screen_size = [1024,768]

key_repeat = [300,20] #initial and subsequent delay, in ms

slider_width = 15 #pixels

font_path_or_search_name = "consolas"
font_size = 12



#Get filename

#   http://stackoverflow.com/a/3579625/688624
#   http://stackoverflow.com/a/3579783/688624
if py == 2:
    Tk().withdraw()
else:
    tkinter.Tk().withdraw()
filename = askopenfilename()

if filename == "":
    sys.exit(0)



#Initialize libraries

##if sys.platform in ["win32","win64"]: os.environ["SDL_VIDEO_CENTERED"]="1"

pygame.display.init()
pygame.font.init()

pygame.key.set_repeat(*key_repeat)

font = pygame.font.SysFont(font_path_or_search_name,font_size)

icon = pygame.Surface((1,1)); icon.set_alpha(0); pygame.display.set_icon(icon)
pygame.display.set_caption("notepad--")
surface = pygame.display.set_mode(screen_size,RESIZABLE)



#Load file

try:
    file = open(filename,"r")
    data = file.read()
    file.close()
except:
    print("Could not open file \"%s\"!"%filename)
    sys.exit(-1)

lines = data.split("\n")



#Main

scroll = 0
scrolling = 0
scrolling_uneaten = 0

class Slider(object):
    def __init__(self):
        self.part = 0.0

        self.n = len(lines)

        self.y =            0
        self.w = slider_width
        self.h =            0

    def _update_part(self):
        self.y = int( self.part * (screen_size[1]-self.h) )

    def update_scroll(self):
        self.part = float(scroll) / float(self.n-1)
        self._update_part()

    def screen_collides(self, screen_y):
        return screen_y >= self.y and screen_y < self.y+self.h
    def screen_to_part(self, screen_y):
        assert self.h < screen_size[1]
        return clamp( float(screen_y-self.h/2.0)/float(screen_size[1]-self.h), 0.0,1.0 )
    def part_to_screen(self):
        return clamp(rndint(self.part * float(screen_size[1]-self.h) + self.h/2.0), 0,screen_size[1]-1)
    def click_toward(self, mouse_y):
        target = self.screen_to_part(mouse_y)
        if abs(target-self.part)<0.1: self.part=target
        else:
            if target>self.part: self.part+=0.1
            else:                self.part-=0.1
        self._update_part()
    def click_set(self, mouse_y):
        self.part = self.screen_to_part(mouse_y)
        self._update_part()
    def click_move(self, dy):
        self.click_set( self.part_to_screen() + dy )

    def draw(self):
        scrollable_pixels = font.get_height() * (self.n-1)
        bar_part = float(screen_size[1]) / float(scrollable_pixels+screen_size[1])
        self.h = int(bar_part * screen_size[1])
        if self.h<self.w: self.h=min([self.w,max([screen_size[1]-1,0])])

        pygame.draw.rect(surface, (255,)*3, (screen_size[0]-self.w,0,self.w,screen_size[1]))
        pygame.draw.line(surface, (225,)*3, (screen_size[0]-self.w,0),(screen_size[0]-15,screen_size[1]))
        pygame.draw.rect(surface, (192,)*3, (screen_size[0]-self.w,self.y,15,self.h))
slider = Slider()

def try_scroll_by(delta):
    global scroll
    scroll = clamp(scroll+delta, 0,len(lines)-1)
    slider.update_scroll()
def try_scroll_to(to):
    global scroll
    scroll = clamp(to, 0,len(lines)-1)
    slider.update_scroll()
frame = 0
def get_input():
    global scroll,scrolling,scrolling_uneaten, screen_size, surface, frame
    keys_pressed = pygame.key.get_pressed()
    mouse_buttons = pygame.mouse.get_pressed()
    mouse_position = pygame.mouse.get_pos()
    mouse_rel = pygame.mouse.get_rel()
    for event in pygame.event.get():
        if   event.type == QUIT: return False
        elif event.type == KEYDOWN:
            if   event.key == K_ESCAPE: return False
            elif event.key == K_g and (keys_pressed[K_LALT] or keys_pressed[K_RALT]):
                scroll = int(input("Go to line: "))
            elif event.key == K_PAGEDOWN:
                page_height_lines = screen_size[1] // font.get_height()
                try_scroll_by(  page_height_lines-1 )
            elif event.key == K_PAGEUP:
                page_height_lines = screen_size[1] // font.get_height()
                try_scroll_by(-(page_height_lines-1))
        elif event.type == MOUSEBUTTONDOWN:
            if   event.button == 1:
                if mouse_position[0] >= screen_size[0] - slider.w:
                    if slider.screen_collides(mouse_position[1]):
                        scrolling = 1
                        scrolling_uneaten = 0
                    else:
                        scrolling = 2
                        frame = rndint(0.300 * 60)
            elif event.button == 4:
                try_scroll_by(-5)
            elif event.button == 5:
                try_scroll_by( 5)
        elif event.type == MOUSEBUTTONUP:
            if   event.button == 1:
                scrolling = 0
        elif event.type == VIDEORESIZE:
            screen_size = list(event.size)
            surface = pygame.display.set_mode(screen_size,RESIZABLE)
    if scrolling == 1:
        if mouse_rel[1] != 0:
##            temp = scrolling_uneaten
            dy = scrolling_uneaten + mouse_rel[1]

            y0 = slider.y
            slider.click_move(dy)
            try_scroll_to(rndint( slider.part * slider.n ))
            y1 = slider.y

            scrolling_uneaten = dy - (y1-y0)
##            print("rel %d + accum %d = %d; moved %d->%d so new accum %d"%( mouse_rel[1],temp,dy, y0,y1, scrolling_uneaten))
    ##        slider.click_set(mouse_position[1])
    elif scrolling == 2:
        if frame == 0:
            slider.click_toward(mouse_position[1])
            try_scroll_to(rndint( slider.part * slider.n ))
            frame = rndint(0.100 * 60)
        else:
            frame -= 1

    return True

def draw():
    surface.fill((255,)*3)

    y = 0
    lines_drawn = 0
    for i in range(scroll,len(lines),1):
        num = font.render("% 5d|"%(i), True, (192,)*3)
        line = font.render(lines[i], True, (0,)*3)

        surface.blit(num, (0,y))
        surface.blit(line, (num.get_width(),y))

        lines_drawn += 1
        y += font.get_height()
        if y >= screen_size[1]:
            break

    slider.draw()

    pygame.display.flip()

def main():
    clock = pygame.time.Clock()
    while True:
        if not get_input(): break
        draw()
        clock.tick(60)
    pygame.quit()
if __name__ == "__main__":
    try:
        main()
    except:
        traceback.print_exc()
        pygame.quit()
        input()
