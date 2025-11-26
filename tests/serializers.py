from rest_framework import serializers
from .models import Test, Question, Attempt

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'

class TestSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    class Meta:
        model = Test
        fields = '__all__'

class AttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attempt
        fields = '__all__'

class ResultSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.first_name', read_only=True)
    test_name = serializers.CharField(source='test.name', read_only=True)

    class Meta:
        model = Attempt
        fields = ['id','student_name','test_name','score','submitted_at']
