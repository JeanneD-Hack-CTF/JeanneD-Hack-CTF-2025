# Titre : Cryptic archive

## Informations principales

**Difficulté** : $\color{orange}{\textsf{Moyen}}$ \
**Flag** : JDHACK{1_$H0ULD_HAV3_U$3_7H3_Z!P_3NCRYP7_0P7!0N}

## Description

Durant leur dernière assaut numérique sur le site de propagande du gouvernement cybernétique, Jeanne d'Hack a mis
la main sur deux archives.

L'une est chiffrée et l'autre est en clair. Elle pense que les deux sont liés par et que l'archive chiffrée contient
un indice important pouvant l'aider dans sa quête de liberté.
Un extrait de l'historique de commande d'un utilisateur montre que les deux fichiers ont été créés à la suite :

```bash
zip archive.zip propaganda.png
zip secret.zip propaganda.png secret.png
python3 encrypt.py secret.zip
rm secret.png
```
Par chance, elle a aussi exfiltré le script permettant de chiffrer cette archive, mais la clé utilisée semble
aléatoire et impossible à retrouver.

## Auteur(s) du challenge

- loukabvn
