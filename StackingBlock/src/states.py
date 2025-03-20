import os
import pygame
import src.settings as set
from random import randint, choice
import json

pygame.mixer.init()


class Pieces:
    def __init__(self, width, height) -> None:
        self.width = width
        self.height = height
    
    


class StateManager:
    """
    State (screen) manager
    """
    def __init__(self):
        self.states = {
            "loading": LoadingState(),
            "menu": MenuState(),
            "play":GameState(),
            "settings":set.SettingsState(),
            # "stat":StatisticsState()
        }
        self.current_state = self.states["loading"]

    def switch_state(self, new_state):
        self.current_state.reset()
        self.current_state = self.states[new_state]
        self.current_state.reset()

    def update(self, events):
        next_state = self.current_state.update(events)
        if next_state == "quit":
            return "quit"
        if next_state:
            self.switch_state(next_state)

    def render(self, screen, size):
        self.current_state.render(screen, size)


class LoadingState:
    """
    Loading Screen
    """
    def __init__(self):
        ...

    def reset(self) -> None:
        ...

    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE, pygame.K_BACKSPACE, pygame.K_ESCAPE]:
                    return "menu"
    def render(self, screen, screen_size):
        screen.fill(set.BLACK)
        text = set.times48.render("Welcome to Stacking!", True, (255, 255, 255))
        text_rect = text.get_rect(center=(screen_size[0]/2, screen_size[1]/2)) # centers the text
        screen.blit(text, text_rect)
        text2 = set.times24.render("- press enter ~Kömen -", True, (255, 255, 255))
        text2_rect = text2.get_rect(center=(screen_size[0]/2, (screen_size[1]/2)+60))
        screen.blit(text2, text2_rect)


