# tests/models.py
import random, string
from django.db import models
from accounts.models import User
from django.utils import timezone
from ckeditor.fields import RichTextField

def generate_test_code():
    return ''.join(random.choices(string.digits, k=6))

class Test(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    code = models.CharField(max_length=6, unique=True, default=generate_test_code, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tests', null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now) 
    def __str__(self):
        return f"{self.name} ({self.code})"

class Section(models.Model):
    SECTION_TYPES = (
        ('rw1', 'Reading and Writing 1'),
        ('rw2', 'Reading and Writing 2'),
        ('break', 'Break'),
        ('m1', 'Math 1'),
        ('m2', 'Math 2'),
    )
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='sections', null=True, blank=True)
    type = models.CharField(max_length=10, choices=SECTION_TYPES, null=True, blank=True)
    order = models.PositiveIntegerField(null=True, blank=True)
    duration_minutes = models.PositiveIntegerField(null=True, blank=True)
    title = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        unique_together = ('test', 'order')
        ordering = ['order']

    def __str__(self):
        return f"{self.test.name if self.test else ''} - {self.title} ({self.duration_minutes} mins)"


class Question(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='questions', null=True, blank=True)
    text = RichTextField(blank=True, null=True)  
    image = models.ImageField(upload_to='questions/', blank=True, null=True)

    is_open_ended = models.BooleanField(default=False, help_text="Mark this if question requires manual answer")

    option_a_text = models.TextField( blank=True, null=True)
    option_a_image = models.ImageField(upload_to='options/', blank=True, null=True)

    option_b_text = models.TextField( blank=True, null=True)
    option_b_image = models.ImageField(upload_to='options/', blank=True, null=True)

    option_c_text = models.TextField( blank=True, null=True)
    option_c_image = models.ImageField(upload_to='options/', blank=True, null=True)

    option_d_text = models.TextField( blank=True, null=True)
    option_d_image = models.ImageField(upload_to='options/', blank=True, null=True)

    correct_option = models.CharField(
        max_length=1,
        choices=[('A','A'),('B','B'),('C','C'),('D','D')],
        null=True, blank=True
    )

    def __str__(self):
        return f"Q: {(self.text or '')[:30]}..."



class Attempt(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attempts', null=True, blank=True)
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='attempts', null=True, blank=True)
    answers = models.JSONField(default=dict, null=True, blank=True)
    score = models.IntegerField(default=0, null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.email if self.student else ''} - {self.test.name if self.test else ''}"
