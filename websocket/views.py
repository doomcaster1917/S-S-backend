from django.http import HttpResponseForbidden, HttpResponse
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status, authentication, exceptions
from .models import User
from rest_framework.generics import RetrieveAPIView
from rest_framework.views import APIView
from django.contrib.auth.decorators import login_required

import json
import time

class GameGroupAPIView(RetrieveAPIView):

    permission_classes = (AllowAny,)

    def post(self, request):

        user_id = request.data.get('user_id')
        current_user = User.objects.get(user_id=user_id)
        group = current_user.group
        if not group:
            time.sleep(0.2) #For case when frontend would call the endpoint faster 
            self.post(request)#than consumers(ws) creates the group object
        players = list(group.user_set.all())

        players.remove(current_user)
        enemy_user = players[0]

        enemy_user_name = f'{enemy_user.first_name} {enemy_user.last_name}'
        enemy_user_avatar = enemy_user.avatar_url

        current_user_name = f'{current_user.first_name} {current_user.last_name}'
        current_user_avatar = current_user.avatar_url


        data = {
            "enemy_user_name": enemy_user_name,
            "enemy_user_id": enemy_user.user_id,
            "enemy_user_avatar": enemy_user_avatar,
            "current_user_avatar": current_user_avatar,
            "current_user_name": current_user_name,
            "group_id": group.owner_id
        }

        return Response(json.dumps(data), status=status.HTTP_200_OK)

class UsersListApIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        users_raw = list(User.objects.values_list('user_id', 'first_name', 'last_name'))
        users = []

        for user in users_raw:
            users.append({'user_id': user[0], 'first_name': user[1], 'last_name': user[2]})

        
        return Response(users)


