# Ismail Boussekkine — Portfolio

Un portfolio en français, construit autour de votre portrait, de cinq projets et de vos documents. Identité éditoriale ivoire, noir et cuivre ; galerie filtrable, constellation de projets, détails en plein écran, sculpture Three.js, CV, certificats, parcours et contact.

**Livraison locale : ce ZIP n’a pas été publié sur Internet.** La version React compilée est incluse. Le code Django, les migrations et les tests sont fournis ; leur exécution n’a pas pu être vérifiée dans l’environnement de création, qui ne pouvait pas installer les dépendances Python. Voir `docs/VERIFICATIONS.md`.

## Démarrage rapide sous Windows

1. Extraire le ZIP entièrement dans un dossier, par exemple `C:\Users\ismail\portfolio-ismail`.
2. Installer Python 3.10 ou plus si nécessaire (cocher **Add python.exe to PATH**).
3. Pour voir immédiatement l’interface : double-cliquer **APERCU.bat**. Cela utilise seulement Python, sans installer de bibliothèques. L’administration et l’enregistrement des messages sont désactivés dans cet aperçu.
4. Pour installer le projet complet : double-cliquer **INSTALLER.bat**. La première installation nécessite Internet. Choisir son propre nom d’utilisateur et mot de passe administrateur quand le terminal les demande. Le mot de passe ne s’affiche pas pendant la saisie : c’est normal.
5. Après installation, double-cliquer **DEMARRER.bat**.

- Portfolio : `http://127.0.0.1:8000`
- Administration : `http://127.0.0.1:8000/admin/`
- Laisser la fenêtre du terminal ouverte. `Ctrl+C` arrête le serveur.
- Si `py` n’est pas reconnu mais `python` fonctionne, utiliser `python setup.py`, puis `python start.py` depuis le dossier du projet.
- Ne pas ouvrir directement `frontend/dist/index.html` : les modules JavaScript ont besoin d’un serveur HTTP.

## نفس الخطوات بالدارجة

- فكّ الضغط على ZIP كامل.
- باش تشوف غير الشكل بسرعة: افتح `APERCU.bat`، خاصك Python يكون مثبّت.
- باش تخدم حتى الإدارة والرسائل: افتح `INSTALLER.bat` أول مرة، وخلي الإنترنت خدام.
- منين يسولك على حساب الإدارة، اختار اسم المستخدم وكلمة السر ديالك. ما كاين حتى حساب أو كلمة سر جاهزة.
- من بعد افتح `DEMARRER.bat`. الموقع كيفتح فالمتصفح.
- باش تبدل المشاريع والصور والمعلومات، دخل للرابط `/admin/` وسجّل الدخول.
- النسخة محلية: باش الناس يشوفوها خاص نشر الواجهة وDjango على استضافة، وهاد الخطوة ما تدارَتش فهاد التسليم.

## Technologies réellement utilisées

| Couche | Choix |
| --- | --- |
| Interface | React 19 + TypeScript |
| Outils | Vite 8, Tailwind CSS 4 + CSS personnalisé |
| Animation | CSS, IntersectionObserver, Three.js r160 en module local |
| Serveur | Python + Django 5.2 |
| Données | SQLite en local ; réglages PostgreSQL facultatifs |
| Administration | Django Admin en français |
| Envoi | Enregistrement en base ; notification SMTP facultative |

GSAP et React Three Fiber, envisagés au départ, ne sont pas utilisés : les animations sont natives et Three.js est intégré directement. Le module Three.js provient de la copie déjà fournie dans votre projet Nike ; pas de dépendance CDN à l’exécution.

## Modifier le contenu

Après connexion à `/admin/`, les rubriques **Profil personnel**, **Projets**, **Compétences**, **Certificats** et **Parcours** permettent de modifier le contenu, ajouter des fichiers et changer l’ordre d’affichage.

- Décocher **Publié** masque un élément.
- Les technologies, fonctionnalités et compétences s’écrivent **une par ligne**.
- Ajouter un lien de dépôt ou de démo à un projet fait apparaître le bouton correspondant. Aucun lien de dépôt spécifique n’a été inventé.
- Les liens GitHub et LinkedIn personnels sont déjà configurés.
- Les messages du formulaire apparaissent dans **Messages reçus**. On peut les marquer comme lus ou les supprimer.
- Un rechargement de la page publique récupère les mises à jour.
- Les champs « fichier inclus » pointent vers les fichiers du ZIP. Un fichier téléversé dans l’administration prend la priorité.

Le JSON `backend/initial_content.json` sert uniquement à la première initialisation. `seed_portfolio` ajoute les éléments absents sans écraser ceux déjà modifiés. La copie `frontend/src/content.json` permet un aperçu sans backend ; elle n’est pas automatiquement synchronisée avec la base. **Une publication destinée à recevoir des messages et à refléter l’administration doit inclure Django.**

## Modifier le design / développer avec React

Node.js 22.12 ou plus est nécessaire pour reconstruire l’interface. Les versions npm sont verrouillées dans `package-lock.json`.

Terminal 1, depuis la racine :

```powershell
.venv\Scripts\python.exe backend\manage.py runserver
```

Terminal 2 :

```powershell
cd frontend
npm ci
npm run dev
```

Ouvrir `http://localhost:5173`. Vite transmet `/api/` et `/media/` à Django.

Après modification :

```powershell
cd frontend
npm run build
```

Puis utiliser `DEMARRER.bat` pour afficher la nouvelle version compilée.

- `frontend/src/main.tsx` : composants et interactions.
- `frontend/src/styles.css` : composition, couleurs et responsive.
- `frontend/src/studio.js` : sculpture 3D, arrêt hors écran, limite de résolution.
- `frontend/public/assets` : photo, visuels et documents.
- `backend/portfolio/models.py` : structure des données.
- `backend/portfolio/views.py` : API et traitement du contact.

## Notifications par e-mail (facultatif)

Sans configuration SMTP, les messages sont enregistrés dans l’administration. Pour recevoir également une notification, copier `backend/.env.example` vers `backend/.env` et renseigner `EMAIL_HOST`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `DEFAULT_FROM_EMAIL` et `CONTACT_NOTIFY_EMAIL`. Utiliser les réglages de votre fournisseur. Ne jamais mettre `.env` sur GitHub. Aucun e-mail n’a été envoyé lors de la création du projet.

## Vérifications à lancer après installation

Depuis le dossier `backend`, avec l’environnement Python du projet :

```powershell
..\.venv\Scripts\python.exe manage.py check
..\.venv\Scripts\python.exe manage.py makemigrations --check --dry-run
..\.venv\Scripts\python.exe manage.py test portfolio
```

Les tests couvrent notamment la validation, CSRF, le stockage des messages, le contrôle de fréquence, le masquage des projets et la conservation des modifications au réensemencement.

## Documents et limites de contenu

Le CV utilisé est `CV_Ismail_Boussekkine.pdf` fourni par vous (2e année, formation prévue jusqu’en juin 2027), conservé sans réécriture. Il est orienté emploi étudiant/temps partiel ; vous pourrez le remplacer par une version ciblée développement web depuis l’administration.

Les projets sont présentés à partir du code et des documents fournis, sans affirmer un déploiement public ou des résultats clients. Les cartes GymQuest, Bibliothèque et ISOGYM sont des compositions graphiques, pas des captures de leurs interfaces. Les archives originales de tous vos projets ne sont pas dupliquées dans ce ZIP : il contient le code complet du **nouveau portfolio**.

Voir `docs/DEPLOIEMENT.md`, `docs/VERIFICATIONS.md` et `docs/CREDITS.md`.
