##
## pysnake.py
##

## Setting Window Position

# Available in Windows 8.1

window_pos_x = 100
window_pos_y = 50
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (window_pos_x, window_pos_y)

import sys
import random
import pygame

wind_width = 800
wind_height = 600
grid_size = 20

x_num = wind_width / grid_size
y_num = wind_height / grid_size

bg_color = (255,255,255)
grid_color = (0,0,0)
head_color = (0,255,255)
body_color = (255,0,255)
food_color = (255,255,0)

SHEAD = 0
SBODY = 1

RIGHT = [1, 0]
LEFT = [-1, 0]
UP = [0, -1]
DOWN = [0, 1]

NON_AVAILABLE_DIRECTION = [0, 0]

MAX_LIFE = 3

def checkMoveAvailable(dir1, dir2):
	available = []
	for i,j in zip(dir1, dir2):
		summ = i + j
		available.append(summ)
	return available != NON_AVAILABLE_DIRECTION

class SnakeGrid():
	
	def __init__(self, screen, sgtype):
		self.sgtype = sgtype
		self.screen = screen
					
	def set_pos(self, x, y):
		self.x = x
		self.y = y
		self.rect = pygame.Rect(0, 0, grid_size, 
			grid_size)
		self.rect.left = self.x * grid_size
		self.rect.top = self.y * grid_size
				
	def draw_grid(self):
		if self.sgtype == SHEAD:
			pygame.draw.rect(self.screen, head_color, self.rect)
		elif self.sgtype == SBODY:
			pygame.draw.rect(self.screen, body_color, self.rect)

class Snake():
	
	def __init__(self, screen, snake_grids, direction):
		self.screen = screen
		self.snake_grids = snake_grids
		self.direction = direction
		
	def snake_turn(self, food_grids, direction):
		if checkMoveAvailable(self.direction , direction):
			self.direction = direction	
			
	def snake_move(self, food_grids, direction):
		if checkMoveAvailable(self.direction , direction):
			self.direction = direction
			new_head = SnakeGrid(self.screen, SHEAD)
			# I used "new_head = self.snake_grids[0]" to initialize at first, but bug occured.
			# That appears a "reference" which changed the value of self.snake_grids[0] in the following line.
			new_head.set_pos(self.snake_grids[0].x + self.direction[0], self.snake_grids[0].y + self.direction[1])
						
			self.snake_head_insert(new_head)
			food_occupied_grids = get_occupied_grids(food_grids)
			
			if [self.snake_grids[0].x, self.snake_grids[0].y] in food_occupied_grids:
				for _grid in food_grids:
					if [_grid.x, _grid.y] == [self.snake_grids[0].x, self.snake_grids[0].y]:
						food_grids.remove(_grid)								
			else:	
				self.snake_tail_delete()	
	
	def snake_head_insert(self, new_head):
		if new_head.x == self.snake_grids[0].x + self.direction[0] and \
			new_head.y == self.snake_grids[0].y + self.direction[1]:
				new_head.sgtype = SHEAD
				self.snake_grids.insert(0, new_head)
				self.snake_grids[1].sgtype = SBODY
	
	def snake_tail_delete(self):
		self.snake_grids.pop()
		
	def check_snake_hit(self):
		[x, y] = [self.snake_grids[0].x, self.snake_grids[0].y]
		
		HIT_WALL = x >= x_num - 1 or x < 1 or y >= y_num - 1 or y < 1 
		HIT_SELF = [x, y] in get_occupied_grids(self.snake_grids[1:])
		
		return HIT_WALL or HIT_SELF
		
	def draw_snake(self):
		for snake_grid in self.snake_grids:
			snake_grid.draw_grid()	

class FoodGrid():
	
	def __init__(self, snake_grids, screen):
		self.screen = screen
		self.snake_grids = snake_grids
		
	def set_pos(self, x, y):
		if [x, y] not in get_occupied_grids(self.snake_grids):
			self.x = x
			self.y = y
			self.rect = pygame.Rect(0, 0, grid_size, 
				grid_size)
			self.rect.left = self.x * grid_size
			self.rect.top = self.y * grid_size
			
	def set_random_pos(self):
		while True:
			x = random.randint(1, x_num - 2)
			y = random.randint(1, y_num - 2)
			if [x, y] not in get_occupied_grids(self.snake_grids):
				break
		self.set_pos(x, y)
	
	def draw_grid(self):
		pygame.draw.rect(self.screen, food_color, self.rect)

