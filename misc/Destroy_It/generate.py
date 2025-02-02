
octets = []

with open("FLAG.png", "rb") as g:
    while (octet := g.read(1)):
        octets.append(octet)
        
ocr = octets[::-1]

with open("Jeanne.png", "ab") as f:
    for oc in ocr:
        f.write(oc)

