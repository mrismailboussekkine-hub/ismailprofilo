from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models


def validate_size(file):
    if file.size > 8 * 1024 * 1024:
        raise ValidationError('Le fichier doit peser moins de 8 Mo.')


class Ordered(models.Model):
    order = models.PositiveIntegerField('Ordre d’affichage', default=0)
    published = models.BooleanField('Publié', default=True)
    class Meta:
        abstract = True
        ordering = ['order', 'pk']


class Profile(models.Model):
    name = models.CharField('Nom', max_length=120)
    role = models.CharField('Titre', max_length=160)
    location = models.CharField('Ville / pays', max_length=160)
    email = models.EmailField('E-mail public')
    github = models.URLField('GitHub', blank=True)
    linkedin = models.URLField('LinkedIn', blank=True)
    availability = models.CharField('Disponibilité', max_length=200)
    bio = models.TextField('Présentation')
    statement = models.CharField('Phrase personnelle', max_length=220)
    portrait = models.ImageField('Nouvelle photo (facultatif)', upload_to='portraits/', blank=True, validators=[validate_size])
    cv = models.FileField('Nouveau CV (facultatif)', upload_to='documents/', blank=True, validators=[FileExtensionValidator(['pdf']), validate_size])
    initial_portrait = models.CharField('Photo incluse', max_length=250, default='/assets/ismail.webp')
    initial_cv = models.CharField('CV inclus', max_length=250, default='/assets/cv-ismail-boussekkine.pdf')
    class Meta:
        verbose_name = 'Profil personnel'
        verbose_name_plural = 'Profil personnel'
    def __str__(self): return self.name
    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)


class Project(Ordered):
    title = models.CharField('Titre', max_length=140)
    slug = models.SlugField('Identifiant du lien', unique=True)
    category = models.CharField('Catégorie', max_length=80, choices=[(x,x) for x in ['Expérience 3D','Interface interactive','Application full stack','Site web']])
    year = models.CharField('Type / date', max_length=100, default='Projet personnel')
    tags = models.TextField('Technologies', help_text='Une technologie par ligne.')
    image = models.ImageField('Visuel', upload_to='projects/', blank=True, validators=[validate_size])
    initial_image = models.CharField('Visuel inclus', max_length=250, blank=True)
    theme = models.CharField('Style visuel', max_length=20, default='iso', choices=[('nike','Produit'),('morocco','Voyage'),('gym','Sport / graphique'),('library','Bibliothèque'),('iso','Sport / typographie')])
    intro = models.CharField('Accroche', max_length=250)
    description = models.TextField('Description')
    features = models.TextField('Fonctionnalités', help_text='Une fonctionnalité par ligne.')
    challenge = models.TextField('Défi')
    approach = models.TextField('Approche')
    status = models.TextField('État et précisions', blank=True)
    github = models.URLField('Dépôt GitHub du projet', blank=True)
    live = models.URLField('URL du projet en ligne', blank=True)
    class Meta(Ordered.Meta):
        verbose_name = 'Projet'
        verbose_name_plural = 'Projets'
    def __str__(self): return self.title


class SkillGroup(Ordered):
    title = models.CharField('Titre', max_length=150)
    items = models.TextField('Compétences', help_text='Une compétence par ligne.')
    class Meta(Ordered.Meta):
        verbose_name = 'Groupe de compétences'
        verbose_name_plural = 'Compétences'
    def __str__(self): return self.title


class Certificate(Ordered):
    title = models.CharField('Titre exact', max_length=220)
    issuer = models.CharField('Organisme', max_length=200)
    year = models.CharField('Année', max_length=20)
    file = models.FileField('Document PDF', upload_to='certificates/', blank=True, validators=[FileExtensionValidator(['pdf']), validate_size])
    initial_file = models.CharField('Document inclus', max_length=250, blank=True)
    verify = models.URLField('Lien de vérification', blank=True)
    class Meta(Ordered.Meta):
        verbose_name = 'Certificat'
        verbose_name_plural = 'Certificats'
    def __str__(self): return self.title


class Timeline(Ordered):
    date = models.CharField('Période', max_length=100)
    title = models.CharField('Titre', max_length=200)
    place = models.CharField('Établissement / organisme', max_length=200)
    description = models.TextField('Description')
    class Meta(Ordered.Meta):
        verbose_name = 'Étape du parcours'
        verbose_name_plural = 'Parcours'
    def __str__(self): return self.title


class ContactMessage(models.Model):
    name = models.CharField('Nom', max_length=100)
    email = models.EmailField('E-mail')
    subject = models.CharField('Sujet', max_length=100)
    message = models.TextField('Message')
    created_at = models.DateTimeField('Reçu le', auto_now_add=True)
    read = models.BooleanField('Lu', default=False)
    keep = models.BooleanField('Conserver pour un échange en cours', default=False)
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Message reçu'
        verbose_name_plural = 'Messages reçus'
    def __str__(self): return f'{self.name} — {self.subject}'


class RateLimit(models.Model):
    key = models.CharField(max_length=64, unique=True)
    count = models.PositiveIntegerField(default=0)
    expires_at = models.DateTimeField()
