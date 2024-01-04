from rest_framework import permissions


# ログイン中のユーザー自身を認証
class ProfilePermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # SAFE_METHODS:GET以外のリクエストを許可しない。
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.userpro.id == request.user.id


class TweetPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # SAFE_METHODS:GET以外のリクエストを許可しない。
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner.id == request.user.id

