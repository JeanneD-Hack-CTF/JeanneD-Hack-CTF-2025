end_hex = b"\x00\x00\x00\x00\x49\x45\x4e\x44\xae\x42\x60\x82"  
list_oct = []

with open("clone.png", "rb") as f:
    byte = f.read()
    offset = byte.index(end_hex)
    f.seek(offset + len(end_hex))
    octet = f.read(1)
    while octet:
        list_oct.append(octet)
        octet = f.read(1)  
lr = list_oct[::-1]

with open("FLAG.png", "wb") as g:
    for e in lr:
        g.write(e)

