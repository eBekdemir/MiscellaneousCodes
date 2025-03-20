import json
import pygame
initial_settingsss = {"N": 3, "mode": [False, 4], "width": 1920, "height": 1080, "fps-limit": 60, "show_fps": True, "fullscreen": False, "maximize": True, "grid": [4, 4], "grid_margin": 10, "main_colors": [[245, 222, 179], [200, 200, 200], [0, 0, 0], [255, 255, 255]], "sqr_colors": [[255, 255, 255], [0, 0, 0], [255, 0, 0], [255, 255, 0], [0, 255, 0], [0, 255, 255], [0, 0, 255], [255, 0, 255]], "button_colors": [[255, 255, 255], [0, 0, 0], [255, 0, 0], [255, 255, 0], [0, 255, 0], [0, 255, 255], [0, 0, 255], [255, 0, 255]], "text_colors": [[0, 0, 0], [255, 0, 0], [255, 255, 0], [0, 255, 0], [0, 255, 255], [0, 0, 255], [255, 0, 255], [255, 255, 255]], "sel_sqr": [255, 0, 0], "sqr_col": [255, 255, 255], "proc_time": 1.0, "gap_time": 0.5, "color_match_key": 97, "position_match_key": 100, "voice_match_key": 115}

try:
    times24 = pygame.font.Font('C:/Windows/Fonts/times.ttf', 24)
    times48 = pygame.font.Font('C:/Windows/Fonts/times.ttf', 48)
    jbcode16 = pygame.font.Font('src/JBcode.ttf', 16)
except FileNotFoundError:
    ...



def get_settings() -> dict:
    """
    this function gets exist settings from settings.json
    and returns settings as a dictionary
    """
    with open("src/settings.json", 'r', encoding='utf-8') as file:
        settings = json.load(file)
    return settings

def dump_settings(settings:dict) -> None:
    """
    this function dumps given dictionary to settings.json
    and returns None
    """
    with open('src/settings.json', 'w', encoding='utf-8') as file:
        json.dump(settings, file)
    return

def init_settings() -> dict:
    """
    checks if settings.json file exist and have all initial keys

    if the file doesn't exist or doesn't have all initial settings, 
    creates a file with initial values 
    """
    
    try:
        settings = get_settings()
        if not all(key in settings for key in initial_settingsss.keys()):
            raise KeyError(f'There is a problem with keys. 100')
        return settings
    except KeyError and FileNotFoundError:
        dump_settings(initial_settingsss)
        return initial_settingsss

settings = get_settings()
BLACK, WHITE = [0,0,0], [255,255,255]
MAIN_COLOR = settings['main_colors'][0]
SQUARE_COLOR = settings['sqr_colors'][0]
BUTTON_COLOR = settings['button_colors'][0]
TEXT_COLOR = settings['text_colors'][0]

