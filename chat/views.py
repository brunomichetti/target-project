from django.shortcuts import render
from django.utils.safestring import mark_safe
import json


def index(request):
    return render(request, 'chat/index.html', {})


def room(request, match_id):
    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(match_id))
    })
