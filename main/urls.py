# classroom/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClassRoomViewSet, AssignmentViewSet, SubmissionViewSet,Update, NotificationListView

router = DefaultRouter()
router.register(r'classrooms', ClassRoomViewSet)
router.register(r'assignments', AssignmentViewSet)
router.register(r'submissions', SubmissionViewSet)
router.register(r'11update', Update,basename=('update'))

urlpatterns = [
    path('class', include(router.urls)),
    path('notifications/', NotificationListView.as_view(), name='notification-list'),
    # Other URL patterns
]