def get_occupied_grids(grids):
	
	occupied_grids = []
	for _grid in grids:
		occupied_grids.append([_grid.x, _grid.y])
	return occupied_grids

def update_screen(screen, snake, food_grids):
	
	screen.fill(bg_color)
	
	for i in range(grid_size, wind_width, grid_size):
		pygame.draw.line(screen, grid_color, (i,0), (i,wind_height), 1)
	for j in range(grid_size, wind_height, grid_size):
		pygame.draw.line(screen, grid_color, (0,j), (wind_width,j), 1)
	
	edge_rects = []
	edge_rects.append(pygame.Rect(0, 0, wind_width, grid_size))#up
	edge_rects.append(pygame.Rect(0, 0, grid_size, wind_height))#left
	edge_rects.append(pygame.Rect(0, wind_height - grid_size, wind_width, grid_size))#down
	edge_rects.append(pygame.Rect(wind_width - grid_size, 0, grid_size, wind_height))#right
	
	for edge_rect in edge_rects:		
		pygame.draw.rect(screen, grid_color, edge_rect)
	
	for _grid in food_grids:
		_grid.draw_grid()
					
	snake.draw_snake()
					
	pygame.display.flip()
	
def refill_food(snake_grids, food_grids, screen):
	for i in range(40):
		food_grid = FoodGrid(snake_grids, screen)
		food_grid.set_random_pos()
		food_grids.append(food_grid)

def snake_grids_init(screen):
	snake_head = SnakeGrid(screen, SHEAD)
	snake_head.set_pos(int(x_num / 2), int(y_num / 2))
	
	snake_grids = [snake_head]		
	for i in range(1,6):
		new_grid = SnakeGrid(screen, SBODY)
		new_grid.set_pos(int(x_num / 2) - i, int(y_num / 2))
		snake_grids.append(new_grid)
	return snake_grids

def food_init(snake_grids, screen):
	food_grids = []
	refill_food(snake_grids, food_grids, screen)
	return food_grids
		
def run_game():
	
	pygame.init()

	pygame.display.set_caption("pysnake")
	screen = pygame.display.set_mode((wind_width, wind_height))
	
	## ---------Test-----------	
	
	snake_grids = snake_grids_init(screen)
	food_grids = food_init(snake_grids, screen)
	
	snake = Snake(screen, snake_grids, RIGHT)	
	#snake.snake_move(food_grids, RIGHT)
	
	life = MAX_LIFE		
	
	FPS = pygame.time.Clock()
	
	direction = RIGHT
	## -------------------------
	
	while True:
		
		FPS.tick(5)
		
		update_screen(screen, snake, food_grids)
				
		if len(food_grids) == 0:
			refill_food(snake_grids, food_grids, screen)
		
		if snake.check_snake_hit():
			snake_grids = snake_grids_init(screen)
			snake = Snake(screen, snake_grids, RIGHT)
			update_screen(screen, snake, food_grids)
			direction = RIGHT
					
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RIGHT:
					if checkMoveAvailable(direction, RIGHT):
						direction = RIGHT
						snake.snake_turn(food_grids, RIGHT)
				elif event.key == pygame.K_LEFT:
					if checkMoveAvailable(direction, LEFT):
						direction = LEFT
						snake.snake_turn(food_grids, LEFT)
				elif event.key == pygame.K_UP:
					if checkMoveAvailable(direction, UP):
						direction = UP
						snake.snake_turn(food_grids, UP)
				elif event.key == pygame.K_DOWN:
					if checkMoveAvailable(direction, DOWN):
						direction = DOWN
						snake.snake_turn(food_grids, DOWN)
				elif event.key == pygame.K_q:
					sys.exit()
					
		snake.snake_move(food_grids, direction)

	
run_game()

