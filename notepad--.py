import pygame
from pygame.locals import *
import sys, os, traceback
##if sys.platform in ["win32","win64"]: os.environ["SDL_VIDEO_CENTERED"]="1"
pygame.display.init()
pygame.font.init()

screen_size = [1024,768]
icon = pygame.Surface((1,1)); icon.set_alpha(0); pygame.display.set_icon(icon)
pygame.display.set_caption("Text Viewer - Ian Mallett - v.1.0.0 - 2017")
surface = pygame.display.set_mode(screen_size,RESIZABLE)

pygame.key.set_repeat(300,20)

font = pygame.font.SysFont( ("consolas"), 12 )


file = open("bigfile.obj","r")
data = file.read()
file.close()

lines = data.split("\n")


scroll = 0
scrolling = 0
page_height = 0 #lines; set in draw

def clamp(num, low,high):
    if num< low: return  low
    if num>high: return high
    return num
def rndint(num):
    return int(round(num))

class Slider(object):
    def __init__(self):
        self.part = 0.0

        self.n = len(lines)
        
        self.y =  0
        self.w = 15
        self.h =  0

    def update_scroll(self):
        self.part = float(scroll) / float(self.n-1)

    def screen_collides(self, screen_y):
        return screen_y >= self.y and screen_y < self.y+self.h
    def screen_to_part(self, screen_y):
        return clamp( float(screen_y-self.h/2.0)/float(screen_size[1]-self.h), 0.0,1.0 )
    def click_toward(self, mouse_y):
        target = self.screen_to_part(mouse_y)
        if abs(target-self.part)<0.1: self.part=target
        else:
            if target>self.part: self.part+=0.1
            else:                self.part-=0.1
    def click_set(self, mouse_y):
        self.part = self.screen_to_part(mouse_y)

    def draw(self, line_height):
        self.y = int( self.part * (screen_size[1]-self.h) )

        bar_part = float(screen_size[1]) / float(line_height*self.n)
        self.h = int(bar_part * screen_size[1])
        if self.h<self.w: self.h=self.w

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
    global scroll,scrolling, screen_size, surface, frame
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
                try_scroll_by(  page_height-1 )
            elif event.key == K_PAGEUP:
                try_scroll_by(-(page_height-1))
        elif event.type == MOUSEBUTTONDOWN:
            if   event.button == 1:
                if mouse_position[0] >= screen_size[0] - slider.w:
                    if slider.screen_collides(mouse_position[1]):
                        scrolling = 1
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
        slider.click_set(mouse_position[1])
        try_scroll_to(rndint( slider.part * slider.n ))
    elif scrolling == 2:
        if frame == 0:
            slider.click_toward(mouse_position[1])
            try_scroll_to(rndint( slider.part * slider.n ))
            frame = rndint(0.100 * 60)
        else:
            frame -= 1
        
    return True

def draw():
    global page_height
    surface.fill((255,)*3)

    y = 0
    lines_drawn = 0
    for i in range(scroll,len(lines),1):
        num = font.render("% 5d|"%(i), True, (192,)*3)
        line = font.render(lines[i], True, (0,)*3)
        line_height = max([num.get_height(),line.get_height()])
        
        surface.blit(num, (0,y))
        surface.blit(line, (num.get_width(),y))
        
        lines_drawn += 1
        y += line_height
        if y >= screen_size[1]:
            break
    page_height = screen_size[1] // line_height

    slider.draw(line_height)
    
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
