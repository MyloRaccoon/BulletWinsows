import multiprocessing
import time
from packages.player import run_player, Player
from packages.bullet import process_launch, stop_launching, launch_bullet
from packages.timer import timer_process, Timer
from packages.global_mod import Global
import keyboard
from packages.score_screen import process_score_screen
import getpass
import pygetwindow as gw

processes = []

def player_is_ded():
	boolean = False
	try:	
		wins = gw.getWindowsWithTitle("bulletID#123456")
		i = 0
		while i < len(wins) and not boolean:
			if player_colliding(wins[i]):
				boolean = True
			i+=1
	except Exception as e:
		boolean = False
	return boolean

def player_colliding(target_win):
	try:	
		self_win = gw.getWindowsWithTitle("playerID#123456")[0]
		rect1 = (self_win.left, self_win.top, self_win.width, self_win.height)
		rect2 = (target_win.left, target_win.top, target_win.width, target_win.height)

		overlap = not (rect1[0] + rect1[2] <= rect2[0] or rect1[0] >= rect2[0] + rect2[2] or rect1[1] + rect1[3] <= rect2[1] or rect1[1] >= rect2[1] + rect2[3])
	except Exception as e:
		overlap = False
	return overlap

def do_genocide():
	for p in processes:
		p.kill()
	processes.clear()

if __name__ == '__main__':

	manager = multiprocessing.Manager()
	shared_data = manager.dict()

	player = Player()
	timer = Timer(shared_data)
	
	player_process = multiprocessing.Process(target=run_player, args=(player,))
	timer_process = multiprocessing.Process(target=timer_process, args=(timer,))

	processes.append(timer_process)

	bullet_processes = []
	for i in range(Global.n_bullet):
		bullet_process = multiprocessing.Process(target=process_launch)
		processes.append(bullet_process)
		bullet_processes.append(bullet_process)

	processes.append(player_process)

	player_process.start()
	timer_process.start()

	time.sleep(1)

	for p in bullet_processes:
		p.start()

	while (not keyboard.is_pressed('esc') and not player_is_ded()): pass
	do_genocide()

	process_score_screen(getpass.getuser(), shared_data['time'])
