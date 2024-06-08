import pygame
import os
import ctypes
import pygetwindow as gw
from packages.global_mod import Global

def get_hwnd():
	pygame.display.init()
	hwnd = pygame.display.get_wm_info()["window"]
	return hwnd

class Player():

	def __init__(self):
		self.name = "player"
		pygame.init()
		self.x, self.y = Global.screen_width // 2, Global.screen_height // 2 
		self.speed = 1
		self.inputs = {pygame.K_LEFT : False, pygame.K_RIGHT : False, pygame.K_UP : False, pygame.K_DOWN : False}
		self.running = False

	def get_window(self):
		return gw.getWindowsWithTitle(self.name)[0]

	def process(self):
		if self.inputs[pygame.K_LEFT]:
			self.x -= self.speed
		if self.inputs[pygame.K_RIGHT]:
			self.x += self.speed
		if self.inputs[pygame.K_UP]:
			self.y -= self.speed
		if self.inputs[pygame.K_DOWN]:
			self.y += self.speed

		ctypes.windll.user32.SetWindowPos(self.hwnd, None, self.x, self.y, 0, 0, 0x0001)

		if self.is_colliding_bullet():
			self.kill()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.kill()
			if event.type == pygame.KEYDOWN:
				self.inputs[event.key] = True
			if event.type == pygame.KEYUP:
				self.inputs[event.key] = False
		pygame.display.flip()

	def is_colliding_window(self, target_win):
		try:	
			self_win = self.get_window()
			rect1 = (self_win.left, self_win.top, self_win.width, self_win.height)
			rect2 = (target_win.left, target_win.top, target_win.width, target_win.height)

			overlap = not (rect1[0] + rect1[2] <= rect2[0] or rect1[0] >= rect2[0] + rect2[2] or rect1[1] + rect1[3] <= rect2[1] or rect1[1] >= rect2[1] + rect2[3])
		except Exception as e:
			overlap = False
		return overlap

	def is_colliding_bullet(self):
		boolean = False
		try:	
			wins = gw.getWindowsWithTitle("bulletID123456")
			i = 0
			while i < len(wins) and not boolean:
				if self.is_colliding_window(wins[i]):
					boolean = True
				i+=1
		except Exception as e:
			boolean = False
		return boolean
			

	def run(self):
		self.running = True
		self.pyScreen = pygame.display.set_mode((100, 100), pygame.NOFRAME)
		pygame.display.set_caption(self.name)
		self.pyScreen.fill((0,0,255))
		self.hwnd = get_hwnd()

	def kill(self):
		self.running = False

def run_player(player):
	player.run()
	while player.running:
		player.process()
	pygame.quit()

if __name__ == '__main__':
	player = Player()
	run_player(player)