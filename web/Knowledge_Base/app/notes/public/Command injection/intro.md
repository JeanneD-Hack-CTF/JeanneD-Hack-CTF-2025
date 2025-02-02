# Command Injection - Exécution de commandes système

## Description
L'injection de commande est une vulnérabilité qui permet à un attaquant d'exécuter des commandes système arbitraires sur le serveur.

### Exemple de requête vulnérable :
```python
os.system("ping " + user_input)
```

### Payload :
```bash
; ls -la;
```

### Requête générée :
```bash
ping ; ls -la;
```

### Résultat :
Le serveur exécutera non seulement la commande `ping`, mais aussi la commande `ls -la`, qui listera les fichiers présents dans le répertoire courant.

### Protection :
- Utiliser des API système sécurisées (par exemple `subprocess` avec `shell=False` en Python).
- Valider les entrées utilisateur pour éviter l'injection de commandes.
