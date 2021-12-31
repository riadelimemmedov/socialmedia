from django.contrib import admin
from django.urls import path

from .views import *

urlpatterns = [
    path('',home_view,name='home'),
    path('myprofile/',my_profile_view,name='my_profile'),
    path('myfriend/',friend_list,name='friend'),
    path('detaildost/<int:id>',detail_friend,name='detaildost'),
    path('update-profile/',updateaccount,name='update-profile'),
    path('my-invites/',invites_recived_view,name='my_invites'),
    path('profile-list/',ProfileListView.as_view(),name='profile_list'),
    path('invite-list/',invite_profiles_list_view,name='invite_profiles_list'),
    path('send-invite/',create_friend,name='send_invite'),
    path('remove-friend/',remove_friend,name='remove_friend'),
    path('accept-friend/',accept_invitation,name='accept_friend'),
    path('reject-friend/',reject_invitation,name='reject_invitation'),
    path('detail-profile/<int:pk>',profile_detali,name='profile_detail'),
    path('search-profile/',search_account,name='search_profile'),
    path('change-password/',change_password,name='sifre_deyisdir'),
    path('contact-view/',ContacView.as_view(),name='contact_profile'),
]