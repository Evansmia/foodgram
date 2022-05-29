from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Follow, User
from .serializers import (CustomUserSerializer, FollowListSerializer,
                          FollowSerializer)


class UserViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                  mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (IsAuthenticated,)

    def get_permissions(self):
        if self.action == 'create' or self.action == 'retrieve':
            return (AllowAny(),)
        return super().get_permissions()

    @action(methods=['GET'], detail=False)
    def subscriptions(self, request):
        user_obj = User.objects.filter(following__user=request.user)
        paginator = PageNumberPagination()
        paginator.page_size = 6
        page = paginator.paginate_queryset(user_obj, request)
        serializer = FollowListSerializer(
            page, many=True, context={'current_user': request.user}
        )
        return paginator.get_paginated_response(serializer.data)

    @action(methods=['POST', 'DELETE'], detail=False)
    def subscribe(self, request, id):
        following = get_object_or_404(User, id=id)
        data = {'user': request.user.id, 'following': id}
        serializer = FollowSerializer(data=data)
        if request.method == 'POST':
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.user)
            serializer = FollowListSerializer(following)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        subscription = get_object_or_404(Follow, user=request.user,
                                         following__id=id)
        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