class MenuState:
    """
    Menu Screen
    """
    def __init__(self):
        ...

    def reset(self) -> None:
        ...

    def update(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.voice_pos.is_clicked(event):
                    return "play"
                if self.sett.is_clicked(event):
                    return "settings"
                if self.stat.is_clicked(event):
                    return "stat"
                if self.qt.is_clicked(event):
                    return "quit"
                

    def render(self, screen, screen_size):
        screen.fill(set.MAIN_COLOR)
        w, h = screen_size
        button_w = 250
        button_h = 50
        button_margin = 20
        total_height = (button_h + button_margin) * 4 - button_margin # total height of buttons

        # buttons 
        self.voice_pos = set.Button((w-button_w)//2, (h-total_height)//2, button_w, button_h, 'Play', set.jbcode16, set.BUTTON_COLOR, set.BUTTON_COLOR, set.TEXT_COLOR)
        self.voice_pos.draw(screen)
        self.sett = set.Button((w-button_w)//2, (h-total_height)//2 + (button_h + button_margin), button_w, button_h, 'Settings', set.jbcode16, set.BUTTON_COLOR, set.BUTTON_COLOR, set.TEXT_COLOR)
        self.sett.draw(screen)
        self.stat = set.Button((w-button_w)//2, (h-total_height)//2 + (button_h + button_margin)*2, button_w, button_h, 'Statistics', set.jbcode16, set.BUTTON_COLOR, set.BUTTON_COLOR, set.TEXT_COLOR)
        self.stat.draw(screen)
        self.qt = set.Button((w-button_w)//2, (h-total_height)//2 + (button_h + button_margin)*3, button_w, button_h, 'Quit', set.jbcode16, set.BUTTON_COLOR, set.BUTTON_COLOR, set.TEXT_COLOR)
        self.qt.draw(screen)


class GameState:
    """
    Game Screen
    """
    def __init__(self):
        self.piece = 0
        self.score = 0
        self.pause_state = False
        self.game_over = False
        self.proc = 2
        self.time = None
        self.game_time = None
        self.rects = []
        self.wait = 0.005
        self.rect_colors = [[255, 255, 255], [0, 0, 0], [255, 0, 0], [255, 255, 0], [0, 255, 0], [0, 255, 255], [0, 0, 255], [255, 0, 255]]
        try:
            self.rect_colors.remove(set.MAIN_COLOR)
        except: ...
    def reset(self) -> None:
        self.piece = 0
        self.score = 0
        self.pause_state = False
        self.game_over = False
        self.proc = 2
        self.time = None
        self.game_time = None
        self.rects = [] # [color, Rect object]


    def pause(self, screen, screen_size) -> None:
        w, h = screen_size
        button_w = 250
        button_h = 50
        button_margin = 20
        total_height = (button_h + button_margin) * 2 - button_margin # total height of buttons

        pygame.draw.rect(screen, set.BLACK, pygame.Rect((w-button_w)//2 - 30, ((h-total_height)//2)- (button_h/2) , button_w+60,total_height + button_h), 4)
        pygame.draw.rect(screen, set.MAIN_COLOR, pygame.Rect((w-button_w)//2 - 25, ((h-total_height)//2)- (button_h/2)+5 , button_w+50, total_height + button_h-10))

        self.resume = set.Button((w-button_w)//2, (h-total_height)//2, button_w, button_h, 'Resume', set.jbcode16, set.BUTTON_COLOR, set.BUTTON_COLOR, set.TEXT_COLOR)
        self.resume.draw(screen)
        self.menu = set.Button((w-button_w)//2, (h-total_height)//2 + (button_h + button_margin), button_w, button_h, 'Main Menu', set.jbcode16, set.BUTTON_COLOR, set.BUTTON_COLOR, set.TEXT_COLOR)
        self.menu.draw(screen)

    def slide(self) -> None:
        for _, obj in self.rects:
            obj.y += 50

    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_BACKSPACE, pygame.K_ESCAPE]:
                    self.pause_state = False if self.pause_state else True 
                if event.key == pygame.K_DOWN:
                    if len(self.rects)>1:
                        self.rects[-1][1].y = self.rects[-2][1].y-50


            if event.type == pygame.MOUSEBUTTONDOWN and self.pause_state:
                if self.resume.is_clicked(event):
                    self.pause_state = False
                if self.menu.is_clicked(event):
                    return 'menu'
            
                
    def process(self, screen_size) -> None:
        w, h = screen_size
        
        if not self.game_time:
            self.game_time = pygame.time.get_ticks()
        
        if self.proc == 2 and not self.pause_state:
            self.time = pygame.time.get_ticks()
            if len(self.rects)>1:
                width = randint((9*(self.rects[-1][1].width))//10, (12*(self.rects[-1][1].width))//10)
                x = randint((w-width)//4, (w-width)*3//4)

            else:
                width = randint(300, 600)
                x = randint((w-width)//4, (w-width)*3//4)
            self.rects.append([choice(self.rect_colors), pygame.Rect(x, 20, width, 50)])
            self.proc = 0
        
        elif self.proc == 0 and not self.pause_state: # sliding process
            relocate = pygame.key.get_pressed()
            if relocate[pygame.K_RIGHT] and self.rects[-1][1].right + 2 <= w:
                self.rects[-1][1].x += 3
            if relocate[pygame.K_LEFT] and self.rects[-1][1].left - 2 >= 0:
                self.rects[-1][1].x -= 3
            time_con = (pygame.time.get_ticks() - self.time)/1000
            if len(self.rects) > 1:
                if self.rects[-2][1].y <= self.rects[-1][1].y+50 and time_con >= self.wait:
                    self.time = pygame.time.get_ticks()
                    self.proc += 1
                elif time_con >= self.wait:
                    self.time = pygame.time.get_ticks()
                    self.rects[-1][1].y += 2


            elif self.rects[-1][1].y <= h-100 and time_con >= self.wait:
                self.time = pygame.time.get_ticks()
                self.rects[-1][1].y += 2

            elif time_con >= self.wait:
                self.time = pygame.time.get_ticks()
                self.proc += 1

        
        elif self.proc == 1 and not self.pause_state and not self.game_over: # checking
            time_con = (pygame.time.get_ticks() - self.time)/1000
            if len(self.rects) > 1:
                if self.rects[-1][1].y > self.rects[-2][1].y and time_con >= self.wait/5:
                    self.time = pygame.time.get_ticks()
                    self.rects[-1][1].y += 1
                    self.game_over = True

                elif self.rects[-2][1].right >= self.rects[-1][1].left and self.rects[-1][1].left >= self.rects[-2][1].left and self.rects[-1][1].right >= self.rects[-2][1].right: # pos 1
                    self.rects[-1][1].width = self.rects[-2][1].right - self.rects[-1][1].left

                elif self.rects[-1][1].right <= self.rects[-2][1].right and self.rects[-1][1].right >= self.rects[-2][1].left and self.rects[-2][1].left >= self.rects[-1][1].left: # pos 2
                    self.rects[-1][1].width = self.rects[-1][1].right - self.rects[-2][1].left
                    self.rects[-1][1].x = self.rects[-2][1].x

                elif self.rects[-1][1].left >= self.rects[-2][1].left and self.rects[-1][1].right <= self.rects[-2][1].right: # pos 3
                    ...
                
                elif self.rects[-1][1].left <= self.rects[-2][1].left and self.rects[-1][1].right >= self.rects[-2][1].right: # pos 4
                    self.rects[-1][1].width = self.rects[-2][1].width
                    self.rects[-1][1].x = self.rects[-2][1].x
                else:
                    self.game_over = True
            if not self.game_over:
                self.score += ((self.piece**3)/self.rects[-1][1].width)//((pygame.time.get_ticks() - self.game_time)/1000 - 4)
                self.score += 1 + self.piece/6
                self.piece += 1
                self.proc += 1
            if self.rects[-1][1].y <= h//2:
                self.slide()



    def render(self, screen, screen_size) -> None:
        screen.fill(set.MAIN_COLOR)
                
        self.process(screen_size)
        if self.piece >= 1:
            scr = f"Length: {self.piece}    Score: {int(self.score)}    Time: {(pygame.time.get_ticks()-self.game_time)//1000}"
        else:
            scr = f"Length: 0    Score: 0    Time: {(pygame.time.get_ticks()-self.game_time)//1000}"
        text = set.jbcode16.render(scr, True, (0, 0, 0))
        text_rect = text.get_rect(center=(screen_size[0]/2, 10))
        screen.blit(text, text_rect)


        for color, obj in self.rects:
            pygame.draw.rect(screen, color, obj)
            pygame.draw.rect(screen, (255, 255, 255), obj, 1)

        if self.pause_state:
            self.pause(screen, screen_size)