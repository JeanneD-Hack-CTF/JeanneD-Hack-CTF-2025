# SQL Injection - Bypass Authentification

## Description
L'injection SQL est une technique où un attaquant injecte du code SQL dans une requête pour contourner les mécanismes de sécurité ou accéder à des données non autorisées.

### Exemple de requête vulnérable :
```sql
SELECT * FROM users WHERE username = '$username' AND password = '$password';
```

Si l'application ne filtre pas correctement les entrées utilisateur, un attaquant peut utiliser l'injection suivante pour contourner l'authentification :

### Payload :
```sql
' OR 1=1--
```

### Requête générée :
```sql
SELECT * FROM users WHERE username = '' OR 1=1--' AND password = '';
```

### Résultat :
Cela permet à l'attaquant de se connecter sans connaître de nom d'utilisateur ou de mot de passe valide.

### Protection :
- Utiliser des requêtes préparées (statements).
- Échapper correctement les entrées utilisateur.
