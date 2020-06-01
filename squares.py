import pathsettings
import pygame
import time
import sys

class Vlines(pygame.sprite.Sprite):
    def __init__(self,screen, path_settings,x):
        super(Vlines,self).__init__()
        self.screen = screen
        self.rect=pygame.Rect(x,0,1,800)
        self.color=path_settings.line_color
    def draw_vLines(self):
        pygame.draw.rect(self.screen, self.color, self.rect)

class Hlines(pygame.sprite.Sprite):
    def __init__(self,screen, path_settings,y):
        super(Hlines,self).__init__()
        self.screen = screen
        self.rect=pygame.Rect(0,y,1200,1)
        self.color=path_settings.line_color
    def draw_vLines(self):
        pygame.draw.rect(self.screen, self.color, self.rect)

class Squares(pygame.sprite.Sprite):
    def __init__(self,screen,path_settings,x,y):
        super(Squares,self).__init__()
        self.screen = screen
        self.rect=pygame.Rect(x,y,path_settings.square_size,path_settings.square_size)
        self.color=path_settings.bg_color
        self.idle_color=path_settings.bg_color
        self.pressed_color=path_settings.pressed_square_color
        self.startSquare_color=path_settings.start_square_color
        self.finishSquare_color=path_settings.finish_square_color
    def draw_squares(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
    def pressed_square(self):
        self.color=self.pressed_color
    def start_square(self):
        self.color=self.startSquare_color
    def finish_square(self):
        self.color=self.finishSquare_color
    def idle_square(self):#for showing last steps: to implement
        self.color=self.idle_color

class Path():
    def __init__(self,endpoint, probes, sqs, path_settings,searching,obstacles,startpoint):
        self.endpoint=endpoint
        self.probes=probes
        self.sqs=sqs
        self.color=path_settings.paths
        self.pressed_color=path_settings.pressed_square_color
        self.start_color=path_settings.start_square_color
        self.solution_color=path_settings.solution_color
        self.solution=[]
        self.search=searching
        self.obstacles=obstacles
        self.steps_taken=[startpoint]
        self.probes_sent=0
        self.square_size=path_settings.square_size
        self.path_newer=path_settings.solution_path_newer
    def probe(self):
        #generates new paths from existing ones
        validpaths=[]
        for path in self.probes:
            checkpoint=[]
            validpoint=[]
            if self.search:
                try:
                    #calculates possible steps and appends to checkpoint
                    nextStep0=[path[-1][0]+0 ,path[-1][1]+self.square_size]
                    nextStep1=[path[-1][0]+0 ,path[-1][1]-self.square_size]
                    nextStep2=[path[-1][0]-self.square_size,path[-1][1]+0]
                    nextStep3=[path[-1][0]+self.square_size,path[-1][1]+0]
                    nextStep4=[path[-1][0]+self.square_size,path[-1][1]+self.square_size]
                    nextStep5=[path[-1][0]+self.square_size,path[-1][1]-self.square_size]
                    nextStep6=[path[-1][0]-self.square_size,path[-1][1]+self.square_size]
                    nextStep7=[path[-1][0]-self.square_size,path[-1][1]-self.square_size]

                    checkpoint.append(nextStep0)
                    checkpoint.append(nextStep1)
                    checkpoint.append(nextStep2)
                    checkpoint.append(nextStep3)
                    checkpoint.append(nextStep4)
                    checkpoint.append(nextStep5)
                    checkpoint.append(nextStep6)
                    checkpoint.append(nextStep7)
                    
                    #checks for valid steps
                    for point in checkpoint:
                        #inside field
                        if point[0]<0 or point[1]<0 or point[0]>1200 or point[1]>800:
                            continue
                        #outside treaded path
                        if point in self.steps_taken:
                            continue
                        #doensn't step on obstacle
                        if point in self.obstacles:
                            continue
                        validpoint.append(point)

                    #draws valid steps
                    for point in validpoint:
                        for square in self.sqs:
                            if (square.rect.centerx,square.rect.centery)==tuple(point) and point!=self.endpoint:
                                square.color=self.color
                                square.draw_squares()

                    #adds valid steps to probes as a path and checks if any is the solution
                    for point in validpoint:
                        newPath=path.copy()
                        newPath.append(point)
                        validpaths.append(newPath)
                        self.steps_taken.append(point)
                        if tuple(point)==tuple(self.endpoint):
                            self.solution=newPath.copy()
                            self.search=False
                            self.probes_sent+=len(self.probes)
                            print(f'Probes sent{self.probes_sent}')
                            break

                    #draws solution if True
                    for point in self.solution[1:-1]:
                        for square in self.sqs:
                            if (square.rect.centerx,square.rect.centery)==tuple(point):
                                square.color=self.solution_color
                                square.draw_squares()

                    if len(self.solution)!=0:
                        break
                except IndexError:
                    sys.exit(0)

        #checks for impossible solution
        if len(self.probes)==0:
            print("No solution possible")
            self.search=False

        self.probes_sent+=len(self.probes)
        #saves new paths and forgets about the original path 
        self.probes=validpaths.copy()