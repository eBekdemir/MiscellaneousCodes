__author__ = "Kömen - Enes Bekdemir | 2024"


import pygame as py
import numpy as np
import math


py.init()

w, h = 1200, 800
WIN = py.display.set_mode((w,h))
py.display.set_caption("Space Simulator")


clock = py.time.Clock()
timeStep = np.int32(60*60*24) # 1 day
scale = 100
look = [0,0]



class SpaceObject():
    def_colors = {'white':(255,255,255), 'black':(0,0,0), 'sun':(0)}
    font = py.font.Font(None, 16)
    AU = np.int64(149_597_870_700)
    def_density = 5500  
    def __init__(self, name: str, color: tuple[int, int, int], mass: np.float64, coordinate: tuple[float, float], velocity: tuple[float, float], radius: float = '', density: np.int16 = '', lengthYear: int = 500):
        self.name = name if not name in ['', ' ', None] else 'Unknown'
        self.color = color if not color in self.def_colors else self.def_colors[color]
        
        self.mass = mass
        
        self.lengthYear = lengthYear
        
        self.density = density if density != '' else self.def_density
        self.radius = radius if radius != '' else ((math.pow((3 * self.mass) / (4 * math.pi * self.density), 1/3))/self.AU) * scale * 10
        if self.radius >= 4: self.radius *= 4
        elif self.radius >= 3: self.radius *= 7
        elif self.radius >= 2: self.radius *= 9 
        elif self.radius >= 1: self.radius *= 12 
        elif self.radius >= 0.5: self.radius *= 15
        elif self.radius >= 0.3: self.radius *= 18
        elif self.radius >= 0.2: self.radius *= 20
        elif self.radius >= 0.15: self.radius *= 22
        elif self.radius >= 0.1: self.radius *= 25
        elif self.radius >= 0.05: self.radius *= 30
        else: self.radius *= 35
        
        self.X, self.Y = coordinate
        self.vel_X, self.vel_Y = velocity 

        self.accX, self.accY = (0, 0)

        self.orbit = []
    

    def line_display(self, surface):
        if len(self.orbit) > self.lengthYear + 1000:
            self.orbit = self.orbit[-self.lengthYear-10:]
        py.draw.lines(surface, self.color, False, 
                      [((point[0]) * scale + w // 2 + look[0], point[1] * scale + h // 2 + look[1]) for point in self.orbit[-self.lengthYear:]], width=1) 

    def display(self, surface):
        py.draw.circle(surface, self.color, (((self.X/self.AU) * scale + w // 2 + look[0]), ((self.Y/self.AU) * scale + h // 2 + look[1])), self.radius) 
        if len(self.orbit)>2: self.line_display(surface)
        if scale >= 300: 
            vel_surface = self.font.render(f'{math.sqrt(math.pow(self.vel_X, 2) + math.pow(self.vel_Y, 2)):.2f}', True, (255,255,255))
            vel_rect = vel_surface.get_rect(center=(((self.X/self.AU) * scale + w // 2 + look[0]), ((self.Y/self.AU) * scale + h // 2 + look[1] + self.radius + 3)))
            surface.blit(vel_surface, vel_rect)

    def update(self, objects):
        self.X += self.vel_X * timeStep
        self.Y += self.vel_Y * timeStep

        self.orbit.append(((self.X/self.AU), (self.Y/self.AU)))

        a_X, a_Y = Calculations().totalAcc(self, objects)
        self.accX = a_X
        self.accY = a_Y
        self.vel_X += self.accX * timeStep
        self.vel_Y += self.accY * timeStep

    def __str__(self):
        return f'{str(self.name + ":").ljust(10)}\t({(self.X/self.AU) * scale + w // 2}, {(self.Y/self.AU) * scale + h // 2})\tvel=({self.vel_X}, {self.vel_Y})'



class Calculations():
    G = 6.674 * 10**-11 # gravitational constant
    
    def __init__(self):
        pass

    def distanceBetween(self, obj1: SpaceObject, obj2: SpaceObject) -> float:
        return math.sqrt(math.pow((obj2.X - obj1.X), 2) + math.pow((obj2.Y - obj1.Y), 2))

    def gravitationalForce(self, obj1: SpaceObject, obj2: SpaceObject):
        return (self.G * (obj1.mass * obj2.mass)) / (math.pow(self.distanceBetween(obj1, obj2), 2))

    def totalForce(self, mainObject:SpaceObject, objects: list[SpaceObject]) -> tuple[float, float]:
        F_total_x, F_total_y = 0, 0
        for obj in objects:
            if obj != mainObject:
                distance = self.distanceBetween(mainObject, obj)
                if distance == 0:
                    continue
                F = self.gravitationalForce(mainObject, obj)
                dx = obj.X - mainObject.X
                dy = obj.Y - mainObject.Y
                F_total_x += F * (dx / distance)
                F_total_y += F * (dy / distance)
        return F_total_x, F_total_y

    def totalAcc(self, mainObject:SpaceObject, objects: list[SpaceObject]) -> tuple[float, float]:
        F_x, F_y = self.totalForce(mainObject, objects)
        return F_x / mainObject.mass, F_y / mainObject.mass

    def move(self, key):
        directions = {'l':(1,0), 'r':(-1,0), 'u':(0,1), 'd':(0,-1)}
        direction = directions[key]

        look[0] += direction[0]*10
        look[1] += direction[1]*10
        
    def rescale(self, key, objects):
        global scale
        if key == '+' and scale <= 25:
            for obj in objects:
                obj.radius = (obj.radius/scale) * (scale + 1)
            scale += 1
        elif key == '+' and scale <= 100:
            for obj in objects:
                obj.radius = (obj.radius/scale) * (scale + 2)
            scale += 2
        elif key == '+' and scale <= 300:
            for obj in objects:
                obj.radius = (obj.radius/scale) * (scale + 3)
            scale += 3
        elif key == '+' and scale <= 500:
            for obj in objects:
                obj.radius = (obj.radius/scale) * (scale + 4)
            scale += 4
        elif key == '+' and scale <= 1000:
            for obj in objects:
                obj.radius = (obj.radius/scale) * (scale + 5)
            scale += 5



        elif key == '-' and scale >=500:
            for obj in objects:
                obj.radius = (obj.radius/scale) * (scale - 5)
            scale -= 5
        elif key == '-' and scale >=300:
            for obj in objects:
                obj.radius = (obj.radius/scale) * (scale - 4)
            scale -= 4
        elif key == '-' and scale >=100:
            for obj in objects:
                obj.radius = (obj.radius/scale) * (scale - 3)
            scale -= 3
        elif key == '-' and scale >=25:
            for obj in objects:
                obj.radius = (obj.radius/scale) * (scale - 2)
            scale -= 2
        elif key == '-' and scale >=7:
            for obj in objects:
                obj.radius = (obj.radius/scale) * (scale - 1)
            scale -= 1




sun = SpaceObject('Sun', (253, 184, 19), np.float64(1.989e30), (0, 0), (0,0), density=1450)
mercury = SpaceObject('Mercury', (231,232,236), np.float64(3.332e23), (-SpaceObject.AU*0.39, 0), (0,47_360), lengthYear=88)
venus = SpaceObject('Venus', (227,187,118), np.float64(4.869e24), (-SpaceObject.AU*0.72, 0), (0,35_020), lengthYear=225)
earth = SpaceObject('Earth', (40, 122, 184), np.float64(5.9722e24), (-SpaceObject.AU, 0), (0,29_780), lengthYear=365)
mars = SpaceObject('Mars', (142, 106, 90), np.float64(6.39e23), (-SpaceObject.AU*1.52, 0), (0,24_080), lengthYear=687)
jupiter = SpaceObject('Jupiter', (221,188,166), np.float64(1.898e27), (SpaceObject.AU*5.2, 0), (0,-13_060), lengthYear=4331)
saturn = SpaceObject('Saturn', (237,219,173), np.float64(5.683e26), (-SpaceObject.AU*9.54, 0), (0,9_670), lengthYear=10_747)
uranus = SpaceObject('Uranus', (147,205,241), np.float64(8.681e25), (SpaceObject.AU*19.22, 0), (0,-6_790), lengthYear=30_687)
neptune = SpaceObject('Neptune', (91,93,223), np.float64(1.024e26), (SpaceObject.AU*30.06, 0), (0,-5_450), lengthYear=60_190)

# sun2 = SpaceObject('Sun2', (253, 184, 19), np.float64(1.989e30), (-SpaceObject.AU*150,0), (0,0), density=1450)
# mercury2 = SpaceObject('Mercury', (231,232,236), np.float64(3.332e23), (-SpaceObject.AU*150-SpaceObject.AU*0.39, 0), (0,47_360), lengthYear=88)
# venus2 = SpaceObject('Venus', (227,187,118), np.float64(4.869e24), (-SpaceObject.AU*150-SpaceObject.AU*0.72, 0), (0,35_020), lengthYear=225)
# earth2 = SpaceObject('Earth', (40, 122, 184), np.float64(5.9722e24), (-SpaceObject.AU*150-SpaceObject.AU, 0), (0,29_780), lengthYear=365)
# mars2 = SpaceObject('Mars', (142, 106, 90), np.float64(6.39e23), (-SpaceObject.AU*150-SpaceObject.AU*1.52, 0), (0,24_080), lengthYear=687)
# jupiter2 = SpaceObject('Jupiter', (221,188,166), np.float64(1.898e27), (-SpaceObject.AU*150+SpaceObject.AU*5.2, 0), (0,-13_060), lengthYear=4331)
# saturn2 = SpaceObject('Saturn', (237,219,173), np.float64(5.683e26), (-SpaceObject.AU*150-SpaceObject.AU*9.54, 0), (0,9_670), lengthYear=10_747)
# uranus2 = SpaceObject('Uranus', (147,205,241), np.float64(8.681e25), (-SpaceObject.AU*150+SpaceObject.AU*19.22, 0), (0,-6_790), lengthYear=30_687)
# neptune2 = SpaceObject('Neptune', (91,93,223), np.float64(1.024e26), (-SpaceObject.AU*150+SpaceObject.AU*30.06, 0), (0,-5_450), lengthYear=60_190)


key = []
running = True
objects = [sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune]#, sun2, mercury2, venus2, earth2, mars2, jupiter2, saturn2, uranus2, neptune2]
ms100 = py.USEREVENT + 100
py.time.set_timer(ms100, 100) # triggers every 100ms

font = py.font.Font(None, 32)
start_time = py.time.get_ticks() / 1000
mouse_clicked = False
py.mouse.set_system_cursor(py.SYSTEM_CURSOR_CROSSHAIR)
while running: 
    for event in py.event.get():
        if event.type == py.QUIT:
            running = False
            break

        if event.type == py.KEYDOWN:
            key.append(event.key)
        if event.type == py.KEYUP:
            key.remove(event.key)

        if event.type == ms100:
            print(*objects, sep='\n')

        if event.type == py.MOUSEBUTTONDOWN:
            mouse_clicked = True
        if event.type == py.MOUSEBUTTONUP: 
            mouse_clicked = False
        if mouse_clicked and event.type == py.MOUSEMOTION:
            mouseX, mouseY = event.rel 
            look[0] += mouseX
            look[1] += mouseY

        if event.type == py.MOUSEWHEEL:
            mouse_W = event.y
            if mouse_W > 0: [Calculations().rescale('+', objects) for _ in range(6)]
            else: [Calculations().rescale('-', objects) for _ in range(6)]   
    
    WIN.fill((0,0,0))

    
    for obj in objects:
        obj.display(WIN)
        obj.update(objects)

    vel_surface = font.render(f'{(60 * timeStep * (py.time.get_ticks()/1000 - start_time))/(60*60*24):.1f} days', True, (255,255,255))
    vel_rect = vel_surface.get_rect(center=(w//2,20))
    WIN.blit(vel_surface, vel_rect)

    if len(key) > 0:
        for k in key:
            if k == py.K_UP: Calculations().move('u')
            if k == py.K_DOWN: Calculations().move('d')
            if k == py.K_LEFT: Calculations().move('l') 
            if k == py.K_RIGHT: Calculations().move('r')
            if k == py.K_PLUS or k == py.K_KP_PLUS: Calculations().rescale('+', objects)
            if k == py.K_MINUS or k == py.K_KP_MINUS: Calculations().rescale('-', objects)
    
    py.display.flip()
    clock.tick(60)




py.quit()
