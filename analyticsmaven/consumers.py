import json

from channels import Channel, Group
from channels.sessions import channel_session
from channels.handler import AsgiHandler
from channels.auth import http_session_user, channel_session_user, channel_session_user_from_http

from analyticsmaven.models import Chats, NotificationList, MyUser


@channel_session_user_from_http
def ws_connect(message):
    Group("chat-{}".format(message.user.id)).add(message.reply_channel)
    message.reply_channel.send({
        "accept": True
    })
    message.user.is_online = True
    message.user.save()
    print('WS Connect')


@channel_session_user
def ws_message(message):
    print("Message", message.__dict__)
    params = json.loads(message['text'])
    print("Params", params)
    if params['edit']:
        obj = Chats.objects.get(
            id=params['edit']
        )
        obj.message = params['message']
        obj.save()
    else:
        try:
            receiver = MyUser.objects.get(id=params['receiver'])
            read = False if not receiver.is_online else True
        except:
            read = False
        obj = Chats.objects.create(
            chat_id=params['chat'],
            sender_id=params['sender'],
            receiver_id=params['receiver'],
            message=params['message'],
            read=read,
            msg_type=params['type']
        )

    Group("chat-{}".format(int(params['receiver']))).send({
        "text": json.dumps(
            {
                'chat': params['chat'],
                'sender': params['sender'],
                'receiver': params['receiver'],
                'message': params['message'],
                'time': obj.created_at.strftime('%I:%M %p'),
                'id': obj.id,
                'edit': params['edit'],
                'type': params['type']
            }
        )
    })
    Group("chat-{}".format(message.user.id)).send({
        "text": json.dumps(
            {
                'chat': params['chat'],
                'sender': params['sender'],
                'receiver': params['receiver'],
                'message': params['message'],
                'time': obj.created_at.strftime('%I:%M %p'),
                'id': obj.id,
                'edit': params['edit'],
                'type': params['type']
            }
        )
    })


@channel_session_user
def ws_disconnect(message):
    print('WS Disconnect')
    Group("chat-{}".format(message.user.id)).discard(message.reply_channel)
    message.user.is_online = False
    message.user.save()
