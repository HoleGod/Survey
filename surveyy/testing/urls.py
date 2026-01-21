from django.urls import path
from testing import views, test_views
urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.user_login, name="login"),
    path("register/", views.signin, name="register"),
    path("logout/", views.user_logout, name="logout"),
    path("profile/", views.profile, name="profile"),
    path("testing/<int:id>/", test_views.runtest, name="testing"),
    path("test_creating/", test_views.create_test_page, name="create_test_page"),
    path("test_create/", test_views.create_test, name="create_test"),
    path("sent_test/", test_views.sent_test, name="sent_test"),
    path("export_exel/<int:test_id>/", test_views.get_file_exel, name="exel")
]
