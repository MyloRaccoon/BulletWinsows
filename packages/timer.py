import pygame
import os
import ctypes
import pygetwindow as gw
import time

def get_hwnd():
	pygame.display.init()
	hwnd = pygame.display.get_wm_info()["window"]
	return hwnd

class Timer():

	def __init__(self, shared_data):
		pygame.init()
		self.name = "timer"
		self.shared_data = shared_data
		self.shared_data["time"] = 0
		
		self.x, self.y = 0, 0
		self.running = False

	def get_window(self):
		return gw.getWindowsWithTitle(self.name)[0]

	def process(self, font):
		self.pyScreen = pygame.display.set_mode((55 * len(str(self.shared_data["time"])) + 5, 90), pygame.NOFRAME)
		self.pyScreen.fill((255, 255, 255))
		self.pyScreen.blit(font.render(str(self.shared_data["time"]), True, (0,0,0)), (0,0))
		pygame.display.flip()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.kill()
		time.sleep(1)
		self.shared_data["time"] += 1

	def run(self):
		self.running = True
		self.pyScreen = pygame.display.set_mode((self.shared_data["time"], 90), pygame.NOFRAME)
		pygame.display.set_caption(self.name)
		self.hwnd = get_hwnd()
		ctypes.windll.user32.SetWindowPos(self.hwnd, None, self.x, self.y, 0, 0, 0x0001)

	def kill(self):
		self.running = False

def timer_process(timer):
	pygame.init()
	timer.run()
	while timer.running:
		timer.process(pygame.font.Font(None, 150))
	pygame.quit()

if __name__ == '__main__':
	timer = Timer()
	timer_process(timer)