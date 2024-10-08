from django.urls import path
from .views import (
    home_page,
    login_page,
    logout_page,
    register_page,
    settings_page,
    course_page,
    group_page,
    delete_group_page
)


urlpatterns = [
    path("", home_page, name="home"),
    path("settings/", settings_page, name="settings"),
    
    path("course/<int:pk>/", course_page, name="course"),
    
    path("group/<int:pk>/", group_page, name="group"),
    path("delete-group/<int:pk>/", delete_group_page, name="delete_group"),
    
    path("login/", login_page, name="login"),
    path("register/", register_page, name="register"),
    path("logout/", logout_page, name="logout"),
]
