import random
import numpy as np
from PIL import Image
from midiutil import MIDIFile

def poly(a,b,c) :
    return a + b + c
f = open("poly_log.txt","w")
g = open("keys.txt","w")
rand_tab = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','0','9','8','7','6','5','4','3','2','1','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
teseract = {}
FLAG = "JDHACK{________________}"
timeout = 0 
i = 0
for a in range(10):
    for b in range(10):
        for c in range(10):
            for d in range(10):
                for e in range(10):
                    if timeout == 0 and i < len(FLAG):
                        pixel_data = np.random.randint(
                        low=0, 
                        high=256,
                        size=((e + d + 1)*100,(e + d + 1)*100, 3),
                        dtype=np.uint8
                        )
                        image = Image.fromarray(pixel_data)
                        name = "image" + str(i)
                        image.save(name+".png")
                        MF = MIDIFile(1)
                        TRACK = 0
                        CHANNEL = 0
                        TIME = 0
                        DURATION = d + 1 
                        VOLUME = 100
                        TEMPO = 10
                        NOTE = 30 
                        MF.addTempo(TRACK, TIME, TEMPO)
                        MF.addNote(TRACK,CHANNEL,NOTE,TIME,DURATION,VOLUME)
                        name = "song"+str(i)
                        with open(name +".mid", "wb") as output :
                            MF.writeFile(output)
                        f.write(str(poly(a,e,d)))
                        f.write("\n")
                        cold = (a+e+d+c) % 256
                        encrypted = (b + a  + c + d + e + cold + poly(a,d,e)) % 256
                        g.write("cold = " + str(cold) + " keys = "+str(encrypted))
                        g.write("\n")
                        teseract[(a, b, c, d, e)] = FLAG[i]
                        i += 1
                        timeout = random.randint(1, 4000) 
                    elif timeout > 0:
                        teseract[(a, b, c, d, e)] =  rand_tab[random.randint(0, len(rand_tab) - 1)]
                        if(i < len(FLAG)) :
                            timeout -= 1  
print(teseract)
