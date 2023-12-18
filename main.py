import os
DATA = {"is_playable" : False}
TAILLE_GRILLE = 20
WHITE = 47
ORIGINAL_BACKGROUND = "48;5;238"

def clear_screen():
    if os.name == "posix" :
        os.system("clear")
    else:
        os.system("cls")

def create_grid():
    grid = [[{"is_playable" : False, "color" : ORIGINAL_BACKGROUND} for _ in range(TAILLE_GRILLE)] for _ in range(TAILLE_GRILLE)]
    return grid

def setup():
    grid = create_grid()
    for x in range(TAILLE_GRILLE):
        for y in range(TAILLE_GRILLE) :
            if x == 0 or y == 0 or x == TAILLE_GRILLE - 1 or y == TAILLE_GRILLE - 1:
                grid[x][y]["is_playable"] = True
                grid[x][y]["color"] = WHITE
    return grid

def get_colored_text(text,color):
    return f"\x1b[{color}m{text}\x1b[0m"

def print_grid(grid):
    clear_screen()
    for line in grid :
        for elem in line :
            #print(elem["color"],end=" ")
            print(get_colored_text("  ",elem["color"]),end="")
        print()
    

def main():
    grid = setup()
    print_grid(grid)
    

if __name__ == "__main__" :
    main()