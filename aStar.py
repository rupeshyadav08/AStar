import pygame
import math
from queue import PriorityQueue

WIDTH =900
WIN = pygame.display.set_mode((WIDTH,WIDTH))
pygame.display.set_caption("A* Path finder BY Rupesh Yadav")


YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


class Node:
    def __init__(self,row,col,width,total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = YELLOW
        self.neighbors=[]
        self.width=width
        self.total_rows=total_rows
    def  get_pos(self):
        return self.row, self.col
    
    def is_closed(self):
        return self.color == RED
    
    def is_open(self):
        return self.color == GREEN
    
    def is_barrier(self):
        return self.color == BLACK
    
    def is_start(self):
        return self.color == BLUE
    
    def is_end(self):
        return self.color == GREY
    
    def reset(self):
        self.color = YELLOW
        
    def make_start(self):
        self.color = BLUE
    
    def make_closed(self):
        self.color = RED
    
    def make_open(self):
        self.color = GREEN
    
    def make_barrier(self):
        self.color = BLACK
    
    def make_end(self):
        self.color = GREY
    
    def make_path(self):
        self.color = WHITE
    
    def draw(self, win):
    	    pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))
    
    
    def update_neighbors(self,grid):
        """ Updating the neighbour and checking if the row number is 
        not more than total row and if the path is not blocked by the
        barrier using back tracking """
        
        self.neighbors=[]
        if self.row < self.total_rows-1 and not grid[self.row + 1][self.col].is_barrier():
            """ we have done +1 here to check the next down cube """
            self.neighbors.append(grid[self.row+1][self.col])
            
        if self.row > 0 and not grid[self.row -1][self.col].is_barrier():
            """ we have done +1 here to check the next up cube """
            self.neighbors.append(grid[self.row-1][self.col])
            
        if self.col < self.total_rows-1 and not grid[self.row ][self.col+1].is_barrier():
            """ we have done +1 here to check the next right cube """
            self.neighbors.append(grid[self.row][self.col+1])
            
        if self.col > 0 and not grid[self.row ][self.col-1].is_barrier():
            """ we have done +1 here to check the next left cube """
            self.neighbors.append(grid[self.row][self.col-1])
            
    
  
    def __lt__(self,other): #comparing two spots
        return False
    

def Hurustic(p1, p2): #Hurustic function to figure distance between point 1 and point 2
	x1, y1 = p1 #manhatan distance
	x2, y2 = p2
	return abs(x1 - x2) + abs(y1 - y2)

def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
	current.make_path()
        draw()

def algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = Hurustic(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
	    for event in pygame.event.get():
		    if event.type == pygame.QUIT:
			    pygame.quit()

	    current = open_set.get()[2]
	    open_set_hash.remove(current)

	    if current == end:
		    reconstruct_path(came_from, end, draw)
		    end.make_end()
		    return True

	    for neighbor in current.neighbors:
		    temp_g_score = g_score[current] + 1

		    if temp_g_score < g_score[neighbor]:
			    came_from[neighbor] = current
			    g_score[neighbor] = temp_g_score
			    f_score[neighbor] = temp_g_score + Hurustic(neighbor.get_pos(), end.get_pos())
			    if neighbor not in open_set_hash:
				    count += 1
				    open_set.put((f_score[neighbor], count, neighbor))
				    open_set_hash.add(neighbor)
				    neighbor.make_open()

	    draw()

	    if current != start:
		    current.make_closed()

    return False

    


def make_grid(rows,width):
    grid=[]
    gap=width//rows # the help us to find the gap between the each of row(cube width)
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node=Node(i,j,gap,rows)
            grid[i].append(node)
            
    return grid

def draw_grid(win,rows,width):
    gap=width//rows
    for i in range(rows):
        pygame.draw.line(win,PURPLE,(0, i * gap), (width, i * gap)) # drawing horizontal lines
        for j in range(rows):
            pygame.draw.line(win, PURPLE, (j * gap, 0), (j * gap, width))# Drawing verticle lines



def draw(win,grid,rows,width):
    win.fill(YELLOW,)   #fill the entire screen with one colore will do this at beginning of each frame 
    for row in grid:
        for node in row:
            node.draw(win) # draw grid with what color the node is
    draw_grid(win,rows,width)
    pygame.display.update() # update the drawn screen on display
    
    
    
def get_clicked_pos(pos,rows,width): # take mouse position and tells us at what cube we are
    gap = width // rows
    i,j = pos    
    row = i//gap
    col = j//gap
    return row, col

def main(win,width):
    rows=50
    start = None
    end = None
    
    run=True
    started=False
    
    grid=make_grid(rows,width)
    
    while run==True:
        draw(win,grid,rows,width)
        for event in pygame.event.get(): #check for every event happend like click of mouse button and space
            if event.type == pygame.QUIT:
                run=False
            
            if started==True:   #Once the event is started u can only quit and 
                                   #do not do anything else"""
                continue
            
            if pygame.mouse.get_pressed()[0]: # if we pressed the left mouse button
                pos=pygame.mouse.get_pos()
                row,col = get_clicked_pos(pos,rows,width)
                node=grid[row][col]
                if not start and node != end:
                    start=node
                    start.make_start()
                elif not end and end!=start:
                    end=node
                    end.make_end()
                
                elif node != end and node != start:
                    node.make_barrier()
                     
                
            elif pygame.mouse.get_pressed()[2]: #if we pressed the right mouse button
                pos=pygame.mouse.get_pos()
                row,col =get_clicked_pos(pos,rows,width)
                node=grid[row][col]
                node.reset()
                if node==start:
                    start=None
                if node==end:
                    end=None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not started:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    algorithm(lambda:draw(win,grid,rows,width),grid,start,end)
        
    pygame.quit()
    

main(WIN,WIDTH)
    
    
        
  
  
    
        
    

