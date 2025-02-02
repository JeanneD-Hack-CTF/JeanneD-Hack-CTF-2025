
def main():
    encrypted_flag = "OAMDFN~QjN\jZVmLGp\dx"
    decrypted_flag = ""

    for c in encrypted_flag:
        decrypted_char = chr((ord(c) ^ 6) ^ 3)
        decrypted_flag += decrypted_char

    print(decrypted_flag)

if __name__ == '__main__':
    main()
