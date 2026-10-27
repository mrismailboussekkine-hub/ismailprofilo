# Publication du portfolio

Ce projet n’a pas été déployé. La configuration ci-dessous est un point de départ pour un hébergement Python disposant d’un disque persistant ou de PostgreSQL et d’un stockage persistant des médias. Une simple publication du dossier `frontend/dist` affiche le portfolio, mais ne fournit ni l’administration ni l’enregistrement des messages.

## Préparer le serveur

1. Installer les dépendances : `pip install -r backend/requirements-production.txt`.
2. Construire React avec `cd frontend && npm ci && npm run build`.
3. Définir les variables d’environnement depuis `backend/.env.example` :
   - `DJANGO_DEBUG=0`.
   - Une `DJANGO_SECRET_KEY` générée pour ce déploiement.
   - `DJANGO_ALLOWED_HOSTS` avec le domaine réel, sans protocole.
   - `DJANGO_CSRF_TRUSTED_ORIGINS` avec les origines HTTPS réelles.
   - SMTP si des notifications sont souhaitées.
   - PostgreSQL facultatif ; sans ces variables, SQLite est utilisé et son fichier doit rester sur disque persistant.
4. Depuis `backend` : `python manage.py migrate`, `python manage.py seed_portfolio`, `python manage.py createsuperuser`, `python manage.py collectstatic --noinput`.
5. Lancer `python manage.py test portfolio`, puis `python manage.py check --deploy` avec les réglages de production. Résoudre les problèmes avant l’exposition publique.
6. Lancer Gunicorn derrière un reverse proxy HTTPS : `gunicorn config.wsgi:application --bind 127.0.0.1:9000 --workers 2`.
7. Servir `/media/` depuis `backend/media/` par le serveur web. WhiteNoise sert les fichiers statiques compilés et ceux de l’administration. Vérifier les permissions et la persistance des téléversements.

`TRUST_PROXY=1` ne doit être activé que derrière un proxy de confiance qui remplace `X-Forwarded-Proto`. Ne pas rendre Gunicorn directement accessible au public dans ce mode. La limitation du contact est de cinq requêtes valides par tranche de dix minutes et par adresse vue par Django ; derrière un proxy, ajouter un contrôle par IP côté proxy pour éviter de partager la même limite entre visiteurs.

## Conservation et maintenance

- Sauvegarder la base et `backend/media/`.
- Planifier quotidiennement `python manage.py purge_messages` (cron ou tâche de l’hébergeur) pour supprimer les messages de plus de 365 jours, hors échanges marqués en cours.
- La réception d’un message déclenche aussi une purge opportuniste.
- Maintenir Django, Node et les bibliothèques avec leurs mises à jour de sécurité ; les versions utilisées dans ce ZIP ne sont pas une promesse de maintien automatique.
- Vérifier un vrai envoi de contact et une notification SMTP après configuration.
- Le site n’utilise aucun service publicitaire ou analytique. Vérifier la notice de confidentialité selon l’usage réel avant publication.

Référence : https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/
