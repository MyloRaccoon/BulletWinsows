import pygame
import os
import ctypes
import pygetwindow as gw
from enum import Enum
from packages.global_mod import Global
from random import randint

Side = Enum('Side', ['NORTH', 'SOUTH', 'EAST', 'WEST'])
global launching_bullet

def get_hwnd():
	pygame.display.init()
	hwnd = pygame.display.get_wm_info()["window"]
	return hwnd

class Bullet():

	def __init__(self, id_name : str, side_spawn : Side):
		pygame.init()
		self.id = id_name
		self.home_side = side_spawn
		match side_spawn:
			case Side.NORTH:
				self.x, self.y = randint(0, Global.screen_width - 100), -100
			case Side.SOUTH:
				self.x, self.y = randint(0, Global.screen_width - 100), Global.screen_height + 100
			case Side.EAST:
				self.x, self.y = -100, randint(0, Global.screen_height - 100)
			case Side.WEST:
				self.x, self.y = Global.screen_width + 100, randint(0, Global.screen_height - 100)
		self.pyScreen : pygame.Dispay
		self.hwnd : gw.Dispay
		self.speed = 1
		self.running = False

	def get_window(self):
		return gw.getWindowsWithTitle(self.id)[0]

	def process(self):
		match self.home_side:
			case Side.NORTH:
				self.y += self.speed
			case Side.SOUTH:
				self.y -= self.speed
			case Side.EAST:
				self.x += self.speed
			case Side.WEST:
				self.x -= self.speed
		ctypes.windll.user32.SetWindowPos(self.hwnd, None, self.x, self.y, 0, 0, 0x0001)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.kill()

		if self.check_exited():
			self.kill()

		pygame.display.flip()

	def check_exited(self):
		check = False
		if self.home_side == Side.NORTH and self.y >= 900:
			check = True
		elif self.home_side == Side.SOUTH and self.y <= -100:
			check = True
		elif self.home_side == Side.EAST and self.x >= 1600:
			check = True
		elif self.home_side == Side.WEST and self.x <= -100:
			check = True
		return check

	def run(self):
		self.running = True
		self.pyScreen = pygame.display.set_mode((100, 100), pygame.NOFRAME)
		pygame.display.set_caption("notactive yet...")
		self.pyScreen.fill((255,0,0))
		self.hwnd = get_hwnd()
		ctypes.windll.user32.SetWindowPos(self.hwnd, None, self.x, self.y, 0, 0, 0x0001)
		pygame.display.set_caption(self.id)

	def kill(self):
		self.running = False

def launch_bullet():
	bullet = Bullet("bulletID123456", [Side.EAST, Side.SOUTH, Side.WEST, Side.NORTH][randint(0, 3)])
	bullet.run()
	while bullet.running:
		bullet.process()
	pygame.quit()

def process_launch():
	while True:
		launch_bullet()

def stop_launching():
	launching_bullet = False

if __name__ == '__main__':
	process_launch()