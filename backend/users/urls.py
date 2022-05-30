from django.urls import include, path
from djoser import views

from .views import CustomUserViewSet

urlpatterns = [
    path('users/<int:id>/subscribe/', CustomUserViewSet.as_view(
         {'post': 'create', 'delete': 'destroy'}),
         name='subscribe'),
    path('users/subscriptions/', CustomUserViewSet.as_view({'get': 'list'}),
         name='subscription'),
    path('auth/token/login/', views.TokenCreateView.as_view(), name='login'),
    path('auth/token/logout/', views.TokenDestroyView.as_view(),
         name='logout'),
    path('', include('djoser.urls')),
]
