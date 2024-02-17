from django.urls import path
from chat import views
from chat.views import inbox, chat_messages, send_message, UserSearch, New_message
urlpatterns = [
    path('', inbox, name="inbox"),
    path('<username>', chat_messages, name="chat_messages"),
    path('send/', send_message, name="send_message"),
    path('search/', UserSearch, name='search'),
    path('<username>/new_message/', New_message, name='new_message'),
]
