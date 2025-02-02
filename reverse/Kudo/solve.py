# pip install pycryptodome==3.20.0
from argparse import ArgumentParser 
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from base64 import b64decode

def main():
  parser = ArgumentParser()
  parser.add_argument('user')
  parser.add_argument('hash')

  args = parser.parse_args()
 
  # Decode base64
  try:
    decoded = b64decode(args.hash)
  except: 
    print('Hash should be base64 encoded')
    exit(1)

  # Decrypt string 
  key = ''.join([args.user[i % len(args.user)] for i in range(32)]).encode()
  iv = b'58ee6d5465a345d1'

  try:
      cipher = AES.new(key, AES.MODE_CBC, iv)
      decrypted = cipher.decrypt(decoded)
      decrypted = unpad(decrypted, AES.block_size)
  except ValueError:
      print('Fail to decrypt the string, padding is incorrect')
      exit(1)

  # Decode hex 
  hex_decoded = bytes.fromhex(decrypted.decode())

  # Revert xor 
  password_swap = ''.join([chr(hex_decoded[i] ^ i) for i in range(len(hex_decoded))])

  # Swap character
  password = ''
  for c in password_swap:
    match c:
      case '_':
        password += '/'
      case '/':
        password += '_'
      case '+': 
        password += '-'
      case '-':
        password += '+'
      case '!':
        password += '?'
      case '?':
        password += '!'
      case '@':
        password += '#'
      case '#':
        password += '@'
      case _:
        password += c

  print(password)

if __name__ == '__main__':
  main()
