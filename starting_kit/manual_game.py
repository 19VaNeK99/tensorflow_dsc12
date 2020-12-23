from ingestion_program.core import Game
import keyboard
import time
 
f = Game(5, 10)
field, score, game_over = f.GetCurrentState()
f.Show()

while True:
    command = ''
    if keyboard.is_pressed('up'):
        command = 'up'
    if keyboard.is_pressed('down'):
        command = 'down'
    if keyboard.is_pressed('left'):
        command = 'left'
    if keyboard.is_pressed('right'):
        command = 'right'
    if keyboard.is_pressed('esc'):
        command = 'esc'
    if command in ['up', 'down', 'left', 'right']:
        field, score, game_over = f.Move(command)
        f.Show()
        time.sleep(0.2)
        if game_over:
            command = 'esc'
    if command == 'esc':
        print('finish')
        break

 