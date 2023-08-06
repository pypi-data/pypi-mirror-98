from django.urls import path

from .hook import webhook_receiver


urlpatterns = [
    path('tilda/webhook', webhook_receiver, name='webhook_receiver')
]
