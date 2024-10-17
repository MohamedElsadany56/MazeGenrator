import pygame
from random import choice
from collections import deque
from queue import PriorityQueue
import sys




# By 
#          Name           |     ID
# _____________________________________
# |Ahmed magdy elhussiney |  221001359 |
# |Amr Hamouda            |  221001776 | 
# |Mohamed Goma           |  221001823 |
# |____________________________________|


# Screen resolution
RES = WIDTH, HEIGHT = 920, 720         # gride  Size 
RES2 = WIDTH2, HEIGHT2 = 1100, 720     # Screen Size

# TILE ----->  the greater TILE the Smaller Maze Size 
TILE =150

#cols*rows = Num (Gride cells)
cols, rows = WIDTH // TILE, HEIGHT // TILE 


# intializing class attributes

pygame.init()
sc = pygame.display.set_mode(RES2)
clock = pygame.time.Clock()
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)
FONT = pygame.font.Font(None, 20)

# Definig  Cell class that is resposible for drawing Cell and its walls or colors 
class Cell:
    thickness = 2                   # -> walls Size
    counter = 0
    

    def __init__(self, x, y):
        self.x, self.y = x, y
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.visited = False
        self.id = Cell.counter
        Cell.counter += 1

    def __lt__(self, other): # a method to handel comparison for cell and PQueue elements "<" 
        return self.id < other.id
    





# Drawing cell and its boarders

    def draw(self):
        x, y = self.x * TILE, self.y * TILE
        if self.visited:
            pygame.draw.rect(sc, pygame.Color('black'), (x, y, TILE, TILE))

        if self.walls['top']:
            pygame.draw.line(sc, pygame.Color(255, 255, 255), (x, y), (x + TILE, y), self.thickness)
        if self.walls['right']:
            pygame.draw.line(sc, pygame.Color(255, 255, 255), (x + TILE, y), (x + TILE, y + TILE), self.thickness)
        if self.walls['bottom']:
            pygame.draw.line(sc, pygame.Color(255, 255, 255), (x, y + TILE), (x, y + TILE), self.thickness)
        if self.walls['left']:
            pygame.draw.line(sc, pygame.Color(255, 255, 255), (x, y + TILE), (x, y), self.thickness)




    def draw_current_cell(self):
        x, y = self.x * TILE, self.y * TILE
        pygame.draw.rect(sc, pygame.Color('saddlebrown'), (x + 2, y + 2, TILE - 2, TILE - 2))




# Getting  Walls or cells porders
    def get_rects(self):
        rects = []
        x, y = self.x * TILE, self.y * TILE
        if self.walls['top']:
            rects.append(pygame.Rect((x, y), (TILE, self.thickness)))
        if self.walls['right']:
            rects.append(pygame.Rect((x + TILE, y), (self.thickness, TILE)))
        if self.walls['bottom']:
            rects.append(pygame.Rect((x, y + TILE), (TILE, self.thickness)))
        if self.walls['left']:
            rects.append(pygame.Rect((x, y), (self.thickness, TILE)))
        return rects



# checking Cells size 

    def check_cell(self, x, y):
        find_index = lambda x, y: x + y * cols
        if x < 0 or x > cols - 1 or y < 0 or y > rows - 1:
            return False
        return grid_cells[find_index(x, y)]




    def check_neighbors(self):
        neighbors = []
        top = self.check_cell(self.x, self.y - 1)
        right = self.check_cell(self.x + 1, self.y)
        bottom = self.check_cell(self.x, self.y + 1)
        left = self.check_cell(self.x - 1, self.y)
        if top and not top.visited:
            neighbors.append(top)
        if right and not right.visited:
            neighbors.append(right)
        if bottom and not bottom.visited:
            neighbors.append(bottom)
        if left and not left.visited:
            neighbors.append(left)
        return choice(neighbors) if neighbors else False





