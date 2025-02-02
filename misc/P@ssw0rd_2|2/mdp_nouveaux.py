import hashlib
import csv

JOURS = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]
PLANETES = ["mercure", "venus", "terre", "mars", "jupiter", "saturne", "uranus", "neptune"]
POINTS_CARDINAUX = ["nord", "nord-est", "est", "sud-est", "sud", "sud-ouest", "ouest", "nord-ouest"]
SIGNES_ZODIAQUE = ["belier", "taureau", "gemeaux", "cancer", "lion", "vierge", "balance", "scorpion", "sagittaire", "capricorne", "verseau", "poissons"]
NOMS_CARTES = ["david", "pallas", "ogier", "charles", "judith", "lahire", "cesar", "rachel", "hector", "alexandre", "argine", "lancelot"] # roi de pique - valet de trèfle (pique, coeur, carreau, pique)
PREFIXES_UNITE = ["quecto", "ronto", "yocto", "zepto", "atto", "femto", "pico", "nano", "micro", "milli", "kilo", "mega", "giga", "tera", "peta", "exa", "zetta", "yotta", "ronna", "quetta"]
ATOUTS_TAROT = ["individuelle", "enfance", "jeunesse", "maturite", "vieillesse", "matin", "apres-midi", "soir", "nuit", "terre", "air", "eau", "feu", "danse", "achats", "grandair", "artsvisuels", "printemps", "ete", "automne", "hiver", "jeu", "collective"]
ALPHABET_OTAN = ["alpha", "bravo", "charlie", "delta", "echo", "foxtrot", "golf", "hotel", "india", "juliett", "kilo", "lima", "mike", "november", "oscar", "papa", "quebec", "romeo", "sierra", "tango", "uniform", "victor", "whiskey", "x-ray", "yankee", "zulu"]
ELEMENTS_CHIMIQUES = ["hydrogene", "helium", "lithium", "beryllium", "bore", "carbone", "azote", "oxygene", "fluor", "neon", "sodium", "magnesium", "aluminium", "silicium", "phosphore", "soufre", "chlore", "argon", "potassium", "calcium", "scandium", "titane", "vanadium", "chrome", "manganese", "fer", "cobalt", "nickel", "cuivre", "zinc", "gallium", "germanium", "arsenic", "selenium", "brome", "krypton", "rubidium", "strontium", "yttrium", "zirconium", "niobium", "molybdene", "technetium", "ruthenium", "rhodium", "palladium", "argent", "cadmium", "indium", "etain", "antimoine", "tellure", "iode", "xenon", "cesium", "baryum", "lanthane", "cerium", "praseodyme", "neodyme", "promethium", "samarium", "europium", "gadolinium", "terbium", "dysprosium", "holmium", "erbium", "thulium", "ytterbium", "lutecium", "hafnium", "tantale", "tungstene", "rhenium", "osmium", "iridium", "platine", "or", "mercure", "thallium", "plomb", "bismuth", "polonium", "astate", "radon", "francium", "radium", "actinium", "thorium", "protactinium", "uranium", "neptunium", "plutonium", "americium", "curium", "berkelium", "californium", "einsteinium", "fermium", "mendelevium", "nobelium", "lawrencium", "rutherfordium", "dubnium", "seaborgium", "bohrium", "hassium", "meitnerium", "darmstadtium", "roentgenium", "copernicium", "nihonium", "flerovium", "moscovium", "livermorium", "tennesse", "oganesson"]
CHIFFRES_ROMAINS = ["i", "ii", "iii", "iv", "v", "vi", "vii", "viii", "ix", "x", "xi", "xii", "xiii", "xiv", "xv", "xvi", "xvii", "xviii", "xix", "xx", "xxi", "xxii", "xxiii", "xxiv", "xxv", "xxvi", "xxvii", "xxviii", "xxix", "xxx", "xxxi", "xxxii", "xxxiii", "xxxiv", "xxxv", "xxxvi", "xxxvii", "xxxviii", "xxxix", "xxxx", "xxxxi", "xxxxii", "xxxxiii"]

CAMERAS_MDP_CHANGE = [1, 6, 11, 14, 18, 27, 29, 31, 34, 36, 50, 54, 56, 66, 69, 74, 82, 90, 92, 94, 98, 111, 112, 116, 117, 124, 129, 132, 136, 137, 143, 151, 160, 171, 172, 177, 187, 191, 193, 203, 207, 214, 216]
MEMOS_PWDS = []
SHA256 = []

MOTS_DE_PASSE = []

with open('Fichier_joint_au_message_10_cameras.csv') as csvfile:
    lecteur_csv = csv.DictReader(csvfile)
    for row in lecteur_csv:
        if row['Caméra']:
            MEMOS_PWDS.append(row[' Mpewmdos'].strip())
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

