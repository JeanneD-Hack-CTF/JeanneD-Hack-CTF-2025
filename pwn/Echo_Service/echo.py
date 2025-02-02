import subprocess
 

BANNER = """
 _____     _             _____                 _          
|  ___|   | |           /  ___|               (_)         
| |__  ___| |__   ___   \ `--.  ___ _ ____   ___  ___ ___ 
|  __|/ __| '_ \ / _ \   `--. \/ _ \ '__\ \ / / |/ __/ _ \\
| |__| (__| | | | (_) | /\__/ /  __/ |   \ V /| | (_|  __/
\____/\___|_| |_|\___/  \____/ \___|_|    \_/ |_|\___\___|

"""

def main():
    try:
      print(BANNER)
      print('Enter something:')
      arg = input('> ')
      command = "echo " + arg
      result = subprocess.check_output(command, shell=True)
      print('You entered:', result.decode(), end='')
      print('Bye')
    except:
      print('O_o something went wrong!')

if __name__ == '__main__':
    main()
