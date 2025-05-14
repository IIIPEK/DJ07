from rest_framework.decorators import api_view
from rest_framework.response import Response

from bot.models import TelegramUser
from bot.serializers import TelegramUserSerializer


@api_view(['POST'])
def register_user(request):
    data = request.data
    user, created = TelegramUser.objects.get_or_create(
        user_id=data['user_id'],
        defaults={
            'username': data.get('username',''),
        }
    )
    serializer = TelegramUserSerializer(user)
    if created:
        serializer = TelegramUserSerializer(user)
        return Response(serializer.data, status=201)
    else:
        return Response({'message': 'User already exists'})

@api_view(['GET'])
def user_info(request, user_id):
    try:
        user = TelegramUser.objects.get(user_id=user_id)
        serializer = TelegramUserSerializer(user)
        return Response(serializer.data)
    except TelegramUser.DoesNotExist:
        return Response({'message': 'Пользователь еще не зарегистрирован'}, status=404)
