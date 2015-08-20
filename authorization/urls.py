from django.conf.urls import url
from authorization.views import Login, Logout


urlpatterns = [
    url(r'^logout/$', Logout.as_view(), name="logout"),
    url(r'^login/$', Login.as_view(), name="login"),
]