from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from foodgram.pagination import CustomPaginator
from .models import Follow, User
from .serializers import FollowListSerializer, FollowSerializer


class FollowView(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request, id):
        following = get_object_or_404(User, id=id)
        data = {'user': request.user.id, 'following': following.id}
        serializer = FollowSerializer(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, id):
        user = request.user
        following = get_object_or_404(User, id=id)
        subscription = get_object_or_404(Follow, user=user,
                                         following=following)
        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FollowListViewSet(ListAPIView):
    queryset = User.objects.all()
    serializer_class = FollowListSerializer
    pagination_class = CustomPaginator
    permission_classes = [permissions.IsAuthenticated, ]

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(following__user=user)
