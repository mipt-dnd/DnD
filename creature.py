import random
import pygame

class Creature():
    number = 0
    creatures = {}
    
    def __init__(self, x=0, y=1, z=0, hp=10, name = "creature",
                 hit = 0.5, evade = 0.25, maxdamage = 3, char="?", image = ""):
        self.hp = hp
        self.x = x
        self.y = y
        self.z = z
        self.name = name
        self.hit = hit
        self.evade = evade
        self.maxdamage = maxdamage
        self.number = Creature.number
        Creature.number += 1
        Creature.creatures[self.number] = self
        self.char = char
        self.color = (255,0,0)
        self.image = image
        
    
    def report(self):
        return "creature: {} hp: {} hit: {} ev: {} maxdmg: {}".format(self.name,  self.hp, self.hit, self.evade, self.maxdamage)
    
    def move(self):
        return 0, 0
 
class Pig(Creature):
    def __init__(self, posx, posy, posz):
        Creature.__init__(self, posx, posy, posz, 2, "Pig", 0.6, 0.8, 1, "P")
        self.color = (180, 0, 0)
        self.image = pygame.image.load("pig.png")
         
class Dragon(Creature):
    def __init__(self,posx, posy, posz):
        Creature.__init__(self, posx, posy, posz, 30, "Dragon", 0.25, 0.1, 22, "D")
        self.color = (255, 0, 0)
        self.image = pygame.image.load("dragon.png")
    def move(self):
        return random.choice((-1,0, 0, 1)), random.choice((-1, 0, 0, 1))
        
        
class Kobold(Creature):
    def __init__(self,posx, posy, posz):
        Creature.__init__(self,posx, posy, posz, 3, "Kobold", 0.8, 0.01, 1, "K")
        self.color = (0, 150, 150)
        self.image = pygame.image.load("kobold.png")
    def move(self):
        return random.choice((-1,0,0,0,1)), random.choice((-1,0,0,0,1))
         
class Hero(Creature):
    def __init__(self,posx, posy, posz):
        Creature.__init__(self,posx, posy, posz, 10, "Gilyana", 0.7, 0.3, 7, "@")
        self.hunger = 0
        self.money = 0
        self.color = (0,0,255)
        self.image = pygame.image.load("hero.png")

