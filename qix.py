import pygame
from random import randint
from math import sqrt
from enum import Enum
from pygame.locals import QUIT
import sys


sys.setrecursionlimit(10**6)

ORIGINAL_SCREEN_SIZE = (256, 240)
SPEED = 4
LOW_SPEED = 4
Orientation = Enum('Orientation', ['VERTICAL', 'HORIZONTAL'])
Direction = Enum("Direction", ["HAUT","BAS","GAUCHE","DROITE"])
Side = Enum("Side", ["HAUT","BAS","GAUCHE","DROIT"])

def distance(co1, co2):
    return sqrt(pow(abs(co1[0] - co2[0]), 2) + pow(abs(co1[1] - co2[1]), 2))

def most_close_coo(enemy,list_path):
    nearest = min(list_path, key=lambda x: distance(x[0], enemy))
    return nearest

def increase_resolution_multiplicator(x,y,multiplicator):
    return (x * multiplicator,y * multiplicator)

def validate_border(width,heigth,obj_size):
    border_cells = set()
    border_cells.update([(x,y) for x in range(width-obj_size) for y in range(heigth-obj_size) if x == 0 or y == 0 or x == width-obj_size-4 or y == heigth-obj_size-4])
    return border_cells

def what_side(x,y,screen):
    length, width = screen.get_size()
    side = None
    if x == 0 :
        side = Side.HAUT
    elif y == 0 :
        side = Side.GAUCHE
    elif x == length :
        side = Side.BAS
    elif y == width :
        side = Side.DROIT
    return side

def fill_inside(path):
    pass

def move(keys):
    deplacement = (0,0)
    direction = None
    if len(keys) == 2 :
        if pygame.K_l in keys and pygame.K_a in keys:
            deplacement = (SPEED,0)
            direction = Direction.DROITE
        elif pygame.K_j in keys and pygame.K_a in keys:
            deplacement = (-SPEED,0)
            direction = Direction.GAUCHE
        elif pygame.K_k in keys and pygame.K_a in keys:
            deplacement = (0,SPEED)
            direction = Direction.BAS
        elif pygame.K_i in keys and pygame.K_a in keys:
            deplacement = (0,-SPEED)
            direction = Direction.HAUT
        elif pygame.K_l in keys and pygame.K_b in keys:
            deplacement = (LOW_SPEED,0)
            direction = Direction.DROITE
        elif pygame.K_j in keys and pygame.K_b in keys:
            deplacement = (-LOW_SPEED,0)
            direction = Direction.GAUCHE
        elif pygame.K_k in keys and pygame.K_b in keys:
            deplacement = (0,LOW_SPEED)
            direction = Direction.BAS
        elif pygame.K_i in keys and pygame.K_b in keys:
            deplacement = (0,-LOW_SPEED)
            direction = Direction.HAUT
    else :
        if pygame.K_l in keys :
            deplacement = (SPEED,0)
            direction = Direction.DROITE
        elif pygame.K_j in keys :
            deplacement = (-SPEED,0)
            direction = Direction.GAUCHE
        elif pygame.K_k in keys:
            deplacement = (0,SPEED)
            direction = Direction.BAS
        elif pygame.K_i in keys:
            deplacement = (0,-SPEED)
            direction = Direction.HAUT
        else :
            deplacement = (0,0)
    
    return *deplacement, direction

def is_in_bounds(x,y,width,heigth,obj_size):
    return x in range(width-obj_size) and y in range(heigth-obj_size)

def color_valide_cells(valide_cells,screen,obj_size,color="white"):
    for x, y in valide_cells :
        for i in range(obj_size) :
            for j in range(obj_size) :
                screen.set_at((x+i,y+j), pygame.color.Color(color))
    return screen

def add_to_surface(init_x,init_y,new_path,validate_cells,obj_size,tested_cells):
    for i in range(-1,2) :
        for j in range(-1,2) :
            movement = (init_x + i*obj_size, init_y + j*obj_size)
            if movement not in new_path and movement not in validate_cells and movement not in tested_cells:
                tested_cells.append(movement)
                tested_celles = add_to_surface(*movement,new_path,validate_cells,obj_size,tested_cells)
    return tested_cells
