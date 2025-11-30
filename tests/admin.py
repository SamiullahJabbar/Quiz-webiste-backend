# tests/admin.py
from django.contrib import admin
from .models import Test, Section, Question, Attempt

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_by', 'created_at')
    search_fields = ('name', 'created_by__email')

from django.contrib import admin
from .models import Test, Section, Question

class QuestionInline(admin.StackedInline):
    model = Question
    extra = 3
    fields = [
        'text', 'image',
        'is_open_ended',
        'option_a_text', 'option_a_image',
        'option_b_text', 'option_b_image',
        'option_c_text', 'option_c_image',
        'option_d_text', 'option_d_image',
        'correct_option'
    ]

class SectionAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]

admin.site.register(Section, SectionAdmin)
# admin.site.register(Question) 

@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'test', 'score', 'submitted_at')
    list_filter = ('test', 'student')