# Drawing Buttons (A*,BFS,Exit)
def draw_button(text, x, y, width, height, active_color, inactive_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed(3)
    button_rect = pygame.Rect(x, y, width, height)

    if button_rect.collidepoint(mouse):
        pygame.draw.rect(sc, active_color, button_rect)
        if click[0] == 1 and action:
            action()
    else:
        pygame.draw.rect(sc, inactive_color, button_rect)

    text_surf = pygame.font.Font(None, 25).render(text, True, (128, 0, 128))
    text_rect = text_surf.get_rect(center=button_rect.center)
    sc.blit(text_surf, text_rect)





# remove walls  when creating the Maze

def remove_walls(current, next):
    dx = current.x - next.x
    if dx == 1:
        current.walls['left'] = False
        next.walls['right'] = False
    elif dx == -1:
        current.walls['right'] = False
        next.walls['left'] = False
    dy = current.y - next.y
    if dy == 1:
        current.walls['top'] = False
        next.walls['bottom'] = False
    elif dy == -1:
        current.walls['bottom'] = False
        next.walls['top'] = False





# Solving Maze by BFS Algorithm

def bfs(start, end):
    colorBFS_Range=130
    queue = deque([start])
    came_from = {start: None}
    while queue:
        current = queue.popleft()
        if current == end:
            break
        neighbors = []
        if not current.walls['top']:
            neighbors.append(current.check_cell(current.x, current.y - 1))
        if not current.walls['right']:
            neighbors.append(current.check_cell(current.x + 1, current.y))
        if not current.walls['bottom']:
            neighbors.append(current.check_cell(current.x, current.y + 1))
        if not current.walls['left']:
            neighbors.append(current.check_cell(current.x - 1, current.y))
        for neighbor in neighbors:
            if neighbor and neighbor not in came_from:
                queue.append(neighbor)#46, 134, 193
                pygame.draw.rect(sc, pygame.Color(46,134 , min(193,colorBFS_Range)), (neighbor.x * TILE + 5, neighbor.y * TILE + 5, TILE - 10, TILE - 10), border_radius=2)
                colorBFS_Range+=1
                pygame.display.flip()
                clock.tick(10)
                came_from[neighbor] = current
                
    return came_from





# initalizing A* Data Strcture and start and end nodes

grid_cells = [Cell(col, row) for row in range(rows) for col in range(cols)]
current_cell = grid_cells[0]
stack = []
colors, color = [], 20
def heuristic(a, b):
    return abs(a.x - b.x) + abs(a.y - b.y)





# Solving Maze by A* Algorithm

def a_star(start, end):
    open_set = PriorityQueue()
    open_set.put((0, start))
    came_from = {start: None}
    g_score = {cell: float('inf') for cell in grid_cells}
    g_score[start] = 0
    f_score = {cell: float('inf') for cell in grid_cells}
    f_score[start] = heuristic(start, end)

    colorAStar_Range = 130

    while not open_set.empty():
        current = open_set.get()[1]

        if current == end:
            break

        neighbors = []
        if not current.walls['top']:
            neighbors.append(current.check_cell(current.x, current.y - 1))
        if not current.walls['right']:
            neighbors.append(current.check_cell(current.x + 1, current.y))
        if not current.walls['bottom']:
            neighbors.append(current.check_cell(current.x, current.y + 1))
        if not current.walls['left']:
            neighbors.append(current.check_cell(current.x - 1, current.y))
        
        for neighbor in neighbors:
            if neighbor:
                tentative_g_score = g_score[current] + 1
                if tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, end)
                    open_set.put((f_score[neighbor], neighbor))
                    pygame.draw.rect(sc, pygame.Color(255,0 , min(255,colorAStar_Range)), (neighbor.x * TILE + 5, neighbor.y * TILE + 5, TILE - 10, TILE - 10), border_radius=2)
                    colorAStar_Range += 1
                    pygame.display.flip()
                    clock.tick(10)

    return came_from
running = True



#action of button Play_BFS
def play_BFS():
     #Solve the maze using BFS
     start_cell = grid_cells[0]
     end_cell = grid_cells[-1]
     bfs(start_cell, end_cell)
     pygame.display.flip()
     clock.tick(100)




#action of button Play_A_star
def play_A_star():
    start_cell = grid_cells[0]
    end_cell = grid_cells[-1]
    a_star(start_cell, end_cell)
    pygame.display.flip()
    clock.tick(10)
#action of button stop_action 
def stop_action():
    pygame.quit()

# drawing the gride with Gray color
 
sc.fill(pygame.Color(128,128, 128))










# Generating Maze By DFS Algorithm 

while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
    while True:
        
        #print("(", current_cell.x, ",", current_cell.y, ")")
        draw_button('BFS',  910, 10, 150, 50, GREEN, BLUE, play_BFS)
        draw_button('A*', 910, 70, 150, 50, GREEN, BLUE, play_A_star)
        draw_button('Exit', 910, 150, 150, 50, RED, GREEN,stop_action)

        pygame.display.update()

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        [cell.draw() for cell in grid_cells]
        
        current_cell.visited = True
        current_cell.draw_current_cell()
        [pygame.draw.rect(sc, colors[i], (cell.x * TILE + 5, cell.y * TILE + 5, TILE - 5, TILE - 5), border_radius=2) for i, cell in enumerate(stack)]

        next_cell = current_cell.check_neighbors()

        if next_cell:
            next_cell.visited = True
            stack.append(current_cell)
            colors.append((255, min(color, 87),51))
            color += 2
            remove_walls(current_cell, next_cell)
            current_cell = next_cell 
        elif stack:
            current_cell = stack.pop()

        pygame.display.flip() # Style of displaying
        clock.tick(10) # Speed of Drawing Cell and traversing the Maze
    