def recursive_played_cells(init_x,init_y,new_path,validate_cells,obj_size,enemy_pos,tested_cells,is_found = False):
    if not is_found :
        for i in range(-1,2) :
            for j in range(-1,2) :
                movement = (init_x + i*obj_size, init_y + j*obj_size)
                if movement not in new_path and movement not in validate_cells and movement not in tested_cells:
                    if movement in enemy_pos :
                        is_found = True
                    else :
                        tested_cells.append(movement)
                        is_found, tested_cells = recursive_played_cells(*movement,new_path,validate_cells,obj_size,enemy_pos,tested_cells)
                    #validate_cells.add(movement)
    return is_found, tested_cells          

def get_surface_cells(new_path, screen, validate_cells):
    max_x = max(new_path, key=lambda item : item[0])[0]
    max_y = max(new_path, key=lambda item : item[1])[1]
    for i in range(0,max_x,SPEED) :
        for j in range(0,max_y,SPEED) :
            if (i,j) not in validate_cells :
                validate_cells.add((i,j))

def color_blue(blue_colored,surface,obj_width):
    for x,y in blue_colored :
        pygame.draw.rect(surface, (0,0,255), pygame.Rect(x,y,obj_width,obj_width))

def enemy_side(enemy, new_path):
    for i in range(3):
        pass

class enemy :
    def __init__(self, width, heigth, speed, pos):
        self.width = width
        self.heigth = heigth
        self.x = pos[0]
        self.y = pos[1]
        self.speed = speed
    
    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y
    
    def get_width(self):
        return self.width
    
    def get_heigth(self):
        return self.heigth
    
    def get_values(self):
        return self.x, self.y, self.width, self.heigth
    
    def move(self, validate_path, max_x, max_y):
        mutl_speed = randint(1,10)
        gap_x = randint(-1,1)
        gap_y = randint(-1,1)
        move_x = self.x + gap_x * self.speed
        move_y = self.y + gap_y * self.speed
        i = 0
        while gap_x == 0 or gap_y == 0 or (move_x,move_y) in validate_path or (move_x + self.width, move_y + self.width) in validate_path or (move_x + self.width, move_y) in validate_path or (move_x, move_y + self.width) in validate_path : # Pas besoin de vérifier l'appartenance à la grille car elle est entourée de validate path !!
            print("Position impossible :",i)
            gap_x = randint(-1,1)
            gap_y = randint(-1,1)
            move_x = self.x + gap_x * self.speed
            move_y = self.y + gap_y * self.speed 
            i += 1
        self.width = 4 * randint(4,32)//4
        self.x = move_x 
        self.y = move_y 
    
    
            
        

def get_small_part_coo(screen,new_path):
    straigth_line = None
    orientation = None
    i = 1
    lines = []
    while i in range(len(new_path)-1):
        x, y = new_path[i]
        prev_x, prev_y = new_path[i-1]
        next_x, next_y = new_path[i+1]
        if (x-SPEED,y) not in new_path and (x+SPEED,y) not in new_path and (x,y+SPEED) in new_path and (x,y-SPEED) in new_path:
            straigth_line = (x,y)
            orientation = Orientation.VERTICAL
            lines.append((straigth_line,orientation))
        elif (x-SPEED,y) in new_path and (x+SPEED,y) in new_path and (x,y+SPEED) not in new_path and (x,y-SPEED) not in new_path :
            straigth_line = (x,y)
            orientation = Orientation.HORIZONTAL
            lines.append((straigth_line,orientation))
            
        i += 1
    return lines



