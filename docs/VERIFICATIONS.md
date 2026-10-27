# Vérifications de livraison

## Vérifié

- Compilation TypeScript stricte et build de production Vite réussis.
- Installation npm depuis le package-lock vérifiée dans un dossier propre (cache local, scripts d’installation désactivés).
- Interface chargée dans Chromium ; portrait et sections affichés.
- Filtre Full stack : GymQuest et Bibliothèque ; ouverture et fermeture du détail GymQuest.
- Mode Constellation : état activé et liens des projets filtrés présents.
- Affichage de largeur mobile : 375 px utiles, sans débordement horizontal détecté ; menu mobile et accès au contact.
- Validation native du formulaire : les champs requis bloquent un envoi incomplet.
- Ouverture et fermeture du dialogue de CV.
- Syntaxe des fichiers Python vérifiée par compilation.

## À vérifier après installation locale

- Exécution de Django, migrations, connexion administrateur et tests de l’API : non exécutés dans l’environnement de création, car les dépendances Python n’étaient pas installables.
- L’enregistrement réel d’un message et l’envoi SMTP n’ont donc pas été vérifiés.
- PostgreSQL, déploiement HTTPS et téléversement de médias en production : non testés.
- La sculpture Three.js a un remplacement graphique si WebGL n’est pas disponible. La fluidité sur appareil physique n’a pas été mesurée.

Les tests Django fournis couvrent les messages, CSRF, les limites d’envoi, la confidentialité des données, les modifications éditoriales et la purge. Les lancer avec `python manage.py test portfolio` après installation.
