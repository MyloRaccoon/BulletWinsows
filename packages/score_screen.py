import pygame

def get_hwnd():
	pygame.display.init()
	hwnd = pygame.display.get_wm_info()["window"]
	return hwnd

class Score_screen:

	def __init__(self, name, score):
		pygame.init()
		self.name = name
		self.score = score
		self.running = True
		self.pyScreen = pygame.display.set_mode((1000, 300), pygame.NOFRAME)
		pygame.display.set_caption(self.name)
		self.hwnd = get_hwnd()
		self.font = pygame.font.Font(None, 100)
		self.font2 = pygame.font.Font(None, 50)
		self.pyScreen.fill((255,255,255))
		self.pyScreen.blit(self.font.render(f'Congrats {self.name} !', True, (0,0,0)), (0,0))
		self.pyScreen.blit(self.font.render(f'Your score : {self.score} !', True, (0,0,0)), (0,100))
		self.pyScreen.blit(self.font2.render(f'Any key to quit', True, (0,0,0)), (0,200))

	def process(self):
		pygame.display.flip()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.kill()
			if event.type == pygame.KEYDOWN:
				self.kill()

	def kill(self):
		self.running = False

def process_score_screen(nom, score):
	score_screen = Score_screen(nom, score)
	while score_screen.running:
		score_screen.process()
	pygame.quit()

if __name__ == '__main__':
	process_score_screen("n", 0)