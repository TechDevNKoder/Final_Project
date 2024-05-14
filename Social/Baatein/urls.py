from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('update_profile/', views.update_user, name='profile_update'),
    path('index/', views.index, name='index'),
    path('members/', views.members, name='members'),
    path('profile/<int:pk>', views.profile, name='profile'),
    path('comment_talk/<int:pk>', views.comment_talk, name='comment_talk'),
]


# path('talk/<int:pk>/comment/', views.comment_talk, name='comment_talk'),
# path('talk_show/<int:pk>', views.talk_show, name='talk_show'),
