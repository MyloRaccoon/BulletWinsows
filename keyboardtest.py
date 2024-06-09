import keyboard

while True:
	if keyboard.is_pressed('left'):
		print('pressed')
	else:
		print("unpressed")