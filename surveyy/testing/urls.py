from django.urls import path
from testing import views
urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.user_login, name="login"),
    path("register/", views.signin, name="register"),
    path("logout/", views.user_logout, name="logout"),
    path("profile/", views.profile, name="profile"),
    path("testing/<int:id>/", views.runtest, name="testing"),
    path("test_creating/", views.create_test_page, name="create_test_page"),
    path("test_create/", views.create_test, name="create_test"),
    path("sent_test/", views.sent_test, name="sent_test"),
]
