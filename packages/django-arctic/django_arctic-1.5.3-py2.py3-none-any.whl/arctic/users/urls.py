from django.conf.urls import url

from .views import UserCreateView, UserListView, UserUpdateView

app_name = "users"

urlpatterns = [
    url(r"^$", UserListView.as_view(), name="list"),
    url(r"^create/$", UserCreateView.as_view(), name="create"),
    url(r"^(?P<pk>\d+)/$", UserUpdateView.as_view(), name="detail"),
]
