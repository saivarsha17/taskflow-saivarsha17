from rest_framework.routers import DefaultRouter

from tasks.views import ProjectViewSet, TaskViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r"projects", ProjectViewSet, basename="project")
router.register(r"tasks", TaskViewSet, basename="task")

urlpatterns = router.urls
