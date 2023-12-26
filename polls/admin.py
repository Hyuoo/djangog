from django.contrib import admin
from .models import *

# Register your models here.
#admin.site.register(Choice)

# CRUD

#class ChoiceInline(admin.StackedInline):
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        ('질문', {'fields':['question_text']}),
        ('생성일', {'fields':['pub_date'], 'classes': ['collapse']}),
        ('소유자', {'fields':['owner']}),
    ]
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    readonly_fields = ['pub_date']
    inlines = [ChoiceInline]
    list_filter = ['pub_date']
    search_fields = ['question_text', 'choice__choice_text']

admin.site.register(Question, QuestionAdmin)
