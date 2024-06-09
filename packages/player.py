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
		self.name = "playerID#123456"
		pygame.init()
		self.x, self.y = Global.screen_width // 2 - Global.player_size // 2, Global.screen_height // 2 - Global.player_size // 2
		self.speed = Global.player_speed
		self.inputs = {pygame.K_LEFT : False, pygame.K_RIGHT : False, pygame.K_UP : False, pygame.K_DOWN : False}
		self.running = False

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

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.kill()
			if event.type == pygame.KEYDOWN:
				self.inputs[event.key] = True
			if event.type == pygame.KEYUP:
				self.inputs[event.key] = False
		pygame.display.flip()			

	def run(self):
		self.running = True
		self.pyScreen = pygame.display.set_mode((Global.player_size, Global.player_size), pygame.NOFRAME)
		pygame.display.set_caption(self.name)
		self.pyScreen.fill(Global.player_color)
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