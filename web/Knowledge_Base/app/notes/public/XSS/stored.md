# XSS - Stored XSS

## Description
Le Cross-Site Scripting stocké (Stored XSS) se produit lorsque des données malveillantes sont stockées dans la base de données, puis affichées sur une page web à chaque visite d'un utilisateur.

### Payload de test :
```html
<script>alert(document.cookie)</script>
```

### Exemple :
Un attaquant injecte le script dans un formulaire de commentaire, et celui-ci est ensuite affiché pour tous les utilisateurs qui consultent la page de commentaires.

### Résultat :
Le script peut voler les cookies des utilisateurs ou rediriger vers une page malveillante.

### Protection :
- Valider et échapper les données saisies avant de les stocker et de les afficher.
- Utiliser un moteur de template sécurisé.
