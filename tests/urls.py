from rest_framework import routers
from .views import TestViewSet, QuestionViewSet, AttemptViewSet

router = routers.DefaultRouter()
router.register(r'tests', TestViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'attempts', AttemptViewSet)

urlpatterns = router.urls
