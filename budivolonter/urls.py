from django.contrib import admin
from django.urls import path,include
from .views import welcome, open_activity, reg_org, reg_vol, display_my_profile, login_page, do_logout, activity_form, \
view_applications,register_choice,display_profile,inbox,edit_profile,search_org, search_vol, search_choose, search_activity \
,review_volunteers, review_organizations, admin_start,my_acts

urlpatterns = [
        path('',welcome, name='welcome'),
        path('welcome',welcome, name='welcome'),
        path('open_activity',open_activity, name='open_activity'),
        path('register_organization',reg_org, name='register_organization'),
        path('register_volunteer', reg_vol, name='register_volunteer'),
        path('reg_choose',register_choice),
        path('my_profile',display_my_profile, name='my_profile'),
        path('profile',display_profile, name = 'profile'),
        path('login', login_page, name='login'),
        path('logout', do_logout, name='logout'),
        path('api/', include('budivolonter.api')),
        path('activity_form', activity_form , name='activity_form'),
        path('view_applications', view_applications, name='view_applications'),
        path('inbox', inbox, name='inbox'),
        path('edit_profile', edit_profile, name='edit_profile'),
        path('search_organization', search_org, name ='search_organization'),
        path('search_volunteer', search_vol, name ='search_volunteer'),
        path('search_choose',search_choose, name ='search_choose'),
        path('search_activity', search_activity, name='search_activity'),
        path('search_choose',search_choose, name ='search_choose'),
        path('review_volunteers', review_volunteers, name='review_volunteers'),
        path('review_organizations', review_organizations, name='review_organizations'),
        path('admin_start', admin_start, name='admin_start'),
        path('my_acts', my_acts)
        ]
