# XSS - Reflected XSS

## Description
Le Cross-Site Scripting réfléchi (Reflected XSS) se produit lorsque les données fournies par l'utilisateur sont immédiatement renvoyées dans la réponse HTML sans validation ou échappement adéquats.

### Payload de test :
```html
<script>alert('XSS')</script>
```

### Exemple de requête vulnérable :
```
https://vulnerable-website.com/search?q=<script>alert('XSS')</script>
```

### Résultat :
Le script JavaScript injecté sera exécuté dans le contexte du navigateur de la victime, déclenchant une alerte.

### Protection :
- Échapper correctement les entrées utilisateur avant de les afficher.
- Utiliser des politiques de sécurité de contenu (CSP).
