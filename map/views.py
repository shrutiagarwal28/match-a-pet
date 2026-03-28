from django.shortcuts import render
import requests
from django.core import serializers
from accounts.models import User

import os

mapbox_access_token = os.environ.get("MAPBOX_ACCESS_TOKEN", "")


def map_func(request):
    user1 = User.objects.all()
    # print(user[450].longitude)
    # return render(
    #     request,
    #     'map/maps-shelters.html',
    #     {
    #         'mapbox_access_token': mapbox_access_token,
    #         'user': user,
    #     })

    return render(
        request,
        "map/maps-shelters.html",
        {
            "mapbox_access_token": mapbox_access_token,
            "user1": user1,
        },
    )
