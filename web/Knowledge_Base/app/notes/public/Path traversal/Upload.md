# Path Traversal - Upload de fichier malveillant

## Description
L'attaque Path Traversal peut également être exploitée pour téléverser des fichiers malveillants sur le serveur en manipulant le chemin d'accès.

### Exemple de vulnérabilité :
```http
POST /upload HTTP/1.1
Host: vulnerable-website.com
Content-Disposition: form-data; name="file"; filename="evil.php"
```

### Payload (pour téléverser dans un répertoire non sécurisé) :
```
../../../../var/www/html/uploads/evil.php
```

### Résultat :
Le fichier malveillant est stocké dans le répertoire `/uploads/`, ce qui permet à l'attaquant de l'exécuter via une requête HTTP.

### Protection :
- Valider et restreindre les noms de fichiers téléchargés.
- Désactiver l'exécution de scripts dans les répertoires de fichiers téléchargés.
