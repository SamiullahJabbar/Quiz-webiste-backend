# tests/serializers.py
from rest_framework import serializers
from .models import Test, Section, Question, Attempt

class OptionSerializer(serializers.Serializer):
    # Return either text or image URL, whichever exists
    text = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    def get_text(self, obj):
        return obj[0]  # supplied as (text, image_field) pair in QuestionSerializer
    def get_image(self, obj):
        img = obj[1]
        return img.url if img else None


class QuestionSerializer(serializers.ModelSerializer):
    # Only expose question content + options, HIDE correct_option
    question_text = serializers.SerializerMethodField()
    question_image = serializers.SerializerMethodField()

    option_a = serializers.SerializerMethodField()
    option_b = serializers.SerializerMethodField()
    option_c = serializers.SerializerMethodField()
    option_d = serializers.SerializerMethodField()

    # ✅ New field: show if question is open-ended
    is_open_ended = serializers.BooleanField(read_only=True)

    class Meta:
        model = Question
        fields = [
            'id',
            'question_text', 'question_image',
            'is_open_ended',   # ✅ added
            'option_a', 'option_b', 'option_c', 'option_d',
        ]

    def get_question_text(self, obj):
        return obj.text

    def get_question_image(self, obj):
        return obj.image.url if obj.image else None

    def _make_option(self, text, image):
        return OptionSerializer(instance=(text, image)).data

    def get_option_a(self, obj):
        if obj.is_open_ended:
            return None
        return self._make_option(obj.option_a_text, obj.option_a_image)

    def get_option_b(self, obj):
        if obj.is_open_ended:
            return None
        return self._make_option(obj.option_b_text, obj.option_b_image)

    def get_option_c(self, obj):
        if obj.is_open_ended:
            return None
        return self._make_option(obj.option_c_text, obj.option_c_image)

    def get_option_d(self, obj):
        if obj.is_open_ended:
            return None
        return self._make_option(obj.option_d_text, obj.option_d_image)



class SectionSerializer(serializers.ModelSerializer):
    # Provide section meta + questions list
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Section
        fields = ['id', 'title', 'type', 'order', 'duration_minutes', 'questions']

class TestOverviewSerializer(serializers.ModelSerializer):
    # HIDE test code; present sections with their timers and counts
    sections = SectionSerializer(many=True, read_only=True)

    class Meta:
        model = Test
        fields = ['id', 'name', 'sections']

class AttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attempt
        fields = ['id', 'student', 'test', 'answers', 'score', 'submitted_at']
        read_only_fields = ['score', 'submitted_at']



from rest_framework import serializers
from .models import Test, Section, Question

class TestSummarySerializer(serializers.ModelSerializer):
    total_questions = serializers.SerializerMethodField()
    total_duration = serializers.SerializerMethodField()

    class Meta:
        model = Test
        fields = ['id', 'name', 'total_questions', 'total_duration']

    def get_total_questions(self, obj):
        # sum of all section questions
        return sum(section.questions.count() for section in obj.sections.all())

    def get_total_duration(self, obj):
        # sum of all section durations
        return sum(section.duration_minutes for section in obj.sections.all() if section.duration_minutes)
