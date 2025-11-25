from django.urls import path
from . import views


urlpatterns = [
    path('register/',views.register,name='register'),
    path('login/',views.login_view,name="login"),
    path('logout/',views.logout_view,name="logout"),
    path('password_reset/',views.password_reset,name="password_reset"),
    path('reset/<uidb64>/<token>/',views.password_reset_confirm,name="password_reset_confirm"),
    path('profile/edit',views.edit_profile,name="profile_edit"),
    path('profile/<str:username>/follow_action/',views.follow_action,name='follow_action'),
    path('profile/<str:username>',views.profile,name="profile"),
]
