from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, FileViewSet
from .views import ClientUserViewSet, ClientUserProfileViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'files', FileViewSet)

urlpatterns = [
    path('', include(router.urls)),
]


router.register(r'client-users', ClientUserViewSet)
router.register(r'client-user-profiles', ClientUserProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('verify-email/<str:uidb64>/<str:token>/', ClientUserProfileViewSet.as_view({'get': 'verify_email'}), name='verify-email'),
]
