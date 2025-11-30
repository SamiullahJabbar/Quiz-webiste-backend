# tests/admin.py
from django.contrib import admin
from .models import Test, Section, Question, Attempt

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_by', 'created_at')
    search_fields = ('name', 'created_by__email')

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'test', 'title', 'type', 'order', 'duration_minutes')
    list_filter = ('type', 'test')
    ordering = ('test', 'order')

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'section', 'short_text', 'has_image')
    list_filter = ('section__test', 'section__type')

    def short_text(self, obj):
        return (obj.text or "")[:50]
    def has_image(self, obj):
        return bool(obj.image)
    has_image.boolean = True

@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'test', 'score', 'submitted_at')
    list_filter = ('test', 'student')
