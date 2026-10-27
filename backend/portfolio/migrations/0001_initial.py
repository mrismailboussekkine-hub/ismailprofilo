from django.db import migrations, models
from django.core.validators import FileExtensionValidator
import portfolio.models

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField('Nom', max_length=120)),
                ('role', models.CharField('Titre', max_length=160)),
                ('location', models.CharField('Ville / pays', max_length=160)),
                ('email', models.EmailField('E-mail public')),
                ('github', models.URLField('GitHub', blank=True)),
                ('linkedin', models.URLField('LinkedIn', blank=True)),
                ('availability', models.CharField('Disponibilité', max_length=200)),
                ('bio', models.TextField('Présentation')),
                ('statement', models.CharField('Phrase personnelle', max_length=220)),
                ('portrait', models.ImageField('Nouvelle photo (facultatif)', upload_to='portraits/', blank=True, validators=[portfolio.models.validate_size])),
                ('cv', models.FileField('Nouveau CV (facultatif)', upload_to='documents/', blank=True, validators=[FileExtensionValidator(['pdf']), portfolio.models.validate_size])),
                ('initial_portrait', models.CharField('Photo incluse', max_length=250, default='/assets/ismail.webp')),
                ('initial_cv', models.CharField('CV inclus', max_length=250, default='/assets/cv-ismail-boussekkine.pdf')),
            ],
            options={'verbose_name': 'Profil personnel', 'verbose_name_plural': 'Profil personnel'},
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField('Ordre d’affichage', default=0)),
                ('published', models.BooleanField('Publié', default=True)),
                ('title', models.CharField('Titre', max_length=140)),
                ('slug', models.SlugField('Identifiant du lien', unique=True)),
                ('category', models.CharField('Catégorie', max_length=80, choices=[(x, x) for x in ['Expérience 3D', 'Interface interactive', 'Application full stack', 'Site web']])),
                ('year', models.CharField('Type / date', max_length=100, default='Projet personnel')),
                ('tags', models.TextField('Technologies', help_text='Une technologie par ligne.')),
                ('image', models.ImageField('Visuel', upload_to='projects/', blank=True, validators=[portfolio.models.validate_size])),
                ('initial_image', models.CharField('Visuel inclus', max_length=250, blank=True)),
                ('theme', models.CharField('Style visuel', max_length=20, default='iso', choices=[('nike', 'Produit'), ('morocco', 'Voyage'), ('gym', 'Sport / graphique'), ('library', 'Bibliothèque'), ('iso', 'Sport / typographie')])),
                ('intro', models.CharField('Accroche', max_length=250)),
                ('description', models.TextField('Description')),
                ('features', models.TextField('Fonctionnalités', help_text='Une fonctionnalité par ligne.')),
                ('challenge', models.TextField('Défi')),
                ('approach', models.TextField('Approche')),
                ('status', models.TextField('État et précisions', blank=True)),
                ('github', models.URLField('Dépôt GitHub du projet', blank=True)),
                ('live', models.URLField('URL du projet en ligne', blank=True)),
            ],
            options={'ordering': ['order', 'pk'], 'verbose_name': 'Projet', 'verbose_name_plural': 'Projets'},
        ),
        migrations.CreateModel(
            name='SkillGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField('Ordre d’affichage', default=0)),
                ('published', models.BooleanField('Publié', default=True)),
                ('title', models.CharField('Titre', max_length=150)),
                ('items', models.TextField('Compétences', help_text='Une compétence par ligne.')),
            ],
            options={'ordering': ['order', 'pk'], 'verbose_name': 'Groupe de compétences', 'verbose_name_plural': 'Compétences'},
        ),
        migrations.CreateModel(
            name='Certificate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField('Ordre d’affichage', default=0)),
                ('published', models.BooleanField('Publié', default=True)),
                ('title', models.CharField('Titre exact', max_length=220)),
                ('issuer', models.CharField('Organisme', max_length=200)),
                ('year', models.CharField('Année', max_length=20)),
                ('file', models.FileField('Document PDF', upload_to='certificates/', blank=True, validators=[FileExtensionValidator(['pdf']), portfolio.models.validate_size])),
                ('initial_file', models.CharField('Document inclus', max_length=250, blank=True)),
                ('verify', models.URLField('Lien de vérification', blank=True)),
            ],
            options={'ordering': ['order', 'pk'], 'verbose_name': 'Certificat', 'verbose_name_plural': 'Certificats'},
        ),
        migrations.CreateModel(
            name='Timeline',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField('Ordre d’affichage', default=0)),
                ('published', models.BooleanField('Publié', default=True)),
                ('date', models.CharField('Période', max_length=100)),
                ('title', models.CharField('Titre', max_length=200)),
                ('place', models.CharField('Établissement / organisme', max_length=200)),
                ('description', models.TextField('Description')),
            ],
            options={'ordering': ['order', 'pk'], 'verbose_name': 'Étape du parcours', 'verbose_name_plural': 'Parcours'},
        ),
        migrations.CreateModel(
            name='ContactMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField('Nom', max_length=100)),
                ('email', models.EmailField('E-mail')),
                ('subject', models.CharField('Sujet', max_length=100)),
                ('message', models.TextField('Message')),
                ('created_at', models.DateTimeField('Reçu le', auto_now_add=True)),
                ('read', models.BooleanField('Lu', default=False)),
                ('keep', models.BooleanField('Conserver pour un échange en cours', default=False)),
            ],
            options={'ordering': ['-created_at'], 'verbose_name': 'Message reçu', 'verbose_name_plural': 'Messages reçus'},
        ),
        migrations.CreateModel(
            name='RateLimit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=64, unique=True)),
                ('count', models.PositiveIntegerField(default=0)),
                ('expires_at', models.DateTimeField()),
            ],
            options={},
        ),
    ]
