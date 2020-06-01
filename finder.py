import sys
import pygame
from pathsettings import Settings
from squares import Vlines
from squares import Hlines
from squares import Squares
from squares import Path
from pygame.sprite import Group
import math

"""
Try to smooth the solution after after it's done: iterate from start point and all points to finish point to try and find a straighter path
Make solution_path_newer
Try to make the motion smother; maybe use group collide-create class for clicked squares
"""

def acquire_obstacle(square,obstacles,path_settings):
    if square.color==path_settings.pressed_square_color:
        coordinate=[square.rect.centerx,square.rect.centery]
        obstacles.append(coordinate)

def reset(sq):
    for s in sq:
        s.idle_square()

def make_squares(sq,path_settings,screen):
    for y in range(0,800,path_settings.square_size):
        for x in range(0,1200,path_settings.square_size):
            new_sq=Squares(screen,path_settings,x,y)
            sq.add(new_sq)
    for s in sq.sprites():
            s.draw_squares()

def run_game():
    # Initialize pygame, settings, and screen object.
    pygame.init()
    path_settings = Settings()
    screen = pygame.display.set_mode((path_settings.screen_width, path_settings.screen_height))
    pygame.display.set_caption("Path Finder")
    """
    vl=Group() 
    for x in range(0,1200,11):
        new_vl=Vlines(screen,path_settings,x)
        vl.add(new_vl)
    
    hl=Group() 
    for y in range(0,800,11):
        new_hl=Hlines(screen,path_settings,y)
        hl.add(new_hl)
    """
    sq=Group()
    make_squares(sq,path_settings,screen)
    #sq.sprites()[1].pressed_square()#tested right: to implement
    #sq.sprites()[1].draw_squares()
    moving=False
    presses=0
    start_point=[]
    end_point=[]
    probes=[]
    searching=False
    obstacles=[]
    keypresses=0
    escape=True
    # Start the main loop for the game. 
    while escape:
        # Watch for keyboard and mouse events. 
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos=pygame.mouse.get_pos()
                for s in sq.sprites():
                    if s.rect.collidepoint(pos):
                        if presses==0:
                            if s.color==path_settings.bg_color:
                                s.start_square()
                                start_point.append(s.rect.centerx)
                                start_point.append(s.rect.centery)
                                s.draw_squares()
                        elif presses==1:
                            if s.color==path_settings.bg_color:
                                s.finish_square()
                                end_point.append(s.rect.centerx)
                                end_point.append(s.rect.centery)
                                s.draw_squares()
                            else:
                                presses=0
                        else:
                            if s.color==path_settings.bg_color or s.color==path_settings.pressed_square_color:
                                moving=True
                            else:
                                presses=1
                presses+=1
            elif event.type == pygame.MOUSEBUTTONUP:
                moving=False
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_SPACE:
                    if keypresses==0:
                        searching=True
                        epicentre=[start_point]
                        probes.append(epicentre)
                        pathF=Path(end_point, probes, sq.sprites(),path_settings,searching,obstacles,start_point)
                        for s in sq.sprites():
                            acquire_obstacle(s,obstacles,path_settings)
                        keypresses+=1
                    else:
                        escape=False
                
        # Redraw the screen during each pass through the loop
        #screen.fill(path_settings.bg_color)

        #draw squares while pressing down
        while moving:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    moving=False
                pos=pygame.mouse.get_pos()
                xsize=int(path_settings.screen_width/path_settings.square_size)
                x=math.floor(pos[0]/path_settings.square_size)
                y=math.floor(pos[1]/path_settings.square_size)
                square_group_number=xsize*y+x
                if sq.sprites()[square_group_number].color==path_settings.bg_color or sq.sprites()[square_group_number].color==path_settings.pressed_square_color:
                    sq.sprites()[square_group_number].pressed_square()
                    sq.sprites()[square_group_number].draw_squares()
            pygame.display.flip()

        """
        #alternate version for moving:
        while moving:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    moving=False
                pos=pygame.mouse.get_pos()
                print(pos)
                for s in sq.sprites():
                    if s.rect.collidepoint(pos):
                        if s.color==path_settings.bg_color or s.color==path_settings.pressed_square_color:
                            s.pressed_square()#avoid painting over start or finish points
                            s.draw_squares()
            pygame.display.flip()
        """

        """
        for v in vl.sprites():
            v.draw_vLines()
        for h in hl.sprites():
            h.draw_vLines()
        """

        if searching:#this isnt quite righ/elegant
            if pathF.search:
                pathF.probe()

        # Make the most recently drawn screen visible. 
        pygame.display.flip()

while True:       
    run_game()