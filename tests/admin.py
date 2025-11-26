from django.contrib import admin
from .models import Test, Question, Attempt

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code', 'duration_minutes', 'start_time', 'end_time', 'created_by')
    search_fields = ('name', 'code')
    list_filter = ('start_time', 'end_time')

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'test', 'text', 'correct_option')
    search_fields = ('text',)
    list_filter = ('test',)

@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'test', 'score', 'submitted_at')
    search_fields = ('student__email', 'test__name')
    list_filter = ('submitted_at', 'score')