def alterner(s1, s2):
    min_len = min(len(s1), len(s2))
    res = ''.join(s1[i] + s2[i] for i in range(min_len))
    res += s1[min_len:] + s2[min_len:]
    return res

def memo_pwd1(): # ((J!aPC)a(PlaAO<))[0-25]
    for i in range(26):
        jour = leetcode(JOURS[i%len(JOURS)])
        point_cardinal = POINTS_CARDINAUX[i%len(POINTS_CARDINAUX)]
        planete = PLANETES[i%len(PLANETES)]
        lettre_otan = ALPHABET_OTAN[i%len(ALPHABET_OTAN)][::-1]
        res = alterner(jour,point_cardinal)
        res = alterner(res,alterner(planete,lettre_otan))
        MOTS_DE_PASSE.append(res)

def memo_pwd2(): # ((PU!aCR+SZ<)aAT<)[0-23]
    for i in range(26,50):
        prefixe_unite = leetcode(PREFIXES_UNITE[(i-26)%len(PREFIXES_UNITE)])
        chiffre_romain = CHIFFRES_ROMAINS[(i-26)%len(CHIFFRES_ROMAINS)].upper()
        signe_zodiaque = SIGNES_ZODIAQUE[(i-26)%len(SIGNES_ZODIAQUE)][::-1]
        atout_tarot = ATOUTS_TAROT[(i-26)%len(ATOUTS_TAROT)][::-1]
        res = alterner(prefixe_unite,chiffre_romain) + signe_zodiaque
        res = alterner(res,atout_tarot)
        MOTS_DE_PASSE.append(res)

def memo_pwd3(): # (AO<NCEC!aJ+)[0-25]
    for i in range(50,76):
        lettre_otan = ALPHABET_OTAN[(i-50)%len(ALPHABET_OTAN)][::-1]
        nom_carte = NOMS_CARTES[(i-50)%len(NOMS_CARTES)]
        element_chimique = leetcode(ELEMENTS_CHIMIQUES[(i-50)%len(ELEMENTS_CHIMIQUES)])
        jour = JOURS[(i-50)%len(JOURS)].upper()
        res = lettre_otan + nom_carte + alterner(element_chimique,jour)
        MOTS_DE_PASSE.append(res)

def memo_pwd4(): # (Pl<aPUAT+SZ!)[0-23]
    for i in range(76,100):
        planete = PLANETES[(i-76)%len(PLANETES)][::-1]
        prefixe_unite = PREFIXES_UNITE[(i-76)%len(PREFIXES_UNITE)]
        atout_tarot = ATOUTS_TAROT[(i-76)%len(ATOUTS_TAROT)].upper()
        signe_zodiaque = leetcode(SIGNES_ZODIAQUE[(i-76)%len(SIGNES_ZODIAQUE)])
        res = alterner(planete,prefixe_unite) + atout_tarot + signe_zodiaque
        MOTS_DE_PASSE.append(res)

def memo_pwd5(): # (NC!EC<+ATaCR)[0-23]
    for i in range(100,124):
        nom_carte = leetcode(NOMS_CARTES[(i-100)%len(NOMS_CARTES)])
        element_chimique = ELEMENTS_CHIMIQUES[(i-100)%len(ELEMENTS_CHIMIQUES)][::-1].upper()
        atout_tarot = ATOUTS_TAROT[(i-100)%len(ATOUTS_TAROT)]
        chiffre_romain = CHIFFRES_ROMAINS[(i-100)%len(CHIFFRES_ROMAINS)]
        res = nom_carte + element_chimique + alterner(atout_tarot,chiffre_romain)
        MOTS_DE_PASSE.append(res)

def memo_pwd6(): # ((PCJ)<SZ+aEC)[0-11]
    for i in range(124,136):
        point_cardinal = POINTS_CARDINAUX[(i-124)%len(POINTS_CARDINAUX)]
        jour = JOURS[(i-124)%len(JOURS)]
        signe_zodiaque = SIGNES_ZODIAQUE[(i-124)%len(SIGNES_ZODIAQUE)].upper()
        element_chimique = ELEMENTS_CHIMIQUES[(i-124)%len(ELEMENTS_CHIMIQUES)]
        res = (point_cardinal + jour)[::-1] + alterner(signe_zodiaque,element_chimique)
        MOTS_DE_PASSE.append(res)

def memo_pwd7(): # ((AOCR)+aPlPC!)[0-23]
    for i in range(136,160):
        lettre_otan = ALPHABET_OTAN[(i-136)%len(ALPHABET_OTAN)]
        chiffre_romain = CHIFFRES_ROMAINS[(i-136)%len(CHIFFRES_ROMAINS)]
        planete = PLANETES[(i-136)%len(PLANETES)]
        point_cardinal = leetcode(POINTS_CARDINAUX[(i-136)%len(POINTS_CARDINAUX)])
        res = alterner((lettre_otan + chiffre_romain).upper(),planete) + point_cardinal
        MOTS_DE_PASSE.append(res)

