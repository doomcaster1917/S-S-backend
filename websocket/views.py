from django.http import HttpResponseForbidden, HttpResponse
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status, authentication, exceptions
from .models import Group
from rest_framework.generics import RetrieveAPIView
from authentication.models import User
from django.contrib.auth.decorators import login_required
from authentication.serializers import UserSerializer
from authentication.renderers import UserJSONRenderer
import json

class GameGroupAPIView(RetrieveAPIView):

    permission_classes = (AllowAny,)
    model = User
    serializer_class = UserSerializer
    #renderer_classes = (UserJSONRenderer,)


    def retrieve(self, request, group_id):
        group = Group.objects.get(group_id=group_id)

        # if request.user not in group.members.all():
        #     return HttpResponseForbidden("You are not a member of this group. Kindly use the join botton")

        events = group.event_set.all()

        serializer_user = self.serializer_class(request.user)

        current_user_id = serializer_user.data['user_id']

        enemy_user_id = list(group.members.values_list('user_id', flat=True))
        enemy_user_id.remove(current_user_id)
        enemy_user = User.objects.get(user_id=enemy_user_id[0])
        serializer_enemy = self.serializer_class(enemy_user)

        enemy_user_name = f'{serializer_enemy.data["first_name"]} {serializer_enemy.data["last_name"]}'


        current_user_avatar = serializer_user.data['avatar_url']
        enemy_user_avatar = serializer_enemy.data['avatar_url']

        data = {
            "enemy_user_name": enemy_user_name,
            "enemy_user_id": enemy_user_id[0] if enemy_user_id else 0,
            "enemy_user_avatar": enemy_user_avatar,
            "current_user_id": current_user_id,
            "current_user_avatar": current_user_avatar,
            "error": "error",
            "token": authentication.get_authorization_header(request).split()
        }


        return Response(data, status=status.HTTP_200_OK)