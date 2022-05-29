from django.urls import include, path
from djoser import views

from .views import UserViewSet

urlpatterns = [
    path('users/<int:id>/subscribe/', UserViewSet.as_view(),
         name='subscribe'),
    path('users/subscriptions/', UserViewSet.as_view(),
         name='subscription'),
    path('auth/token/login/', views.TokenCreateView.as_view(), name='login'),
    path('auth/token/logout/', views.TokenDestroyView.as_view(),
         name='logout'),
    path('', include('djoser.urls')),
]
