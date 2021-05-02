from django.urls import path, include
from rest_framework.routers import DefaultRouter

from users_api.views import CreateUser, ConfirmUser, UsersViewSet

router = DefaultRouter()
router.register(prefix='users', viewset=UsersViewSet, basename='users')

urlpatterns = [
    path('v1/', include(router.urls)),
]

urlpatterns += [
    path('v1/auth/email/', CreateUser.as_view(), name='user-registration'),
    path('v1/auth/token/', ConfirmUser.as_view(), name='confirm-user'),

]
