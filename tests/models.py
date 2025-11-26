import random, string
from django.db import models
from accounts.models import User

def generate_test_code():
    return ''.join(random.choices(string.digits, k=6))

class Test(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=6, unique=True, default=generate_test_code)
    duration_minutes = models.PositiveIntegerField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tests')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return f"{self.name} ({self.code})"

class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='questions/', blank=True, null=True)
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_option = models.CharField(max_length=1, choices=[('A','A'),('B','B'),('C','C'),('D','D')])

    def __str__(self):
        return f"Q: {self.text[:30]}..."

class Attempt(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attempts')
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='attempts')
    answers = models.JSONField()  # {"Q1":"A","Q2":"C",...}
    score = models.IntegerField(default=0)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.email} - {self.test.name}"
