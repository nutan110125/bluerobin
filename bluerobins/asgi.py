import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bluerobins.settings")
import channels.asgi
# from whitenoise.django import DjangoWhiteNoise
channel_layer = channels.asgi.get_channel_layer()
