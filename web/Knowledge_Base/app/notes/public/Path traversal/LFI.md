# Path Traversal - Lecture de fichiers sensibles

## Description
L'attaque Path Traversal permet à un attaquant d'accéder à des fichiers situés en dehors du répertoire racine de l'application web, en manipulant les paramètres d'entrée qui font référence à des fichiers ou des chemins de fichiers.

### Exemple de requête vulnérable :
```
https://vulnerable-website.com/showfile?filename=report.pdf
```

### Payload :
```
../../../../etc/passwd
```

### Requête générée :
```
https://vulnerable-website.com/showfile?filename=../../../../etc/passwd
```

### Résultat :
Cela permet à l'attaquant de lire des fichiers sensibles tels que `/etc/passwd` sur un système Unix.

### Protection :
- Normaliser les chemins d'accès (sanitize).
- Restreindre les accès en dehors du répertoire autorisé.
- Utiliser des chemins absolus et non manipulables par l'utilisateur.
