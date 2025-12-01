# tests/views.py
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Test, Section, Question, Attempt
from .serializers import (
    TestOverviewSerializer,
    SectionSerializer,
    QuestionSerializer,
    AttemptSerializer
)

class TestViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestOverviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def verify_code(self, request):
        # Input: { "code": "123456" }
        code = request.data.get('code')
        if not code:
            return Response({"message": "Code is required"}, status=400)

        # ✅ Instead of strict lookup, just accept any code
        # Pick first test (or latest) to return overview
        test = Test.objects.first()
        if not test:
            return Response({"valid": False, "message": "No tests available"}, status=404)

        # Return overview, HIDE code
        data = TestOverviewSerializer(test).data
        summary = [
            {
                "section_id": s.id,
                "title": s.title,
                "type": s.type,
                "order": s.order,
                "duration_minutes": s.duration_minutes,
                "question_count": s.questions.count(),
            }
            for s in test.sections.all()
        ]

        return Response({
            "valid": True,
            "received_code": code,  
            "test": data,
            "summary": summary
        }, status=200)


    @action(detail=True, methods=['get'], url_path='section/(?P<section_id>[^/.]+)')
    def get_section(self, request, pk=None, section_id=None):
        # GET /api/tests/<test_id>/section/<section_id>/
        test = self.get_object()
        section = get_object_or_404(Section, id=section_id, test=test)

        # Break sections return only timer info; no questions
        if section.type == 'break':
            return Response({
                "section": {
                    "id": section.id,
                    "title": section.title,
                    "type": section.type,
                    "order": section.order,
                    "duration_minutes": section.duration_minutes
                },
                "is_break": True
            })

        ser = SectionSerializer(section)
        return Response({
            "section": {
                "id": section.id,
                "title": section.title,
                "type": section.type,
                "order": section.order,
                "duration_minutes": section.duration_minutes
            },
            "questions": ser.data.get('questions', [])
        })

    @action(detail=True, methods=['post'], url_path='submit-section')
    def submit_section(self, request, pk=None):
        # POST /api/tests/<test_id>/submit-section/
        # Body: { "section_id": 12, "answers": { "34": "A", "35": "C" } }
        test = self.get_object()
        section_id = request.data.get('section_id')
        answers = request.data.get('answers', {})

        if not section_id:
            return Response({"message": "section_id is required"}, status=400)

        section = get_object_or_404(Section, id=section_id, test=test)
        # Store answers per section in Attempt
        attempt, _ = Attempt.objects.get_or_create(student=request.user, test=test)
        all_answers = attempt.answers or {}
        all_answers[str(section.id)] = answers
        attempt.answers = all_answers
        attempt.save()

        return Response({"message": "Section answers saved", "next": "Proceed to next section"}, status=200)

    @action(detail=True, methods=['post'], url_path='final-submit')
    def final_submit(self, request, pk=None):
        # Optionally compute score here; we only confirm submission
        test = self.get_object()
        try:
            attempt = Attempt.objects.get(student=request.user, test=test)
        except Attempt.DoesNotExist:
            return Response({"message": "No attempt found"}, status=404)

        # Score calculation placeholder (hide correct answers in API)
        # You can implement scoring by comparing attempt.answers with DB correct_option server-side.
        return Response({"message": "Test submitted successfully", "attempt_id": attempt.id}, status=200)



from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Test
from .serializers import TestSummarySerializer

class TestSummaryViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        tests = Test.objects.all()
        serializer = TestSummarySerializer(tests, many=True)
        return Response(serializer.data)
