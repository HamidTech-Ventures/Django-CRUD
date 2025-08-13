from rest_framework.routers import DefaultRouter
from .views import ConversationViewSet, MessageViewSet

router = DefaultRouter()
router.register(r"chat/conversations", ConversationViewSet, basename="conversation")
router.register(r"chat/messages", MessageViewSet, basename="message")

urlpatterns = router.urls