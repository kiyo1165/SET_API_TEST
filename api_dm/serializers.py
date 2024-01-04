from rest_framework import serializers
from core.models import Message, User, Profile


# 友達のユーザーをフィルターする
class FriendsFilteredPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        # ログインしているリクエストを取得
        request = self.context['request']

        try:
            # 自身のプロフィールを取得
            friends = Profile.objects.get(userpro=request.user)
        except Profile.DoesNotExist:
            friends = None
            return

        # 自身の友達リストを配列に格納

        list_friend = []
        for friend in friends.friends.all():
            list_friend.append(friend.id)

        queryset = User.objects.filter(id__in=list_friend)

        return queryset


class MessageSerializer(serializers.ModelSerializer):
    receiver = FriendsFilteredPrimaryKeyRelatedField()

    class Meta:
        model = Message
        fields = ('id', 'sender', 'receiver', 'message')
        read_only_fields = ('id', 'sender')
