BANNER = """
__________            ____.      .__.__   
\______   \___.__.   |    |____  |__|  |  
 |     ___<   |  |   |    \__  \ |  |  |  
 |    |    \___  /\__|    |/ __ \|  |  |__
 |____|    / ____\________(____  /__|____/
           \/                  \/     
"""

banned = ["import", "os", "sys", "system", "subprocess", "pty", "open", "popen", "read" ]

def main():
    print(BANNER)
    print("Write the code you want to test after:")
    try:
        while True:
            code = input('>>> ')
            for keyword in banned:
                if keyword in code:
                    print("WARNING: Escape detected!!!! Shuting down connection!")
                    exit(1)

            exec(code, {'globals': globals()})
    except Exception as e:
        print('O_o something went wrong!')
        print(e)

if __name__ == "__main__":
    main()
