# Titre : Pemp my key !

**Difficulté** : $\color{red}{\textsf{Difficile}}$ \
**Flag** : JDHACK{n3V3r_533N_$UcH_4_w0ND3rFU1_k3y!}

## Description

Créer un clé privée RSA valide au format PEM contenant le motif suivant : `/jeannedhackctf/`.

### Détails

Le fichier `check.sh` fourni permet de vérifier que votre clé privée est valide avant de la soumettre au serveur.
Une clé valide doit retourner la sortie suivante :
```bash
> ./check.sh key.pem
[+] Key contains pattern
[+] RSA key ok
```

Une fois la clé privée validée de votre côté, connectez-vous au serveur et soumettez votre clé pour récupérer le flag.
```
nc <IP_HOST> 50002
```

**Attention** : cela ne sert à rien de tester toutes vos clés avec le serveur, il lancera exactement le même script de vérification que celui fourni ! Et donc pour limiter le nombre de requêtes, vérifier d'abord en local !

## Auteur(s) du challenge

- loukabvn
