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

def check_password(string):
    a, b = (string[:14], string[14:])
    if len(a) != len(b):
        return False

    if b[::-1] != 'n0htyP_c3vA_35':
        return False 

    if ''.join([chr(ord(e) - 13) for e in a]) != '<a*e#R4hRE&i&e':
        return False 

    return True

def main():
    dialog('System', 'Booting up',end='')
    for i in range(3):
        pause(1)
        show('.',end='')
    show('')
    pause(3)
    dialog('System', 'Connection established')
    pause(10)
    dialog('Anonymous', 'Welcome Jeanne')
    pause(20)
    dialog('Anonymous', 'I was waiting for you...')
    pause(20)
    dialog('Anonymous', 'Do you want to play a game?')
    choice = input('[Jeanne] ')
    if not 'yes'.startswith(choice.lower()):
        dialog('Anonymous', 'See you soon')
    else:
        dialog('Anonymous', "Alright then, I'm sure you will never be able to guess my password")
        pause(10)
        while True:
            try:
                string = input('Enter the password: ')
                if check_password(string):
                    dialog('Anonymous', 'DAMN!')
                    pause(20)
                    dialog('Anonymous', "I let you win this time, but next time it won't be that easy!")
                    pause(20)
                    dialog('Anonymous', 'Here is your precious flag:\nJDHACK{%s}' % string)
                    dialog('System', 'Anonymous Left')
                    break
                else:
                    dialog('Anonymous', 'I told you! You will never be able to guess my password')
                    pause(20)
            except EOFError:
                show('\n')
                break
            except KeyboardInterrupt:
                show('\n')
                break

    dialog('System', 'Connection closed')

if __name__ == '__main__':
    main()
