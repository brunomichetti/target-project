import datetime
from django.shortcuts import render
from django.utils.safestring import mark_safe
import json
from django.core.paginator import Paginator

from chat.models import MatchMessage
from users.models import CustomUser


def index(request):
    return render(request, 'chat/index.html', {})


def room(request, match_id):
    if isinstance(request.user, CustomUser):
        user = request.user
    else:
        request.user.__reduce__()[1][0]  # Awful hack
    messages = MatchMessage.objects.filter(
        in_match_id=match_id
    ).order_by('-pk')[:10]
    previous_messages = []
    for m in messages:
        if m.sent_by_id != user.id:
            if m.seen_at is None:
                m.seen_at = datetime.datetime.now()
                m.save()
            msg = f"{m.sent_by.name}" " : " f"{m.content}"
        else:
            msg = "You : " f"{m.content}"
        previous_messages = [msg] + previous_messages 
    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(match_id)),
        'previous_messages': previous_messages,
    })