class Button:
    """
    It creates a button
    """
    def __init__(self, x:int, y:int, width:int, height:int, text:str, font:pygame.font.Font, color, hover_color, text_color, center:bool = True):
        """
        Args:
            x (int): x position
            y (int): y position
            width (int): rect width
            height (int): rect height
            text (str): button's text
            font: pygame font from settings
            color: button's color
            hover_color: hover color
            text_color: text color
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.font = font
        self.text_surf = self.font.render(self.text, True, text_color)
        if center:
            self.text_rect = self.text_surf.get_rect(center=self.rect.center)
        else:
            self.text_rect = self.text_surf.get_rect(center=(self.rect.left+155 ,self.rect.centery))

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, self.hover_color, self.rect, border_radius=8)
        else:
            pygame.draw.rect(screen, self.color, self.rect, border_radius=8)
        screen.blit(self.text_surf, self.text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False


class SettingsState:
    """
    Settings Screen
    """
    def __init__(self):
        self.settings = get_settings()
        self.total_height = None
        self.wheel_adjust = 40
        self.keys = {'change':'Press a button', 97: 'A', 98: 'B', 99: 'C', 100: 'D', 101: 'E', 102: 'F', 103: 'G', 104: 'H', 105: 'I', 106: 'J', 107: 'K', 108: 'L', 109: 'M', 110: 'N', 111: 'O', 112: 'P', 113: 'Q', 114: 'R', 115: 'S', 116: 'T', 117: 'U', 118: 'V', 119: 'W', 120: 'X', 121: 'Y', 122: 'Z', 48: '0', 49: '1', 50: '2', 51: '3', 52: '4', 53: '5', 54: '6', 55: '7', 56: '8', 57: '9', 1073741913: 'Keypad 1', 1073741914: 'Keypad 2', 1073741915: 'Keypad 3', 1073741916: 'Keypad 4', 1073741917: 'Keypad 5', 1073741918: 'Keypad 6', 1073741919: 'Keypad 7', 1073741920: 'Keypad 8', 1073741921: 'Keypad 9', 1073741922: 'Keypad 0'}
        self.numbers = {'change':'N?', 48: '0', 49: '1', 50: '2', 51: '3', 52: '4', 53: '5', 54: '6', 55: '7', 56: '8', 57: '9', 1073741913: '1', 1073741914: '2', 1073741915: '3', 1073741916: '4', 1073741917: '5', 1073741918: '6', 1073741919: '7', 1073741920: '8', 1073741921: '9', 1073741922: '0'}
        # key change memory
        self.cchange = None
        self.vchange = None
        self.pchange = None
        self.N_memory = None

    def reset(self) -> None:
        self.total_height = None
        self.wheel_adjust = 40
        self.settings = get_settings()
        global MAIN_COLOR, SQUARE_COLOR, BUTTON_COLOR, TEXT_COLOR
        MAIN_COLOR = self.settings['main_colors'][0]
        SQUARE_COLOR = self.settings['sqr_colors'][0]
        BUTTON_COLOR = self.settings['button_colors'][0]
        TEXT_COLOR = self.settings['text_colors'][0]


    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_BACKSPACE, pygame.K_ESCAPE]:
                    if self.cchange:
                        self.settings['color_match_key'] = self.cchange
                        self.cchange = None
                    elif self.vchange:
                        self.settings['voice_match_key'] = self.vchange
                        self.vchange = None
                    elif self.pchange:
                        self.settings['position_match_key'] = self.pchange
                        self.pchange = None
                    elif self.N_memory:
                        self.settings['N'] = int(self.N_memory)
                        self.N_memory = None
                    else:
                        return "menu"
                elif (self.cchange or self.pchange or self.vchange) and (event.key in self.keys):
                    if self.cchange and event.key != self.settings['voice_match_key'] and event.key != self.settings['position_match_key']:
                        self.settings['color_match_key'] = event.key
                        self.cchange = None
                    elif self.vchange and event.key != self.settings['color_match_key'] and event.key != self.settings['position_match_key']:
                        self.settings['voice_match_key'] = event.key
                        self.vchange = None
                    elif self.pchange and event.key != self.settings['voice_match_key'] and event.key != self.settings['color_match_key']:
                        self.settings['position_match_key'] = event.key
                        self.pchange = None
                elif self.N_memory and event.key in self.numbers:
                    if self.numbers[event.key] != '0' or len(self.settings['N']) == 2:
                        self.settings['N'] = self.settings['N'] + self.numbers[event.key]
                        if len(self.settings['N']) == 3:
                            self.settings['N'] = int(self.settings['N'][1:])
                            self.N_memory = None
                elif event.key in [pygame.K_RETURN, pygame.K_KP_ENTER] and self.N_memory:
                    self.settings['N'] = int(self.settings['N'][1:]) if len(self.settings['N'])>= 2 else self.N_memory
                    self.N_memory = None

            if event.type == pygame.MOUSEWHEEL:
                move = event.y * 20
                info = pygame.display.Info()
                if abs(self.wheel_adjust + move) <= self.total_height - info.current_h/3:
                    self.wheel_adjust += move
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.full_screen.is_clicked(event):
                    if self.settings['fullscreen'] and self.settings['maximize']:
                        self.settings['fullscreen'] = False
                        self.settings['maximize'] = False
                        self.settings['width'] = 800
                        self.settings['height'] = 800
                    elif not self.settings['fullscreen'] and not self.settings['maximize']:
                        self.settings['fullscreen'] = False
                        self.settings['maximize'] = True
                        info = pygame.display.Info()
                        self.settings['width'] = info.current_w
                        self.settings['height'] = info.current_h

                    elif not self.settings['fullscreen'] and self.settings['maximize']:
                        self.settings['fullscreen'] = True
                        self.settings['maximize'] = True
                if self.resolution.is_clicked(event):
                    ...
                if self.fps_limit.is_clicked(event):
                    self.settings['fps-limit'] = 60 if self.settings['fps-limit'] == 30 else 90 if self.settings['fps-limit'] == 60 else 120 if self.settings['fps-limit'] == 90 else 30
                if self.show_fps.is_clicked(event):
                    self.settings['show_fps'] = False if self.settings['show_fps'] else True
                
                if self.N.is_clicked(event):
                    self.N_memory = self.settings['N']
                    self.settings['N'] = ' '

                if self.mode.is_clicked(event):
                    if self.settings['mode'][1]:
                        self.settings['mode'][0] = False
                        self.settings['mode'][1] = 3 if self.settings['mode'][1] == 2 else 4 if self.settings['mode'][1] == 3 else 5 if self.settings['mode'][1] == 4 else 6 if self.settings['mode'][1] == 5 else 8 if self.settings['mode'][1] == 6 else 10 if self.settings['mode'][1] == 8 else False
                    if not self.settings['mode'][1]:
                        self.settings['mode'][0] = True
                        self.settings['mode'][1] = 2
                
                if self.grid.is_clicked(event):
                    if self.settings['grid'][0]<6:
                        self.settings['grid'][1] += 1
                        self.settings['grid'][0] += 1
                    else:
                        self.settings['grid'][1] = 2
                        self.settings['grid'][0] = 2
                
                if self.proc_time.is_clicked(event):
                    if self.settings['proc_time']<3:
                        self.settings['proc_time'] += 0.25
                    else:
                        self.settings['proc_time'] = 0.5
                if self.gap_time.is_clicked(event):
                    if self.settings['gap_time']<2:
                        self.settings['gap_time'] += 0.25
                    else:
                        self.settings['gap_time'] = 0.25
                
                if self.color_key.is_clicked(event):
                    self.cchange = self.settings['color_match_key']
                    self.settings['color_match_key'] = 'change'
                
                if self.voice_key.is_clicked(event):
                    self.vchange = self.settings['voice_match_key']
                    self.settings['voice_match_key'] = 'change'

                if self.position_key.is_clicked(event):
                    self.pchange = self.settings['position_match_key']
                    self.settings['position_match_key'] = 'change'

                if self.main_color.is_clicked(event):
                    temp = self.settings['main_colors'][1:]
                    temp.append(self.settings['main_colors'][0])
                    self.settings['main_colors'] = temp

                if self.sqr_color.is_clicked(event):
                    temp = self.settings['sqr_colors'][1:]
                    temp.append(self.settings['sqr_colors'][0])
                    self.settings['sqr_colors'] = temp
                
                if self.button_color.is_clicked(event):
                    temp = self.settings['button_colors'][1:]
                    temp.append(self.settings['button_colors'][0])
                    self.settings['button_colors'] = temp


                if self.save.is_clicked(event):
                    self.settings['N'] = int(self.settings['N'])
                    dump_settings(self.settings)
                    return "menu"
                
                if self.res_all.is_clicked(event):
                    dump_settings(initial_settingsss)


    def render(self, screen, screen_size):
        screen.fill(MAIN_COLOR)
        w, h = screen_size
        button_w = 400
        button_h = 50
        button_margin = 20

        self.total_height = (button_h + button_margin) * 16 - button_margin
        
        # buttons
        self.save = Button((w-button_w)//2, self.wheel_adjust, button_w, button_h, f"Save and Exit", times24, BUTTON_COLOR, BUTTON_COLOR, TEXT_COLOR)
        self.save.draw(screen)
        # screen
        self.full_screen = Button((w-button_w)//2, self.wheel_adjust + (button_h + button_margin), button_w, button_h, f"{'Full Screen'.ljust(16)}:{'Yes'.rjust(16) if self.settings['fullscreen'] else 'No'.rjust(16) if not self.settings['maximize'] else 'Maximize'.rjust(16)}", jbcode16, BUTTON_COLOR, BUTTON_COLOR, TEXT_COLOR)
        self.full_screen.draw(screen)
        self.resolution = Button((w-button_w)//2, self.wheel_adjust + (button_h + button_margin)*2, button_w, button_h, f"{'Resolution'.ljust(16)}:{str(str(self.settings['width']) + 'x' + str(self.settings['height'])).rjust(16)}", jbcode16, BUTTON_COLOR, BUTTON_COLOR, TEXT_COLOR)
        self.resolution.draw(screen)
        self.fps_limit = Button((w-button_w)//2, self.wheel_adjust + (button_h + button_margin)*3, button_w, button_h, f"{'FPS Limit'.ljust(16)}:{str(self.settings['fps-limit']).rjust(16)}", jbcode16, BUTTON_COLOR, BUTTON_COLOR, TEXT_COLOR)
        self.fps_limit.draw(screen)
        self.show_fps = Button((w-button_w)//2, self.wheel_adjust + (button_h + button_margin)*4, button_w, button_h, f"{'Show FPS'.ljust(16)}:{'Yes'.rjust(16) if self.settings['show_fps'] else 'No'.rjust(16)}", jbcode16, BUTTON_COLOR, BUTTON_COLOR, TEXT_COLOR)
        self.show_fps.draw(screen)


        # game-play
        self.N = Button((w-button_w)//2, self.wheel_adjust + (button_h + button_margin)*5, button_w, button_h, f"{'N (step)'.ljust(16)}:{str(self.settings['N']).rjust(16)}", jbcode16, BUTTON_COLOR, BUTTON_COLOR, TEXT_COLOR)
        self.N.draw(screen)
        self.mode = Button((w-button_w)//2, self.wheel_adjust + (button_h + button_margin)*6, button_w, button_h, f"{'Mode'.ljust(16)}:{str('+1/'+str(self.settings['mode'][1]) + ' chance').rjust(16) if not self.settings['mode'][0] else 'Full Randomly'.rjust(16)}", jbcode16, BUTTON_COLOR, BUTTON_COLOR, TEXT_COLOR)
        self.mode.draw(screen)
        self.grid = Button((w-button_w)//2, self.wheel_adjust + (button_h + button_margin)*7, button_w, button_h, f"{'Grid'.ljust(16)}:{str(str(self.settings['grid'][0]) + 'x' + str(self.settings['grid'][1])).rjust(16)}", jbcode16, BUTTON_COLOR, BUTTON_COLOR, TEXT_COLOR)
        self.grid.draw(screen)
        self.proc_time = Button((w-button_w)//2, self.wheel_adjust + (button_h + button_margin)*8, button_w, button_h, f"{'Process Time'.ljust(16)}:{str(self.settings['proc_time']).rjust(16)}", jbcode16, BUTTON_COLOR, BUTTON_COLOR, TEXT_COLOR)
        self.proc_time.draw(screen)
        self.gap_time = Button((w-button_w)//2, self.wheel_adjust + (button_h + button_margin)*9, button_w, button_h, f"{'Gap Time'.ljust(16)}:{str(self.settings['gap_time']).rjust(16)}", jbcode16, BUTTON_COLOR, BUTTON_COLOR, TEXT_COLOR)
        self.gap_time.draw(screen)

        # keyboard
        self.color_key = Button((w-button_w)//2, self.wheel_adjust + (button_h + button_margin)*10, button_w, button_h, f"{'Color Match'.ljust(16)}:{str(self.keys[self.settings['color_match_key']]).rjust(16)}", jbcode16, BUTTON_COLOR, BUTTON_COLOR, TEXT_COLOR)
        self.color_key.draw(screen)
        self.voice_key = Button((w-button_w)//2, self.wheel_adjust + (button_h + button_margin)*11, button_w, button_h, f"{'Voice Match'.ljust(16)}:{str(self.keys[self.settings['voice_match_key']]).rjust(16)}", jbcode16, BUTTON_COLOR, BUTTON_COLOR, TEXT_COLOR)
        self.voice_key.draw(screen)
        self.position_key = Button((w-button_w)//2, self.wheel_adjust + (button_h + button_margin)*12, button_w, button_h, f"{'Position Match'.ljust(16)}:{str(self.keys[self.settings['position_match_key']]).rjust(16)}", jbcode16, BUTTON_COLOR, BUTTON_COLOR, TEXT_COLOR)
        self.position_key.draw(screen)

        # theme
        self.main_color = Button((w-button_w)//2, self.wheel_adjust + (button_h + button_margin)*13, button_w, button_h, f"{'Main Color'.ljust(16)}:{' '.rjust(16)}", jbcode16, BUTTON_COLOR, BUTTON_COLOR, TEXT_COLOR)
        self.main_color.draw(screen)
        pygame.draw.rect(screen, self.settings['main_colors'][0], pygame.Rect((w-button_w)//2 + button_w//2 + 10, (self.wheel_adjust + (button_h + button_margin)*13) + 8, button_w//2 - 20, button_h - 16), border_radius=6)

        self.sqr_color = Button((w-button_w)//2, self.wheel_adjust + (button_h + button_margin)*14, button_w, button_h, f"{'Square Colors'.ljust(16)}:{' '.rjust(16)}", jbcode16, BUTTON_COLOR, BUTTON_COLOR, TEXT_COLOR)
        self.sqr_color.draw(screen)
        pygame.draw.rect(screen, self.settings['sqr_colors'][0], pygame.Rect((w-button_w)//2 + button_w//2 + 10, (self.wheel_adjust + (button_h + button_margin)*14) + 8, button_w//2 - 20, button_h - 16), border_radius=6)

        self.button_color = Button((w-button_w)//2, self.wheel_adjust + (button_h + button_margin)*15, button_w, button_h, f"{'Button Colors'.ljust(16)}:{' '.rjust(16)}", jbcode16, BUTTON_COLOR, BUTTON_COLOR, TEXT_COLOR)
        self.button_color.draw(screen)
        pygame.draw.rect(screen, self.settings['button_colors'][0], pygame.Rect((w-button_w)//2 + button_w//2 + 10, (self.wheel_adjust + (button_h + button_margin)*15) + 8, button_w//2 - 20, button_h - 16), border_radius=6)

        # reset
        self.res_all = Button((w-button_w)//2, self.wheel_adjust + (button_h + button_margin)*16, button_w, button_h, f"Reset all settings", times24, BUTTON_COLOR, BUTTON_COLOR, TEXT_COLOR)
        self.res_all.draw(screen)