import json
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction
from portfolio.models import Profile,Project,SkillGroup,Certificate,Timeline
class Command(BaseCommand):
    help='Installe le contenu initial sans écraser les modifications existantes.'
    @transaction.atomic
    def handle(self,*args,**options):
        data=json.loads((settings.BASE_DIR/'initial_content.json').read_text(encoding='utf-8'))
        p=dict(data['profile']);p['initial_portrait']=p.pop('portrait');p['initial_cv']=p.pop('cv')
        Profile.objects.get_or_create(pk=1,defaults=p)
        for i,item in enumerate(data['projects']):
            p=dict(item);slug=p.pop('slug');p['tags']='\n'.join(p['tags']);p['features']='\n'.join(p['features']);p['initial_image']=p.pop('image');p['order']=i
            Project.objects.get_or_create(slug=slug,defaults=p)
        for i,item in enumerate(data['skills']):
            p=dict(item);title=p.pop('title');p['items']='\n'.join(p['items']);p['order']=i
            SkillGroup.objects.get_or_create(title=title,defaults=p)
        for i,item in enumerate(data['certificates']):
            p=dict(item);title=p.pop('title');p['initial_file']=p.pop('file');p['order']=i
            Certificate.objects.get_or_create(title=title,defaults=p)
        for i,item in enumerate(data['timeline']):
            p=dict(item);title=p.pop('title');p['order']=i
            Timeline.objects.get_or_create(title=title,defaults=p)
        self.stdout.write(self.style.SUCCESS('Contenu initial prêt. Les données existantes ont été préservées.'))
