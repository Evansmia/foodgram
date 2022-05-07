from django.urls import include, path
from djoser import views

from users.views import FollowView, FollowListViewSet

urlpatterns = [
    path('users/<int:id>/subscribe/', FollowView.as_view(),
         name='subscribe'),
    path('users/subscriptions/', FollowListViewSet.as_view(),
         name='subscription'),
    path('auth/token/login/', views.TokenCreateView.as_view(), name='login'),
    path('auth/token/logout/', views.TokenDestroyView.as_view(),
         name='logout'),
    path('', include('djoser.urls')),
]
