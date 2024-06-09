from django.urls import path
from .api_func import fetch_activities_org,update_free_spaces,fetch_activities_vol, resolveApplication, download,get_chats, get_messages,open_chat,get_unread

urlpatterns = [
    path('get_activities_org',fetch_activities_org),
    path('get_activities_vol',fetch_activities_vol),
    path('update_free_spaces',update_free_spaces),
    path('resolve_application',resolveApplication),
    path('download',download),
    path('get_chats',get_chats),
    path('get_messages',get_messages),
    path('open_chat',open_chat),
    path('get_unread',get_unread)
]