def main():
    

    # Initialise screen
    pygame.init()
    screen_dimension = increase_resolution_multiplicator(*ORIGINAL_SCREEN_SIZE,2)
    screen = pygame.display.set_mode(screen_dimension)
    pygame.display.set_caption('Première images du Qix')

    # Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))

    # Display some text
    font = pygame.font.Font(None, 36)
    text = font.render("QIX", 1, (10, 10, 10))
    textpos = text.get_rect()
    textpos.centerx = background.get_rect().centerx
    background.blit(text, textpos)

    # Blit everything to the screen
    screen.blit(background, (0, 0))
    pygame.display.flip()
    
    
    
    #win_width = 600
    #win_height = 500
    #game_window = pygame.display.set_mode((win_width, win_height))
    clock = pygame.time.Clock()
    
    obj_width = 4
    obj_height = 4
    obj_x = screen.get_size()[0] // 2
    obj_y = screen.get_size()[1] - 2*obj_width
    obj_speed = 4
    
    """
    enemy_width = 15
    enemy_height = 15
    enemy_x = 120
    enemy_y = 240
    enemy_pos = [(enemy_x, enemy_y)]
    """
    qix = enemy(16, 16, 4, (120, 240))

    # Event loop
    wanna_play = True
    is_pressed = False
    nb_pressed = 0
    keys = []
    validate_cells = validate_border(*screen.get_size(),obj_width)
    new_path = []
    new_path_closed = False
    prev_coo = (0,0)
    prev_direction = None
    blue_covered = set()
    blue = pygame.Surface(screen_dimension)
    corners = []
    coo_start_path = None
    coo_end_path = None
    
    screen.fill((0, 1, 1))
    while wanna_play:
        
        if new_path_closed :
            pygame.time.wait(1000)
            new_path_closed = False
        
        for event in pygame.event.get(): 
            if event.type == QUIT:
                wanna_play = False
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
             
            # checking if keydown event happened or not
            
            if event.type == pygame.KEYDOWN: # Pour toutes les touches potentiellement touchées
                is_pressed = True
                nb_pressed += 1
                key = event.key
                keys.append(key)
            if event.type == pygame.KEYUP:
                is_pressed = False
                nb_pressed -= 1
                key = event.key
                keys.remove(key)
        
        if 0 < nb_pressed <= 3 :
            gap_x, gap_y, direction = move(keys)
            
            movement = (gap_x, gap_y)
            mov_x = obj_x + gap_x
            mov_y = obj_y + gap_y
            if nb_pressed == 1 :
                if is_in_bounds(mov_x,mov_y,*screen.get_size(),obj_width) and (mov_x,mov_y) in validate_cells:
                    obj_x += gap_x
                    obj_y += gap_y
                    coo = (obj_x, obj_y)
            else :
                
                if is_in_bounds(mov_x,mov_y,*screen.get_size(),obj_width) and (mov_x,mov_y) not in new_path and (prev_coo not in validate_cells or (mov_x,mov_y) not in validate_cells) and (mov_x,mov_y) not in blue_covered: 
                    obj_x += gap_x
                    obj_y += gap_y
                    coo = (obj_x, obj_y)
                    if coo in validate_cells :
                        validate_cells.update(new_path)
                        
                        list_lines = get_small_part_coo(screen,new_path)
                        validate_cells.update([elem for elem, orientation in list_lines])
                       
                        best = most_close_coo((qix.get_x(),qix.get_y()),list_lines)
                        best_x, best_y = best[0][0],best[0][1]
                        if best[1] == Orientation.VERTICAL :
                            if qix.get_x() > best_x : # Si enemy est à droite
                                side = (best_x - 1 * obj_width, best_y)
                            else :
                                side = (best_x + 1 * obj_width, best_y)
                        else :
                            if qix.get_y() > best_y : # Si enemy est plus bas
                                side = (best_x, best_y - 1 * obj_width)
                            else :
                                side = (best_x, best_y + 1 * obj_width)
                        tested_cells = add_to_surface(*side,new_path,validate_cells,obj_width,[])
                        blue_covered.update(tested_cells)
                        color_blue(blue_covered,blue,obj_width)
                        new_path = []
                        new_path_closed = True
                    else :
                        new_path.append(coo)
                        
            
                    
                    if direction != prev_direction and prev_coo not in validate_cells:
                        corners.append(coo)
                    prev_coo = coo
                    prev_direction = direction
                    

        screen.blit(background, (0, 0))
        
            
        #obj_x += obj_speed

        # Draw the object and update the display
        screen.fill((0, 1, 1))
        screen.blit( blue, ( 0, 0 ) )
        screen = color_valide_cells(validate_cells,screen,obj_width)
        screen = color_valide_cells(new_path,screen,obj_width,"red")
        
        pygame.draw.rect(screen, (255, 0, 0), (obj_x, obj_y, obj_width, obj_height))
        qix.move(validate_cells,*screen.get_size())
        pygame.draw.rect(screen, (150, 0, 0), qix.get_values())
        pygame.display.flip()
        clock.tick(60)
        

if __name__ == "__main__":
    main()