from rest_framework.routers import DefaultRouter

from auth.views import AuthViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r"", AuthViewSet, basename="auth")

urlpatterns = router.urls
