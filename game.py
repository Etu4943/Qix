import pygame
from enum import Enum
from pygame.locals import QUIT
import sys

ORIGINAL_SCREEN_SIZE = (256, 240)
SPEED = 4
LOW_SPEED = 2
Orientation = Enum('Orientation', ['VERTICAL', 'HORIZONTAL'])

def increase_resolution_multiplicator(x,y,multiplicator):
    return (x * multiplicator,y * multiplicator)

def validate_border(width,heigth,obj_size):
    border_cells = set()
    border_cells.update([(x,y) for x in range(width-obj_size) for y in range(heigth-obj_size) if x == 0 or y == 0 or x == width-obj_size-4 or y == heigth-obj_size-2])
    return border_cells

def fill_inside(path):
    pass
def move(keys):
    deplacement = (0,0)
    if len(keys) == 2 :
        if pygame.K_l in keys and pygame.K_a in keys:
            deplacement = (SPEED,0)
        elif pygame.K_j in keys and pygame.K_a in keys:
            deplacement = (-SPEED,0)
        elif pygame.K_k in keys and pygame.K_a in keys:
            deplacement = (0,SPEED)
        elif pygame.K_i in keys and pygame.K_a in keys:
            deplacement = (0,-SPEED)
        elif pygame.K_l in keys and pygame.K_b in keys:
            deplacement = (LOW_SPEED,0)
        elif pygame.K_j in keys and pygame.K_b in keys:
            deplacement = (-LOW_SPEED,0)
        elif pygame.K_k in keys and pygame.K_b in keys:
            deplacement = (0,LOW_SPEED)
        elif pygame.K_i in keys and pygame.K_b in keys:
            deplacement = (0,-LOW_SPEED)
    else :
        if pygame.K_l in keys :
            deplacement = (SPEED,0)
        elif pygame.K_j in keys :
            deplacement = (-SPEED,0)
        elif pygame.K_k in keys:
            deplacement = (0,SPEED)
        elif pygame.K_i in keys:
            deplacement = (0,-SPEED)
        elif pygame.K_l in keys :
            deplacement = (LOW_SPEED,0)
        elif pygame.K_j in keys :
            deplacement = (-LOW_SPEED,0)
        elif pygame.K_k in keys :
            deplacement = (0,LOW_SPEED)
        elif pygame.K_i in keys :
            deplacement = (0,-LOW_SPEED)
        else :
            deplacement = (0,0)
    
    return deplacement

def is_in_bounds(x,y,width,heigth,obj_size):
    return x in range(width-obj_size) and y in range(heigth-obj_size)

def color_valide_cells(valide_cells,screen,obj_size):
    for x, y in valide_cells :
        for i in range(obj_size) :
            for j in range(obj_size) :
                screen.set_at((x+i,y+j), pygame.color.Color('white'))
    return screen

def get_every_cell_around(validate_cells,covered,x,y):
    print("Origine pos : ", (x,y))
    covered.append((x,y))
    for i in range(-1,1):
        for j in range(-1,1):
            if (x+(i*SPEED),y+(j*SPEED)) != (x,y) and (x+(i*SPEED),y+(j*SPEED)) not in covered and (x+(i*SPEED),y+(j*SPEED)) not in validate_cells:
                covered.append((x+(i*SPEED),y+(j*SPEED)))
                get_every_cell_around(validate_cells,covered,x+(i*SPEED),y+(j*SPEED))
    return covered 

def get_small_part_coo(screen,new_path):
    straigth_line = None
    orientation = None
    i = 1
    while i in range(len(new_path)-1) and straigth_line == None :
        x, y = new_path[i]
        prev_x, prev_y = new_path[i-1]
        next_x, next_y = new_path[i+1]
        if (x-SPEED,y) not in new_path and (x+SPEED,y) not in new_path and (x,y+SPEED) in new_path and (x,y-SPEED) in new_path:
            straigth_line = (x,y)
            orientation = Orientation.HORIZONTAL
        elif (x-SPEED,y) in new_path and (x+SPEED,y) in new_path and (x,y+SPEED) not in new_path and (x,y-SPEED) not in new_path :
            straigth_line = (x,y)
            orientation = Orientation.VERTICAL
            
        i += 1
    return *straigth_line, orientation

def main():
    

    # Initialise screen
    pygame.init()
    screen = pygame.display.set_mode(increase_resolution_multiplicator(*ORIGINAL_SCREEN_SIZE,2))
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
    pygame.display.set_caption("Moving Object Using PyGame")
    clock = pygame.time.Clock()
    
    obj_width = 4
    obj_height = 4
    obj_x = 0
    obj_y = 0
    obj_speed = 4

    # Event loop
    wanna_play = True
    is_pressed = False
    nb_pressed = 0
    keys = []
    validate_cells = validate_border(*screen.get_size(),obj_width)
    new_path = []
    new_path_closed = False
    prev_coo = None
    blue_covered = []
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
            gap_x, gap_y = move(keys)
            movement = (gap_x, gap_y)
            mov_x = obj_x + gap_x
            mov_y = obj_y + gap_y
            if nb_pressed == 1 :
                if is_in_bounds(mov_x,mov_y,*screen.get_size(),obj_width) and (mov_x,mov_y) in validate_cells:
                    obj_x += gap_x
                    obj_y += gap_y
                    coo = (obj_x, obj_y)
                    print(coo)
                    prev_coo = coo
            else :
                if is_in_bounds(mov_x,mov_y,*screen.get_size(),obj_width) and (mov_x,mov_y) not in new_path and (prev_coo not in validate_cells or (mov_x,mov_y) not in validate_cells): 
                    obj_x += gap_x
                    obj_y += gap_y
                    coo = (obj_x, obj_y)
                    if coo in validate_cells :
                        validate_cells.update(new_path)
                        x,y, orientation = get_small_part_coo(screen,new_path)
                        if orientation == Orientation.VERTICAL :
                            print("Barre verticale")
                            blue_covered = get_every_cell_around(validate_cells,blue_covered,x,y-(1*SPEED))
                        if orientation == Orientation.HORIZONTAL :
                            blue_covered = get_every_cell_around(validate_cells,blue_covered,x-(1*SPEED),y)
                        print("covered", blue_covered)
                        new_path = []
                        new_path_closed = True
                    else :
                        new_path.append(coo)
            
                    prev_coo = coo
                
                    

        screen.blit(background, (0, 0))
        
            
        #obj_x += obj_speed

        # Draw the object and update the display
        screen.fill((0, 1, 1))  
        screen = color_valide_cells(validate_cells,screen,obj_width)
        screen = color_valide_cells(blue_covered,screen,obj_width)
        pygame.draw.rect(screen, (150, 255, 0), (obj_x, obj_y, obj_width, obj_height))
        pygame.display.flip()
        clock.tick(60)
        

if __name__ == "__main__":
    main()