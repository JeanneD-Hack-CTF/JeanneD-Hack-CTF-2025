# SQL Injection - Extraction de données avec UNION

## Description
L'injection SQL via UNION permet de combiner plusieurs résultats de requêtes SQL. Un attaquant peut exploiter cette technique pour extraire des données d'autres tables.

### Exemple de requête vulnérable :
```sql
SELECT name, price FROM products WHERE id = '$product_id';
```

### Payload :
```sql
' UNION SELECT username, password FROM users --
```

### Requête générée :
```sql
SELECT name, price FROM products WHERE id = '' UNION SELECT username, password FROM users --';
```

### Résultat :
L'attaquant peut extraire les noms d'utilisateurs et mots de passe de la table `users`.

### Protection :
- Limiter l'utilisation de l'opérateur UNION dans les requêtes SQL.
- Utiliser des requêtes préparées.
