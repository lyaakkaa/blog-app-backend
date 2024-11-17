from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SignInView, SignUpView, UserViewSet, TopicViewSet, PostViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'topics', TopicViewSet)
router.register(r'posts', PostViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('signin/', SignInView.as_view(), name='signin'),
    path('signup/', SignUpView.as_view(), name='signup'),  

]