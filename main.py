import multiprocessing
import subprocess
import time
from packages.player import run_player, Player
from packages.bullet import process_launch, stop_launching, launch_bullet
from packages.timer import timer_process, Timer
from packages.global_mod import Global
import keyboard
from packages.score_screen import process_score_screen
import getpass

processes = []

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
	for i in range(3):
		bullet_process = multiprocessing.Process(target=process_launch)
		processes.append(bullet_process)
		bullet_processes.append(bullet_process)

	processes.append(player_process)

	player_process.start()
	timer_process.start()

	time.sleep(1)

	for p in bullet_processes:
		p.start()

	while (not keyboard.is_pressed('esc') and player_process.is_alive()): pass
	do_genocide()

	process_score_screen(getpass.getuser(), shared_data['time'])
