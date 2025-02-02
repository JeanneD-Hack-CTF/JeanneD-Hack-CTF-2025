import time
import sys 

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

try:
    from securelib import check_password
except Exception as e:
    print('O_o: oups... something went wrong')
    exit(-42)

def main():
    dialog('System', 'Booting up',end='')
    for i in range(3):
        pause(1)
        show('.',end='')
    show('')
    pause(3)
    dialog('System', 'Connection established')
    pause(10)
    dialog('Anonymous', 'Welcome back Jeanne')
    pause(20)
    dialog('Anonymous', 'Are you ready to fight?')
    choice = input('[Jeanne] ')
    if not 'yes'.startswith(choice.lower()):
        dialog('Anonymous', 'See you soon')
    else:
        dialog('Anonymous', "Alright then, I'm sure you will never be able to guess my password")
        dialog('Anonymous', 'This time my securelib will keep my password secret')
        pause(10)
        while True:
            try:
                string = input('Enter the password: ')
                if check_password(string):
                    dialog('Anonymous', 'HOW IS IT POSSIBLE ?!?')
                    pause(20)
                    dialog('Anonymous', "ARG!!! I swear the next time will not be the same")
                    pause(20)
                    dialog('Anonymous', 'Here is your stupid flag:\nJDHACK{%s}' % string)
                    pause(20)
                    dialog('Anonymous', 'See you soon...')
                    pause(20)
                    dialog('System', 'Anonymous Left')
                    break
                else:
                    dialog('Anonymous', 'I told you! You will never be able to guess my password')
                    pause(20)
            except KeyboardInterrupt:
                show('\n')
                break

    dialog('System', 'Connection closed')

if __name__ == '__main__':
    main()
