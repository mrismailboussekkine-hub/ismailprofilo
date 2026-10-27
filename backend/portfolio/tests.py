import json
from datetime import timedelta
from django.core.management import call_command
from django.test import Client, TestCase
from django.utils import timezone
from .models import Profile, Project, ContactMessage

class PortfolioTests(TestCase):
    @classmethod
    def setUpTestData(cls): call_command('seed_portfolio',verbosity=0)
    def setUp(self):
        self.client=Client(enforce_csrf_checks=True)
        self.token=self.client.get('/api/csrf/').json()['csrfToken']
        self.payload={'name':'Visiteur test','email':'test@example.com','subject':'Un projet freelance','message':'Un message de test pour le portfolio.','consent':'on','website':''}
    def send(self,payload=None,token=True):
        return self.client.post('/api/contact/',data=json.dumps(self.payload if payload is None else payload),content_type='application/json',**({'HTTP_X_CSRFTOKEN':self.token} if token else {}))
    def test_contact_saves_and_remains_private(self):
        self.assertEqual(self.send().status_code,201)
        self.assertEqual(ContactMessage.objects.count(),1)
        self.assertNotIn('messages',self.client.get('/api/content/').json())
        self.assertEqual(self.client.get('/admin/portfolio/contactmessage/').status_code,302)
    def test_csrf_required(self):
        self.assertEqual(self.send(token=False).status_code,403)
        self.assertEqual(ContactMessage.objects.count(),0)
    def test_invalid_fields_and_consent(self):
        for patch in [{'email':'invalid'},{'message':'court'},{'name':['x']},{'consent':False},{'subject':'inconnu'}]:
            self.assertEqual(self.send({**self.payload,**patch}).status_code,400)
        self.assertEqual(ContactMessage.objects.count(),0)
    def test_non_object_json_rejected(self): self.assertEqual(self.send(['bad']).status_code,400)
    def test_honeypot_does_not_store(self):
        self.assertEqual(self.send({**self.payload,'website':'https://example.com'}).status_code,201)
        self.assertEqual(ContactMessage.objects.count(),0)
    def test_rate_limit(self):
        for _ in range(5):self.assertEqual(self.send().status_code,201)
        self.assertEqual(self.send().status_code,429)
        self.assertEqual(ContactMessage.objects.count(),5)
    def test_public_content_respects_updates_and_visibility(self):
        Profile.objects.filter(pk=1).update(bio='Présentation modifiée')
        Project.objects.filter(slug='gymquest').update(published=False)
        data=self.client.get('/api/content/').json()
        self.assertEqual(data['profile']['bio'],'Présentation modifiée')
        self.assertNotIn('gymquest',[p['slug'] for p in data['projects']])
        self.assertIsInstance(data['projects'][0]['tags'],list)
    def test_seed_does_not_overwrite_content(self):
        Profile.objects.filter(pk=1).update(bio='Mon texte')
        call_command('seed_portfolio',verbosity=0)
        self.assertEqual(Profile.objects.get(pk=1).bio,'Mon texte')
        self.assertEqual(Project.objects.count(),5)
    def test_retention_preserves_active_correspondence(self):
        self.send()
        old=timezone.now()-timedelta(days=366)
        ContactMessage.objects.all().update(created_at=old)
        active=ContactMessage.objects.create(name='Test',email='active@example.com',subject='Suivi',message='Échange en cours',keep=True)
        ContactMessage.objects.filter(pk=active.pk).update(created_at=old)
        call_command('purge_messages',verbosity=0)
        self.assertEqual(list(ContactMessage.objects.values_list('pk',flat=True)),[active.pk])
    def test_methods_are_restricted(self):
        self.assertEqual(self.client.get('/api/contact/').status_code,405)
        self.assertEqual(self.client.post('/api/content/',HTTP_X_CSRFTOKEN=self.token).status_code,405)
