import time
import sys 
import Maze

BASE_DELAY = 0.05

def show(string, end='\n', fp=sys.stdout, delay=BASE_DELAY):
    for c in string:
        fp.write(c)
        fp.flush()
        time.sleep(delay)
    fp.write(end)
    fp.flush()

def dialog(user, msg, end='\n', fp=sys.stdout, delay=BASE_DELAY):
    print(f'[{user}]', file=fp, end=' ')
    fp.flush()
    show(msg, end=end, fp=fp, delay=delay)

def pause(count):
    time.sleep(BASE_DELAY*count)

def enter_maze():
    Maze.generate()
    while not Maze.is_finished():
        dialog('Maze', 'Where do you like to go?')
        try:
            choice = input('[Jeanne] ')
            if len(choice) > 0:
                if 'up'.startswith(choice.lower()): 
                    Maze.up()
                elif 'down'.startswith(choice.lower()): 
                    Maze.down()
                elif 'right'.startswith(choice.lower()): 
                    Maze.right()
                elif 'left'.startswith(choice.lower()): 
                    Maze.left()
                elif 'flag'.startswith(choice.lower()): 
                    Maze.flag() 
        except (EOFError, KeyboardInterrupt):
            show('\n')
            break

def main():
    dialog('System', 'Booting up',end='')
    for i in range(3):
        pause(1)
        show('.',end='')
    show('')
    pause(3)
    dialog('System', 'Connection established')
    pause(10)
    dialog('Anonymous', 'Hello Jeanne')
    pause(20)
    dialog('Anonymous', 'Are you ready to play?')
    choice = input('[Jeanne] ')
    if not 'yes'.startswith(choice.lower()):
        dialog('Anonymous', 'See you soon')
    else:
        try:
            dialog('Anonymous', 'This time I prepared something different since you keep cheating!')
            pause(20)
            dialog('Anonymous', 'I created a maze from which you will never escape!')
            pause(20)
            dialog('Anonymous', "I'm so confident that you will never escape, I bet my name on it")
            pause(20)
            dialog('Anonymous', 'Farewell Jeanne :)')
            pause(20)
            enter_maze()
        except KeyboardInterrupt:
            pass

    dialog('System', 'Connection closed')

if __name__ == '__main__':
    main()
