from django.contrib import admin
from .models import Profile, Project, SkillGroup, Certificate, Timeline, ContactMessage
admin.site.site_header = 'Ismail — Atelier du portfolio'
admin.site.site_title = 'Administration du portfolio'
admin.site.index_title = 'Votre contenu, vos projets, vos messages'

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    def has_add_permission(self, request): return not Profile.objects.exists()
    def has_delete_permission(self, request, obj=None): return False

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'published', 'order']
    list_editable = ['published', 'order']
    list_filter = ['category', 'published']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}

@admin.register(SkillGroup)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['title', 'published', 'order']
    list_editable = ['published', 'order']

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ['title', 'issuer', 'published', 'order']
    list_editable = ['published', 'order']

@admin.register(Timeline)
class TimelineAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'published', 'order']
    list_editable = ['published', 'order']

@admin.action(description='Marquer les messages comme lus')
def mark_read(modeladmin, request, queryset): queryset.update(read=True)

@admin.register(ContactMessage)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject', 'created_at', 'read', 'keep']
    list_filter = ['read', 'keep', 'subject']
    search_fields = ['name', 'email', 'message']
    readonly_fields = ['name', 'email', 'subject', 'message', 'created_at']
    actions = [mark_read]
    def has_add_permission(self, request): return False
