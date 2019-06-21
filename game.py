import pygame 
import random
from creature import *


level1 = """
######################
#...##.....>.##....$$#
#...##...P.........$$#
#.b.##...P.........$$#
#.b.##.......##....$$#
#.b.###########....$$#
#.b................$$#
#.bbbbbbbbbbbb.....$$#
#..................$$#
######################
"""

level2 = """
######################
#......#.K...........#
#....K.#............<#
#......#..K..........#
#.K....#.#############
#......#.............#
#...K..#............>#
#......#....##########
#..............a....c#
######################
"""

level3 = """
######################
#########$$$$$$$$$$$$#
#########......D....$#
#<......#...........$#
#.................D.$#
#....................#
#.......#......D.....#
#########............#
#########...........<#
######################
"""

food = {"a":("apple",5,0, pygame.image.load("apple.png")),
        "b":("banana",6,2, pygame.image.load("apple.png")),
        "p":("pork",9,0, pygame.image.load("apple.png")),
        "r":("rotten meat",4,-2, pygame.image.load("apple.png")),
        "c":("cake",17,0, pygame.image.load("cake.png")),
        "h":("big health potion",0,42, pygame.image.load("cake.png"))}

"""
food = {"a":("apple",5,0),
        "b":("banana",6,2),
        "p":("pork",9,0),
        "r":("rotten meat",4,-2),
        "c":("cake",17,0),
        "h":("big health potion",0,42)}
"""

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0 , 255)
WALL = (101, 67, 33)
FLOOR = (242, 243, 244)
BLACK = (0, 0, 0)
FONT = (0, 168, 107)

class Particle(pygame.sprite.Sprite):
    
    def __init__(self, x, y, speed=50, move_x=None, move_y=None, color=None):
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x
        self.y = y
        if move_x is None:
            self.move_x = random.random() * speed - speed/2
        else:
            self.move_x = move_x
        if move_y is None:
            self.move_y = random.random() * speed - speed/2
        else:
            self.move_y = move_y
        if color is None:
            self.color = WHITE
        else:
            self.color = color
        self.lifetime = 1 + random.random() * 1.5
        self.image = pygame.Surface((5,5))
        pygame.draw.circle(self.image, self.color, (2,2), 2)
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        
    def update(self, seconds):
        self.lifetime -= seconds
        if self.lifetime < 0:
            self.kill()
        self.x += self.move_x * seconds
        self.y += self.move_y * seconds
        self.rect.center = (round(self.x, 0), round(self.y,0))
        
        

