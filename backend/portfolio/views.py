import json
import logging
from datetime import timedelta
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.core.validators import validate_email
from django.db.models import F
from django.http import JsonResponse, FileResponse, HttpResponse
from django.middleware.csrf import get_token
from django.utils import timezone
from django.utils.crypto import salted_hmac
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_GET, require_POST
from .models import Profile, Project, SkillGroup, Certificate, Timeline, ContactMessage, RateLimit

log = logging.getLogger(__name__)
SUBJECTS = ['Une opportunité de stage', 'Une offre d’emploi', 'Un projet freelance', 'Une autre idée']
def lines(text): return [x.strip() for x in text.splitlines() if x.strip()]
def uploaded(field, fallback): return field.url if field else fallback

@require_GET
@never_cache
def content(request):
    profile = Profile.objects.first()
    if profile is None:
        return JsonResponse({'error': 'Contenu à initialiser avec python manage.py seed_portfolio.'}, status=503)
    person = {k: getattr(profile, k) for k in ['name','role','location','email','github','linkedin','availability','bio','statement']}
    person.update(portrait=uploaded(profile.portrait, profile.initial_portrait), cv=uploaded(profile.cv, profile.initial_cv))
    projects = []
    for p in Project.objects.filter(published=True):
        item = {k:getattr(p,k) for k in ['slug','title','category','year','theme','intro','description','challenge','approach','status','github','live']}
        item.update(tags=lines(p.tags), features=lines(p.features), image=uploaded(p.image, p.initial_image))
        projects.append(item)
    return JsonResponse({'profile':person, 'projects':projects, 'skills':[{'title':s.title,'items':lines(s.items)} for s in SkillGroup.objects.filter(published=True)], 'certificates':[{'title':c.title,'issuer':c.issuer,'year':c.year,'file':uploaded(c.file,c.initial_file),'verify':c.verify} for c in Certificate.objects.filter(published=True)], 'timeline':list(Timeline.objects.filter(published=True).values('date','title','place','description'))})

@require_GET
@never_cache
@ensure_csrf_cookie
def csrf(request): return JsonResponse({'csrfToken':get_token(request)})

def csrf_failure(request, reason=''):
    if request.path.startswith('/api/'):
        return JsonResponse({'error':'La session de sécurité a expiré. Actualisez la page puis réessayez.'}, status=403)
    return HttpResponse('Vérification de sécurité échouée. Actualisez la page.', status=403)

@require_GET
def health(request): return JsonResponse({'status':'ok'})

@require_POST
def contact(request):
    if len(request.body) > 20000:
        return JsonResponse({'error':'Le message est trop volumineux.'}, status=413)
    try:
        payload=json.loads(request.body)
    except (ValueError, UnicodeDecodeError):
        return JsonResponse({'error':'Format de message invalide.'}, status=400)
    if not isinstance(payload,dict):
        return JsonResponse({'error':'Format de message invalide.'}, status=400)
    if payload.get('website'):
        return JsonResponse({'ok':True}, status=201)
    limits={'name':(2,100),'email':(3,254),'message':(10,5000),'subject':(1,100)}
    values={}
    for key,(minimum,maximum) in limits.items():
        value=payload.get(key)
        if not isinstance(value,str) or not minimum<=len(value.strip())<=maximum:
            return JsonResponse({'error':f'Le champ « {key} » est invalide.'},status=400)
        values[key]=value.strip()
    try: validate_email(values['email'])
    except ValidationError: return JsonResponse({'error':'Vérifiez votre adresse e-mail.'},status=400)
    if values['subject'] not in SUBJECTS or payload.get('consent') not in ('on',True):
        return JsonResponse({'error':'Choisissez un sujet et acceptez l’utilisation de vos coordonnées.'},status=400)
    now=timezone.now()
    # Pas de confiance aveugle dans X-Forwarded-For. Derrière un proxy, configurer REMOTE_ADDR côté serveur.
    bucket=int(now.timestamp())//600
    key=salted_hmac('portfolio.contact',f'{request.META.get("REMOTE_ADDR", "unknown")}:{bucket}').hexdigest()
    RateLimit.objects.filter(expires_at__lt=now).delete()
    rate,_=RateLimit.objects.get_or_create(key=key,defaults={'expires_at':now+timedelta(minutes=11)})
    accepted=RateLimit.objects.filter(pk=rate.pk,count__lt=5).update(count=F('count')+1)
    if not accepted:
        return JsonResponse({'error':'Trop de messages rapprochés. Réessayez dans quelques minutes ou utilisez l’e-mail.'},status=429)
    ContactMessage.objects.create(**values)
    ContactMessage.objects.filter(keep=False,created_at__lt=now-timedelta(days=365)).delete()
    if settings.EMAIL_HOST and settings.CONTACT_NOTIFY_EMAIL:
        try:
            EmailMessage(subject=f'Portfolio : {values["subject"]}',body=f'{values["name"]}\n{values["email"]}\n\n{values["message"]}',from_email=settings.DEFAULT_FROM_EMAIL,to=[settings.CONTACT_NOTIFY_EMAIL],reply_to=[values['email']]).send()
        except Exception:
            # Le message reste dans la base même si la notification SMTP échoue.
            log.warning('Notification SMTP indisponible ; message conservé dans l’administration.')
    return JsonResponse({'ok':True},status=201)

@require_GET
def home(request):
    index=settings.FRONTEND_DIST/'index.html'
    if not index.exists():
        return HttpResponse('Construisez le frontend : cd frontend puis npm run build. Administration : /admin/',status=503)
    return FileResponse(index.open('rb'),content_type='text/html; charset=utf-8')
