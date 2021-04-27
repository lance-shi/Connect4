import pygame
import numpy as np
import random

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
		self.screen = pygame.display.set_mode((self.tile_size * self.width + 200, self.tile_size * (self.height+ 1)))
		pygame.display.set_caption("Connect 4")
		pygame.mixer.init(44100, -16, 1, 512)
		pygame.font.init()
		self.font = pygame.font.SysFont("monospace", 75)
		self.menu_font = pygame.font.SysFont("arial", 35)
		self.tiles = np.zeros((self.height, self.width))
		self.sound_move = pygame.mixer.Sound("sound/move.wav")
		self.winning_wording = "You win"
		self.player_turn = True
		self.trace = []
		self.undo_text = self.menu_font.render("Undo", False, self.colors["GREEN"])
		self.undo_rect = self.undo_text.get_rect(topleft=(750, 130))
		self.restart_text = self.menu_font.render("Restart", False, self.colors["GREEN"])
		self.restart_rect = self.restart_text.get_rect(topleft=(750, 230))

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
					if self.undo_rect.collidepoint(event.pos):
						self.undo()
					if self.restart_rect.collidepoint(event.pos):
						self.restart()
					if self.player_turn and not self.game_over:
						self.get_down(event)

			self.draw_board()
			self.draw_menu()
			self.draw_winning()
			pygame.display.update()

		pygame.quit()

	def undo(self):
		if len(self.trace) == 0:
			return
		latest = self.trace.pop()
		self.tiles[latest[0]][latest[1]] = 0
		if not self.game_over:
			self.current_color = -self.current_color
		self.game_over = False
		

	def restart(self):
		self.game_over = False
		self.tiles = np.zeros((self.height, self.width))
		self.current_color = 1
		self.trace = []

	def draw_board(self):
		self.screen.fill(self.colors["BLACK"])
		pygame.draw.rect(self.screen, self.colors["BLUE"], (0, self.tile_size, self.width * self.tile_size, self.height * self.tile_size))
		for i in range(self.height):
			for j in range(self.width):
				color = self.colors["BLACK"]
				if self.tiles[i][j] == 1:
					color = self.colors["YELLOW"]
				elif self.tiles[i][j] == -1:
					color = self.colors["RED"]
				pygame.draw.circle(self.screen, color, (int(j*self.tile_size+self.tile_size/2), 
					int((i+1)*self.tile_size+self.tile_size/2)), self.radius)

	def draw_menu(self):
		self.screen.blit(self.undo_text, self.undo_rect)
		self.screen.blit(self.restart_text, self.restart_rect)

	def get_down(self, event):
		x = event.dict['pos'][0]
		column = x // self.tile_size
		if column >= self.width:
			return
		line = self.get_available_slot(self.tiles, column)

		if line >= 0:
			self.drop_piece(self.tiles, line, column, self.current_color)
			self.trace.append([line, column, self.current_color])
			if self.judge_winning(self.current_color, line, column):
				self.game_over = True
				self.winning_wording = "You win!"
			else:
				self.current_color = -self.current_color
				self.sound_move.play()
				self.player_turn = False
				self.ai_play()

	def drop_piece(self, cur_board, line, column, color):
		cur_board[line][column] = color

	def get_available_slot(self, cur_board, column):
		line = self.height - 1
		while line >= 0:
			if cur_board[line][column] == 0:
				return line
			line -= 1
		return line

	def get_valid_spots(self, cur_board):
		valid_spots = []
		for col in range(self.width):
			line = self.get_available_slot(cur_board, col)
			if line >= 0:
				valid_spots.append((line, col))

		return valid_spots

	def ai_play(self):
		valid_spots = self.get_valid_spots(self.tiles)
		line, col = random.choice(valid_spots)
		self.ai_drop(line, col)

	def ai_drop(self, line, column):
		self.drop_piece(self.tiles, line, column, self.current_color)
		self.trace.append([line, column, self.current_color])
		if self.judge_winning(self.current_color, line, column):
			self.game_over = True
			self.winning_wording = "Computer wins"
		else:
			self.current_color = -self.current_color
			self.player_turn = True
			self.sound_move.play()

	def draw_winning(self):
		if self.game_over:
			self.screen.blit(self.font.render(self.winning_wording, False, self.colors["GREEN"]), [0, 0])

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