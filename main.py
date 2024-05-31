import pygame
import random
from queue import PriorityQueue

WIDTH, HEIGHT = 800, 600 
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

SPEED = 10 #Default: 10

GREEN = [150, 204, 96]
DARK_GREEN = [135, 183, 87]
BACKGROUND_COLORS = {True: GREEN, False: DARK_GREEN}

BLUE = [14, 146, 207]
RED = [214, 41, 41]

class Grid:
	def __init__(self, cell_size):
		self.cell_size = cell_size
		self.grid_rows = HEIGHT // self.cell_size
		self.grid_columns = WIDTH // self.cell_size 
		self.grid = [[0 for col in range(self.grid_columns)] for row in range(self.grid_rows)]
		self.apple_pos = [0, 0]

	def spawn_apple(self):
		open_spaces = []
		for row in range(len(self.grid)):
			for col in range(len(self.grid[0])):
				if self.grid[row][col] == 0:
					open_spaces.append([row, col])

		if len(open_spaces) > 0:
			self.apple_pos = random.choice(open_spaces)
			self.grid[self.apple_pos[0]][self.apple_pos[1]] = 2

	def get_apple_pos(self):
		return self.apple_pos

	def get_grid(self):
		return self.grid		

	def draw(self, win):
		color = True
		for row in range(len(self.grid)):
			for col in range(len(self.grid[0])):
				start_col = col * self.cell_size
				start_row = row * self.cell_size

				if self.grid[row][col] == 0:
					pygame.draw.rect(win, BACKGROUND_COLORS[color], (start_col, start_row, self.cell_size, self.cell_size))
				elif self.grid[row][col] == 1:
					pygame.draw.rect(win, BACKGROUND_COLORS[True], (start_col, start_row, self.cell_size, self.cell_size))
					pygame.draw.rect(win, BLUE, (start_col, start_row, self.cell_size, self.cell_size), border_radius=self.cell_size // 4)
				elif self.grid[row][col] == 2:
					pygame.draw.rect(win, BACKGROUND_COLORS[color], (start_col, start_row, self.cell_size, self.cell_size))
					pygame.draw.rect(win, RED, (start_col, start_row, self.cell_size, self.cell_size), border_radius=self.cell_size)

				color = not color
			color = not color

class Snake:
	def __init__(self, start_pos):
		self.snake = start_pos
		self.length = 1
		self.directions = {"up": [-1, 0],
							"down": [1, 0], 
							"left": [0, -1],
							"right": [0, 1]}

	def move(self, grid, direction):
		new_row = self.directions[direction][0]
		new_col = self.directions[direction][1]

		head_pos = self.snake[0]

		if check_new_pos(grid.get_grid(), self.snake[0], [new_row, new_col]):
			row_pos = self.snake[0][0] + new_row
			col_pos = self.snake[0][1] + new_col
			if grid.get_grid()[row_pos][col_pos] == 1:
				return True
			elif grid.get_grid()[row_pos][col_pos] == 2:
				body_1 = self.snake[len(self.snake) - 1]
				body_2 = self.snake[len(self.snake) - 2]
				row = body_1[0] + body_1[0] - body_2[0]
				col = body_1[1] + body_1[1] - body_2[1]
				self.snake.append([row, col])
				self.length += 1
				grid.spawn_apple()
			self.snake[0] = [row_pos, col_pos]
		else:
			return True

		for i in range(1, len(self.snake)):
			temp = self.snake[i]
			self.snake[i] = head_pos
			head_pos = temp

		return False
		
	def draw(self, grid):
		for row in range(len(grid.get_grid())):
			for col in range(len(grid.get_grid()[0])):
				if grid.get_grid()[row][col] == 1:
					grid.get_grid()[row][col] = 0

		for i in self.snake: 
			grid.get_grid()[i[0]][i[1]] = 1

def check_new_pos(grid, curr_pos, new_pos):
	row_pos = curr_pos[0] + new_pos[0]
	col_pos = curr_pos[1] + new_pos[1]

	if row_pos >= 0 and row_pos < len(grid) and col_pos >= 0 and col_pos < len(grid[0]):
		return True
	else: 
		return False	

def get_neighbors(grid, node):
	neighbors = []

	node_row = node[0]
	node_col = node[1]

	rows = [1, -1, 0, 0]
	cols = [0, 0, -1, 1]

	for i in range(len(rows)):
		new_row = rows[i] + node_row
		new_col = cols[i] + node_col
		if check_new_pos(grid, node, [rows[i], cols[i]]):
			if grid[new_row][new_col] != 1:
				neighbors.append([new_row, new_col])

	return neighbors

def manhattan_dist(node_1, node_2):
	return abs(node_1[0] - node_2[0]) + abs(node_1[1] - node_2[1])

def find(node, lst):
	for i in range(len(lst)):
		row = lst[i][0]
		col = lst[i][1]
		if node[0] == row and node[1] == col:
			return i

def generate_path(came_from, current):
	path = []
	run = True
	while True:
		temp = current
		for i in range(len(came_from)):
			row = came_from[i][0][0]
			col = came_from[i][0][1]
			if current[0] == row and current[1] == col:
				path.append(current)
				current = came_from[i][1]

		if current == temp:
			run = False 
			break

	return path

def algorithm(grid, start, end):
	open_set = PriorityQueue()
	open_set.put((0, start))
	came_from = []
	g_score = []
	f_score = []
	for row in range(len(grid)):
		for col in range(len(grid[0])):
			g_score.append([row, col, float("inf")])
			f_score.append([row, col, float("inf")])
	g_score[find(start, g_score)][2] = 0
	f_score[find(start, f_score)][2] = manhattan_dist(start, end)
	open_set_hash = [start]

	while not open_set.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = open_set.get()[1]
		open_set_hash.remove(current)

		if current[0] == end[0] and current[1] == end[1]:
			return generate_path(came_from, end)

		neighbors = get_neighbors(grid, current)
		for neighbor in neighbors:
			temp_g_score = g_score[find(current, g_score)][2] + 1

			if temp_g_score < g_score[find(neighbor, g_score)][2]:
				came_from.append([neighbor, current])
				g_score[find(neighbor, g_score)][2] = temp_g_score 
				f_score[find(neighbor, f_score)][2] = temp_g_score + manhattan_dist(neighbor, end)
				if neighbor not in open_set_hash: 
					open_set.put((f_score[find(neighbor, f_score)][2], neighbor))
					open_set_hash.append(neighbor)

	return False

def find_direction(curr_pos, new_pos):
	row = new_pos[0] - curr_pos[0]
	col = new_pos[1] - curr_pos[1]

	if row == 1:
		return "down"
	if row == -1:
		return "up"
	if col == 1:
		return "right"
	if col == -1:
		return "left"

def update(win, grid, snake):
	snake.draw(grid)
	grid.draw(win)
	pygame.display.update()

def main():
	clock = pygame.time.Clock()

	grid = Grid(40)
	grid.spawn_apple()

	center  = [len(grid.get_grid()) // 2, len(grid.get_grid()[0]) // 2]
	snake = Snake([center])

	direction = None 
	game_over = False

	AI = False 
	
	run = True
	while run:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False 
				break 

			if event.type == pygame.KEYDOWN: 
				if event.key == pygame.K_UP:
					if direction != "up" and direction != "down":
						direction = "up"
				if event.key == pygame.K_DOWN:
					if direction != "down" and direction != "up":
						direction = "down"
				if event.key == pygame.K_LEFT:
					if direction != "left" and direction != "right":
						direction = "left"
				if event.key == pygame.K_RIGHT:
					if direction != "right" and direction != "left":
						direction = "right"

				if event.key == pygame.K_SPACE:
					AI = True

		if AI:
			path = algorithm(grid.get_grid(), snake.snake[0], grid.get_apple_pos())

			if path:
				direction = find_direction(snake.snake[0], path[-1])

		if direction != None: 
			if snake.move(grid, direction):
				game_over = True

		if game_over:
			print ("Score: " + str(snake.length))
			run = False
			break

		update(WINDOW, grid, snake)

		clock.tick(SPEED)

	pygame.quit()

if __name__ == "__main__":
	main()