def memo_pwd8(): # ((ATJ)!(NCaPU)<)[0-27]
    for i in range(160,188):
        atout_tarot = ATOUTS_TAROT[(i-160)%len(ATOUTS_TAROT)]
        jour = JOURS[(i-160)%len(JOURS)]
        nom_carte = NOMS_CARTES[(i-100)%len(NOMS_CARTES)]
        prefixe_unite = PREFIXES_UNITE[(i-160)%len(PREFIXES_UNITE)]
        res = leetcode(atout_tarot + jour) + alterner(nom_carte,prefixe_unite)[::-1]
        MOTS_DE_PASSE.append(res)

def memo_pwd9(): # (((ECaAO)+<a(PUPC!))[0-19]
    for i in range(188,208):
        element_chimique = ELEMENTS_CHIMIQUES[(i-188)%len(ELEMENTS_CHIMIQUES)]
        lettre_otan = ALPHABET_OTAN[(i-188)%len(ALPHABET_OTAN)]
        prefixe_unite = PREFIXES_UNITE[(i-188)%len(PREFIXES_UNITE)]
        point_cardinal = leetcode(POINTS_CARDINAUX[(i-188)%len(POINTS_CARDINAUX)])
        res = alterner((alterner(element_chimique,lettre_otan)).upper()[::-1],prefixe_unite + point_cardinal)
        MOTS_DE_PASSE.append(res)

def memo_pwd10(): # (CR<SZaNC+Pl<!)[0-11]
    for i in range(208,len(SHA256)):
        chiffre_romain = CHIFFRES_ROMAINS[(i-208)%len(CHIFFRES_ROMAINS)][::-1]
        signe_zodiaque = SIGNES_ZODIAQUE[(i-208)%len(SIGNES_ZODIAQUE)]
        nom_carte = NOMS_CARTES[(i-208)%len(NOMS_CARTES)].upper()
        planete = leetcode(PLANETES[(i-208)%len(PLANETES)][::-1])
        res = chiffre_romain + alterner(signe_zodiaque,nom_carte) + planete
        MOTS_DE_PASSE.append(res)

def memo_pwd_changed(): # (((JCR)<a((NC<aSZ<)a(Pl+EC))<!)a((AO<aAT+)!<a(PU+<PC)))[0-42]
    index = 0
    for cam in CAMERAS_MDP_CHANGE:
        jour = JOURS[index%len(JOURS)]
        chiffre_romain = CHIFFRES_ROMAINS[index%len(CHIFFRES_ROMAINS)]
        nom_carte = NOMS_CARTES[index%len(NOMS_CARTES)][::-1]
        signe_zodiaque = SIGNES_ZODIAQUE[index%len(SIGNES_ZODIAQUE)][::-1]
        planete = PLANETES[index%len(PLANETES)].upper()
        element_chimique = ELEMENTS_CHIMIQUES[index%len(ELEMENTS_CHIMIQUES)]
        lettre_otan = ALPHABET_OTAN[index%len(ALPHABET_OTAN)][::-1]
        atout_tarot = ATOUTS_TAROT[index%len(ATOUTS_TAROT)].upper()
        prefixe_unite = PREFIXES_UNITE[index%len(PREFIXES_UNITE)].upper()[::-1]
        point_cardinal = POINTS_CARDINAUX[index%len(POINTS_CARDINAUX)]
        res = leetcode(alterner(alterner(nom_carte,signe_zodiaque),planete+element_chimique)[::-1])
        res = alterner((jour+chiffre_romain)[::-1],res)
        res = alterner(res,alterner(leetcode(alterner(lettre_otan,atout_tarot))[::-1],prefixe_unite+point_cardinal))
        MOTS_DE_PASSE[cam-1] = res
        index += 1

memo_pwd1()
memo_pwd2()
memo_pwd3()
memo_pwd4()
memo_pwd5()
memo_pwd6()
memo_pwd7()
memo_pwd8()
memo_pwd9()
memo_pwd10()
memo_pwd_changed()


# for i in CAMERAS_MDP_CHANGE:
#     print("caméra" + str(i) + " " + MOTS_DE_PASSE[i-1])
print()
for i in range(len(MOTS_DE_PASSE)):
    hash = hashlib.sha256(MOTS_DE_PASSE[i].encode()).hexdigest()
    if(hash == SHA256[i]):
        print("caméra" + str(i+1) + " " + MOTS_DE_PASSE[i])
    else:
        print("caméra" + str(i+1) + " " + MOTS_DE_PASSE[i] + ", " + hash + " != " + SHA256[i])
print()
