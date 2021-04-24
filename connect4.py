import pygame
import numpy as np

class Board:
	def __init__(self):
		self.colors = {
			"BLACK": (0, 0, 0),
			"RED": (255, 0, 0),
			"YELLOW": (255, 255, 0),
			"BLUE": (0, 0, 255),
			"WHITE": (0, 0, 0),
			"GREEN": (0, 255, 0)
		}
		self.tile_size = 100
		self.radius = int(self.tile_size/2 - 5)
		self.width, self.height = 7, 6
		self.current_color = 1 #yellow, -1 means red
		self.game_over = False
		self.screen = pygame.display.set_mode((self.tile_size * self.width, self.tile_size * (self.height+ 1)))
		pygame.display.set_caption("Connect 4")
		pygame.mixer.init(44100, -16, 1, 512)
		pygame.font.init()
		self.font = pygame.font.SysFont("monospace", 75)
		self.tiles = np.zeros((self.height, self.width))
		self.sound_move = pygame.mixer.Sound("sound/move.wav")
		self.winning_color = "Yellow"

		self.main_loop()

	def main_loop(self):
		clock = pygame.time.Clock()
		run = True
		while run:
			clock.tick(60)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					run = False
				if event.type == pygame.MOUSEBUTTONUP:
					'''
					if self.regretRect.collidepoint(event.pos):
						self.regret()
					'''
					if not self.game_over:
						self.get_down(event)

			self.draw_board()
			self.draw_winning()
			pygame.display.update()

		pygame.quit()

	def draw_board(self):
		self.screen.fill(self.colors["BLUE"])
		pygame.draw.rect(self.screen, self.colors["BLACK"], (0, 0, self.width * self.tile_size, self.tile_size))
		for i in range(self.height):
			for j in range(self.width):
				color = self.colors["BLACK"]
				if self.tiles[i][j] == 1:
					color = self.colors["YELLOW"]
				elif self.tiles[i][j] == -1:
					color = self.colors["RED"]
				pygame.draw.circle(self.screen, color, (int(j*self.tile_size+self.tile_size/2), 
					int((i+1)*self.tile_size+self.tile_size/2)), self.radius)

	def get_down(self, event):
		x = event.dict['pos'][0]
		column = x // self.tile_size
		if column >= self.width:
			return
		line = self.height - 1
		while line >= 0:
			if self.tiles[line][column] == 0:
				self.tiles[line][column] = self.current_color
				break
			line -= 1

		if line >= 0:
			if self.judge_winning(self.current_color, line, column):
				self.game_over = True
				if self.current_color == 1:
					self.winning_color = "Yellow"
				else:
					self.winning_color = "Red"
			else:
				self.current_color = -self.current_color
				self.sound_move.play()

	def draw_winning(self):
		if self.game_over:
			self.screen.blit(self.font.render(self.winning_color + " wins", False, self.colors["GREEN"]), [0, 0])

	def judge_winning(self, color, x, y):
		verticalCount = 0
		for i in range(x-1, -1, -1):
			if self.tiles[i][y] == color:
				verticalCount += 1
				if verticalCount >= 3:
					return True
			else:
				break
		for i in range(x+1, self.height):
			if self.tiles[i][y] == color:
				verticalCount += 1
				if verticalCount >= 3:
					return True
			else:
				break

		horizontalCount = 0
		for i in range(y-1, -1, -1):
			if self.tiles[x][i] == color:
				horizontalCount += 1
				if horizontalCount >= 3:
					return True
			else:
				break
		for i in range(y+1, self.width):
			if self.tiles[x][i] == color:
				horizontalCount += 1
				if horizontalCount >= 3:
					return True
			else:
				break

		diagonalCount1 = 0
		for i in range(1, 4):
			if x - i >= 0 and y - i >=0 and self.tiles[x-i][y-i] == color:
				diagonalCount1 += 1
				if diagonalCount1 >= 3:
					return True
			else:
				break
		for i in range(1, 4):
			if x + i < self.height and y + i < self.width and self.tiles[x+i][y+i] == color:
				diagonalCount1 += 1
				if diagonalCount1 >= 3:
					return True
			else:
				break

		diagonalCount2 = 0
		for i in range(1, 4):
			if x - i >= 0 and y + i < self.width and self.tiles[x-i][y+i] == color:
				diagonalCount2 += 1
				if diagonalCount2 >= 3:
					return True
			else:
				break
		for i in range(1, 4):
			if x + i < self.height and y - i >= 0 and self.tiles[x+i][y-i] == color:
				diagonalCount2 += 1
				if diagonalCount2 >= 3:
					return True
			else:
				break

		return False

def main():
	game = Board()

if __name__ == "__main__":
	main()