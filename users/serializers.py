from rest_framework.serializers import ModelSerializer
from users.models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'avatar', 'phone', 'tg_nick', 'tg_chat_id']
