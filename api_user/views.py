from django.shortcuts import render
from rest_framework import generics, authentication, permissions
from api_user import serializers
from core.models import Profile, User
from core.onwpermissions import ProfilePermission

from django.db.models import Q
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError


# ユーザーの新規登録
class CreateUserView(generics.CreateAPIView):
    serializer_class = serializers.UserSerializer


# ユーザー登録情報の変更
class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = serializers.UserSerializer
    # Tokenによる認証
    authentication_classes = (authentication.TokenAuthentication,)
    # 認証済みである状態
    permission_classes = (permissions.IsAuthenticated,)

    # ログインしている自身の情報を取得
    def get_object(self):
        return self.request.user


# ユーザーのプロフィールのCRUDを一括作成
class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = serializers.ProfileSerializer
    # Tokenによる認証
    authentication_classes = (TokenAuthentication,)
    # 認証済みである状態
    permission_classes = (permissions.IsAuthenticated, ProfilePermission)

    # 友達のプロフィール一覧を取得
    def get_queryset(self):
        try:
            is_friend = Profile.objects.get(userpro=self.request.user)
        except Profile.DoesNotExist:
            is_friend = None
            return is_friend

        friend_filter = Q()
        for friend in is_friend.friends.all():
            friend_filter = friend_filter | Q(userpro=friend)
        return self.queryset.filter(friend_filter)

    # ログインしている自身を保存
    def perform_create(self, serializer):
        # 複数のプロファイルを作成を防ぐ
        try:
            serializer.save(userpro=self.request.user)
        except IntegrityError:
            raise ValidationError("User can have only one own profile")
