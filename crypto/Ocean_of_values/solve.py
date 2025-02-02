from PIL import Image
from mido import MidiFile

FLAG = ""
LEN = 24

def poly(a, b, c):
    return a + b + c

def map(namefile):
    hashmap = {}
    with open(namefile, 'r') as f:
        ligne = f.read()
        i = 0
        while i < len(ligne):
            if ligne[i] == '(':
                start = i
                i += 1
                while ligne[i] != ')':
                    i += 1
                cle = ligne[start:i + 1]
                i += 4 
                start = i 
                while ligne[i] != "'": 
                    i += 1
                valeur = ligne[start:i ]
                hashmap[eval(cle)] = valeur
            i += 1
    return hashmap
namefile = 'teseract.txt' 
hashmap = map(namefile)

f = open("poly_log.txt", "r")
g = open("keys.txt", "r")

poly_lines = f.readlines()
keys_lines = g.readlines()

for i in range(0, LEN):  
    if i == 24:
        break
    name = "song" + str(i)
    mid = MidiFile(name + ".mid")
    d = (mid.length / 6) - 1
    name = "image" + str(i)
    image = Image.open(name + ".png") 
    width, height = image.size
    e = (width / 100) - d - 1
    poly_i = int(poly_lines[i])
    a = poly_i - d - e
    split = keys_lines[i].split()  
    cold = int(split[2]) 
    keys = int(split[5]) 
    c = (cold - (a + e + d)) % 256
    b = (keys - (a + c + d + e + cold + poly(a, d, e))) % 256

    key = (int(a), int(b), int(c), int(d), int(e))
    if key in hashmap:
        FLAG += hashmap[key]

print(FLAG)
