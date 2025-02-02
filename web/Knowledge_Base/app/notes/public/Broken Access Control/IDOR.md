# IDOR (Insecure Direct Object Reference)

## Description
Une vulnérabilité IDOR (Insecure Direct Object Reference) se produit lorsqu'un utilisateur peut accéder ou modifier des objets auxquels il ne devrait pas avoir accès en manipulant directement les identifiants de ces objets dans une requête. Cela peut conduire à l'accès non autorisé aux données ou à leur modification.

## Exemples d'attaque IDOR
1. **Exemple basique** :
   Supposons que l'URL suivante permette à un utilisateur de visualiser son profil :  
   `https://example.com/user/profile?id=123`

   Un attaquant pourrait changer l'ID pour accéder au profil d'un autre utilisateur :  
   `https://example.com/user/profile?id=124`

2. **Modification d'objet** :  
   Une API REST pourrait permettre de mettre à jour un enregistrement en envoyant une requête PATCH avec un ID :  
   `/api/orders/123`  
   En modifiant l'ID, un utilisateur non autorisé peut altérer la commande d'un autre utilisateur.

## Techniques de détection
- **Requêtes manuelles** : Manipulez les paramètres d'URL et les données envoyées dans les requêtes pour tester l'accès.
- **Fuzzing automatisé** : Utilisez des outils d'automatisation pour essayer plusieurs ID d'objets.

## Conseils de prévention
1. Implémentez des contrôles d'autorisation sur les objets.
2. Évitez de dépendre uniquement des identifiants d'objets transmis par les utilisateurs.

