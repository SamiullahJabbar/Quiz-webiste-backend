from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Test, Question, Attempt
from .serializers import TestSerializer, QuestionSerializer, AttemptSerializer, ResultSerializer



class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]

from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Test, Question, Attempt
from .serializers import TestSerializer, QuestionSerializer, AttemptSerializer, ResultSerializer

class TestViewSet(viewsets.ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    permission_classes = [permissions.IsAuthenticated]  # ✅ only logged-in users

    # 1️⃣ Available tests API
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def available(self, request):
        now = timezone.now()
        tests = Test.objects.filter(start_time__lte=now, end_time__gte=now)
        serializer = TestSerializer(tests, many=True)
        return Response(serializer.data)

    # 2️⃣ Access test by code API
    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def access(self, request):
        code = request.data.get('code')
        try:
            test = Test.objects.get(code=code)
            test_data = TestSerializer(test).data
            return Response({
                "valid": True,
                "test": test_data,
                "questions": QuestionSerializer(test.questions.all(), many=True).data
            })
        except Test.DoesNotExist:
            return Response({"valid": False, "message": "Invalid test code"}, status=400)

    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def verify_code(self, request):
        code = request.data.get('code')
        try:
            test = Test.objects.get(code=code)
            return Response({
                "valid": True,
                "test": {
                    "id": test.id,
                    "name": test.name,
                    "code": test.code,
                    "duration_minutes": test.duration_minutes,
                    "start_time": test.start_time,
                    "end_time": test.end_time
                }
            })
        except Test.DoesNotExist:
            return Response({"valid": False, "message": "Invalid test code"}, status=400)

class AttemptViewSet(viewsets.ModelViewSet):
    queryset = Attempt.objects.all()
    serializer_class = AttemptSerializer
    permission_classes = [permissions.IsAuthenticated]  # ✅ only logged-in users

    def perform_create(self, serializer):
        # student identity from JWT token
        student = self.request.user
        test = serializer.validated_data['test']
        answers = serializer.validated_data['answers']

        # calculate score
        score = 0
        for q in test.questions.all():
            if answers.get(str(q.id)) == q.correct_option:
                score += 1

        serializer.save(student=student, score=score)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def my_results(self, request):
        attempts = Attempt.objects.filter(student=request.user)
        serializer = ResultSerializer(attempts, many=True)
        return Response(serializer.data)