class Game(object):
    width = 0
    height = 0
    def __init__(self, width=600, height=500, fps=30):
        pygame.init()
        pygame.display.set_caption("Press ESC to quit")
        self.width = width
        self.height = height
        Game.width = width
        Game.height = height
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF)
        self.background = pygame.Surface(self.screen.get_size()).convert()  
        self.background.fill(WHITE) # fill background white
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.playtime = 0.0
        self.font = pygame.font.SysFont('mono', 32, bold=True)
        self.log = []
        self.log.append("Welcome")
        self.turn = 0
        self.allgroup = pygame.sprite.LayeredUpdates()
        self.particlegroup = pygame.sprite.Group()
        Particle.groups = self.allgroup, self.particlegroup
        # ------ generiere creature -------
        self.hero = Hero(1,1,0)

        self.levels = []
        for z, levelstring in enumerate((level1, level2, level3)):
            
            level = []
            for line in levelstring.split():
                level.append(list(line))
                

            for y, line in enumerate(level) :
                for x, char in enumerate(line) :
                    if char in "DKP" :
                        level[y][x] = "."
                        if char == "P":
                            Pig(x,y,z)
                        elif char == "D" :
                            Dragon(x,y,z)            
                        elif char == "K" :
                            Kobold(x,y,z)            
            self.levels.append(level)

    def levelchange(self):
        self.tilesy = len(self.levels[self.hero.z])
        self.tilesx = len(self.levels[self.hero.z][0])
        self.widthx = (self.width - 100) / self.tilesx
        self.widthy = (self.height - 100) / self.tilesy
        self.gridsizex = self.width - 100
        self.gridsizey = self.height - 100
        self.tile = int(min(self.widthx, self.widthy))
        self.wall = pygame.Surface((self.tile, self.tile))
        
        
        self.wall.fill(WALL) # Walls
        image_wall = pygame.image.load("platform.png")
        image_wall = pygame.transform.scale(image_wall, (self.tile, self.tile))
        self.wall.blit(image_wall, (0, 0))
        self.wall.convert()
        self.ground = pygame.Surface((self.tile, self.tile))
        self.ground.fill(FLOOR) # Floor
        image_floor = pygame.image.load("floor.png")
        image_floor = pygame.transform.scale(image_floor, (self.tile, self.tile))
        self.ground.blit(image_floor, (0, 0))
        self.ground.convert()
       




    def paintgrid(self, color = BLACK):
        for x in range(0, self.tilesx * self.tile, self.tile):
            pygame.draw.line(self.background, color, (x,0),
                (x, self.tilesy * self.tile), 1)
        for y in range(0, self.tilesy * self.tile, self.tile):
            pygame.draw.line(self.background, color, (0,y),
                (self.tilesx * self.tile, y), 1)
                   

    # LOG
    def paintlog(self):
        self.background.fill(WHITE)
        y = self.height - 20
        i = 0
        for line in self.log:
            self.draw_text(line,  5, y, (i,i,i), 15, self.background)
            y -= 20
            i += 5
            i = min(255,i) 
            if y < self.tile * self.tilesy:
                break
        


    def paint(self):
        """painting on the surface"""
        self.paintlog()
        
        for y, line in enumerate(self.levels[self.hero.z]):
            for x, char in enumerate(line):
                self.background.blit(self.ground, (x*self.tile, y*self.tile))
                for num, creature in Creature.creatures.items():
                    if creature.hp < 1:
                        continue
                    if creature.x == x and creature.y == y and creature.z == self.hero.z:
                        self.draw_text(creature.char, x*self.tile, y*self.tile, creature.color, 24, self.background, creature.image)
                        break
                else:        
                    if char == "#":
                        self.background.blit(self.wall, (x*self.tile, y*self.tile))
                    elif char == ".":
                        pass
                    else:
                        self.draw_text(char, x*self.tile, y*self.tile, GREEN, 24, self.background)


        self.paintgrid()
        x = self.gridsizex - self.tile / 2 
        self.draw_text("HP: {}".format(self.hero.hp), x, 10, FONT, 20, self.background)
        self.draw_text("Hunger: {}".format(self.hero.hunger), x, 25, FONT, 15, self.background)
        self.draw_text("Gold: {}".format(self.hero.money), x, 40, FONT, 15, self.background)
        self.draw_text("x:{} y:{} z:{}".format(self.hero.x, self.hero.y, self.hero.z), x, 55, FONT, 15, self.background)
        self.draw_text("turn: {}".format(self.turn), x, 70, FONT, 15, self.background)
        self.draw_text("evade: {:.1f}%".format(self.hero.evade*100), x, 85, FONT, 15, self.background)
        self.draw_text("Hit: {:.1f}%".format(self.hero.hit*100), x, 100, FONT, 15, self.background)
        self.draw_text("maxDamge: {}".format(self.hero.maxdamage), x, 115, FONT, 15, self.background)
 
                
        
    def teleport(self, distance=5):
        teleports = [] # list of valid teleports
        teleports.append((0,0)) # add start position
        for move_y in range(-distance, distance+1):
            if self.hero.y + move_y < 0:
                continue
            if self.hero.y + move_y > len(self.levels[self.hero.z]):
                continue
            for move_x in range(-distance, distance+1):                    
                if self.hero.x + move_x < 0:
                    continue
                if self.hero.x + move_x > len(self.levels[self.hero.z][self.hero.y]):
                    continue
                if (move_x**2 + move_y**2)**0.5 > distance:
                    continue
                if self.levels[self.hero.z][self.hero.y+move_y][self.hero.x+move_x] == ".":
                    teleports.append((move_x,move_y))
        move_x, move_y = random.choice(teleports)
        if move_x == 0 and move_y == 0:
            self.log.insert(0,"The telporter sends you to your old position.")
            return
        self.log.insert(0,"The telporter sends you to a new random position.")
        self.hero.x += move_x
        self.hero.y += move_y
            
            
    
    
    def gameturn(self, command="", arg2=None):
        # ------------ new game turn  -------------
        self.turn += 1
        self.hero.hunger += 1
       
        print("pos:", self.hero.x, self.hero.y, self.hero.z)
        move_x = 0
        move_y = 0
        mytile = self.levels[self.hero.z][self.hero.y][self.hero.x]
        if command == "LEFT":
            move_x = -1
        elif command == "RIGHT":
            move_x = 1
        elif command == "UP":
            move_y = -1
        elif command == "DOWN":
            move_y = 1
        elif command == "WAIT":
            self.log.insert(0, "WE WAIT")
        elif command == "TELEPORT":
            if mytile == ">":
                self.hero.z += 1
                self.levelchange()
                #self.paint()
            elif mytile == "<":
                self.hero.z -= 1
                self.levelchange()
        
    
        # --------legal move? ---------
        if (self.hero.x + move_x < 0 or 
            self.hero.x + move_x > len(self.levels[self.hero.z][self.hero.y]) or
            self.hero.y < 0 or
            self.hero.y > len(self.levels[self.hero.z])):
            move_x = 0
            move_y = 0
        elif self.levels[self.hero.z][self.hero.y + move_y][self.hero.x + move_x] == "#":
            move_x = 0
            move_y = 0
        else:
            # --- run into Creature? -----
            for creature in Creature.creatures.values():
                if creature.number == self.hero.number:
                    continue
                elif creature.hp <1:
                    continue
                elif creature.z != self.hero.z:
                    continue
                elif creature.x == self.hero.x + move_x and creature.y == self.hero.y + move_y:
                    self.log.insert(0, "You fight against " + creature.report())
                    self.fight(self.hero, creature)
                    if creature.hp < 1:
                        self.hero.money += random.randint(0,10)
                    move_x = 0
                    move_y = 0
                    break
            self.hero.x += move_x
            self.hero.y += move_y
            self.paint()
                
        ## ----------Auswertung----------
        stuff = self.levels[self.hero.z][self.hero.y][self.hero.x]
        ## ------ Rätselkiste ---- 
        #if stuff == "?":
            #riddlebox(hero)
                
        ## ------ teleport --------
        if stuff == ":":
            self.teleport()
            self.paint()
        ## ------ food and money -----
        elif stuff in food:
                #print("You eat : ", food[stuff][0])
                self.log.insert(0,"You eat : {}".format(food[stuff][0]))
                self.hero.hunger -= food[stuff][1]
                self.hero.hp += food[stuff][2]
                self.levels[self.hero.z][self.hero.y][self.hero.x] = "."
        elif stuff == "$":
                self.log.insert(0, "You found gold!")
                self.hero.money += random.randint(1, 20)
                self.levels[self.hero.z][self.hero.y][self.hero.x] = "."
        elif stuff == ">":
            self.log.insert(0, "It is Teleport. Press T")
        elif stuff == "<":
            self.log.insert(0, "It is Teleport. Press T")

        # ---- end ----
        self.paint()
        # -------- moving creatures -----
        for creature in Creature.creatures.values():
            if creature.number == self.hero.number:
                continue 
            if creature.z != self.hero.z:
                continue
            if creature.hp < 1:
                continue # no dead creatures moving around!
            move_x, move_y = creature.move()
            if move_x == 0 and move_y == 0:
                continue
            try:
                target = self.levels[self.hero.z][creature.y+move_y][creature.x+move_x]
            except:
                continue
            #if creature.x + move_x < 0 or creature.x + move_x > len(line) or creature.y + move_y < 0 or creature.y+move_y >len(level):
                #move_x = 0
                #move_y = 0
            if target in "#<>:sd":
                continue
            for creature2 in Creature.creatures.values():
                if creature2.number == creature.number:
                    continue
                if creature2.hp < 1:
                    continue
                if creature2.z != self.hero.z:
                    continue
                if creature.x + move_x == creature2.x and creature.y+move_y == creature2.y:
                    move_x = 0
                    move_y = 0
                    if creature2.number == self.hero.number:
                        self.log.insert(0, "A wandering creature attacks you!")
                        self.fight(creature, self.hero)
                        
                    break
            creature.x += move_x
            creature.y += move_y
            #if hero.hp <1:
                #break


    
    
    def run(self):
        self.levelchange()
        self.paint() 
        running = True
        while running:
            milliseconds = self.clock.tick(self.fps)
            seconds = milliseconds / 1000.0
            self.playtime += seconds
            #self.draw_text("FPS: {:6.3}{}PLAYTIME: {:6.3} SECONDS".format(self.clock.get_fps(), " "*5, self.playtime), self.width-250, self.height-10, (0,0,0), 10)
            
            if self.hero.hp < 1 or self.hero.hunger > 100:
                break
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False 
                elif event.type == pygame.KEYDOWN:
                    # keys that you press once and release
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_w or event.key == pygame.K_UP:
                        self.gameturn("UP")
                    elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                        self.gameturn("DOWN")
                    elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                        self.gameturn("LEFT")
                    elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                        self.gameturn("RIGHT")
                    elif event.key == pygame.K_SPACE or event.key == pygame.K_PERIOD:
                        self.gameturn("WAIT")
                    elif event.key == pygame.K_t:
                        self.gameturn("TELEPORT")
                        
                        
            pressedkeys = pygame.key.get_pressed() # keys that you can press all the time
            #self.allgroup.clear(self.screen, self.background)
            self.screen.blit(self.background, (0, 0))
            self.allgroup.update(seconds)
            self.allgroup.draw(self.screen)    
            pygame.display.flip()
            
        pygame.quit()

    def attack(self, angreifer, verteidiger):
        msg = "{} is attacking {}!".format(angreifer.name, verteidiger.name)
        self.log.insert(0, msg)
        attack = random.random() # 0...1
        evade = random.random()
        damage = random.randint(1, angreifer.maxdamage)
        if attack < angreifer.hit:
             msg = "Attack successfull!!"
             self.log.insert(0,msg)
             if evade < verteidiger.evade:
                 msg = "but {} can evade!".format(verteidiger.name)
                 self.log.insert(0, msg)
             else:
                 msg = "{} make {} damage ({} hp left)".format(angreifer.name, damage, verteidiger.hp-damage)
                 self.log.insert(0, msg)
                 verteidiger.hp -= damage
        else:
             msg = "Attack failed!"
             self.log.insert(0, msg)
        #return msg

    def fight(self, angreifer, verteidiger):
        x = verteidiger.x * self.tile + self.tile/2
        y = verteidiger.y * self.tile + self.tile/2
        for p in range(25):
            Particle(x,y)
        #battleround = 0
        #battleround += 1
        #print("---------- Battle Round {} ----------".format(battleround))
        self.attack(angreifer, verteidiger)
        if verteidiger.hp < 1:
            self.log.insert(0,"{} wins!".format(angreifer.name))
            #del Creature.creatures[verteidiger.number]
            return
        self.paint()
        self.attack(verteidiger, angreifer)
        if angreifer.hp < 1:
            self.log.insert(0,"{} wins!".format(verteidiger.name))
            return
            #input("press enter")
        self.paint()
        


    def draw_text(self, text, x=None, y=None, textcolor=None, fontsize=None, surface=None, im = None):
        """Center text in window"""
        if x is None:
            x = 50
        if y is None:
            y = 150
        if fontsize is None:
            fontsize = 24
        if textcolor is None:
            textcolor = (0, 0, 0)
        if surface is None:
            surface = self.screen
        font = pygame.font.SysFont('mono', fontsize, bold=True)
        fw, fh = font.size(text)
        output = font.render(text, True, (textcolor))
        
        if text in food :
            im = food[text][3]
            #im = pygame.
            im = pygame.transform.scale(im, (self.tile, self.tile))
            surface.blit(im, (x, y))
        elif text == "$" :
            gold = pygame.image.load("gold.jpg")
            gold = pygame.transform.scale(gold, (self.tile, self.tile))
            surface.blit(gold, (x, y))
        elif im != None :
            im = pygame.transform.scale(im, (self.tile, self.tile))
            surface.blit(im, (x, y))
        surface.blit(output, (x, y))


if __name__ == '__main__':
    Game(1600,800).run() # call with width of window and fps
