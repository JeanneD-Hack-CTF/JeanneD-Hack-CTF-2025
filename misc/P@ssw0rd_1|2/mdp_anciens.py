import hashlib
import csv

MOIS = ["janvier", "fevrier", "mars", "avril", "mai", "juin", "juillet", "aout", "septembre", "octobre", "novembre", "decembre"]
ALPHABET_GREC = ["alpha", "beta", "gamma", "delta", "epsilon", "zeta", "eta", "theta", "iota", "kappa", "lambda", "mu", "nu", "xi", "omicron", "pi", "rho", "sigma", "tau", "upsilon", "phi", "chi", "psi", "omega"]

CAMERAS_MDP_CHANGE = [3, 5, 14, 18, 19, 29]
SERIAL_NUMBERS = []
MEMOS_PWDS = []
SHA256 = []

MOTS_DE_PASSE = []

with open('Fichier_joint_au_message_3_cameras.csv') as csvfile:
    lecteur_csv = csv.DictReader(csvfile)
    for row in lecteur_csv:
        if row['Caméra']:
            SERIAL_NUMBERS.append(row[' Serial Number'].strip())
            MEMOS_PWDS.append(row[' Memo pwds'].strip())
            SHA256.append(row[' sha256'].strip())

remplacements = (
    ("a", "@"),
    ("e", "&"),
    ("i", "!"),
    ("o", "0"),
    ("u", "µ"),
    ("y", "?"),
    ("A", "@"),
    ("E", "&"),
    ("I", "!"),
    ("O", "0"),
    ("U", "µ"),
    ("Y", "?")
)

def leetcode(s):
    for ancien, nouveau in remplacements:
        s = s.replace(ancien, nouveau)
    return s

def memo_pwd1(): # (AG<SNM!)[0-17]
    for i in range(18):
        lettre_grecque = ALPHABET_GREC[i%len(ALPHABET_GREC)][::-1]
        serial_number = SERIAL_NUMBERS[i]
        mois = leetcode(MOIS[i%len(MOIS)])
        res = lettre_grecque + serial_number + mois
        MOTS_DE_PASSE.append(res)

def memo_pwd2(): # ((M<)+AG!SN<)[0-11]
    for i in range(18,len(SERIAL_NUMBERS)):
        mois = MOIS[(i-18)%len(MOIS)][::-1].upper()
        lettre_grecque = ALPHABET_GREC[(i-18)%len(ALPHABET_GREC)]
        serial_number = SERIAL_NUMBERS[i][::-1]
        res = mois + leetcode(lettre_grecque) + serial_number
        MOTS_DE_PASSE.append(res)

memo_pwd1()
memo_pwd2()

for i in CAMERAS_MDP_CHANGE:
    print("caméra" + str(i) + " " + MOTS_DE_PASSE[i-1])
print()
for i in range(len(MOTS_DE_PASSE)):
    hash = hashlib.sha256(MOTS_DE_PASSE[i].encode()).hexdigest()
    if(hash == SHA256[i]):
        print("caméra" + str(i+1) + " " + MOTS_DE_PASSE[i])
    else:
        print("caméra" + str(i+1) + " " + MOTS_DE_PASSE[i] + ", " + hash + " != " + SHA256[i])
