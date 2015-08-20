from django.conf.urls import include, url

import authorization.urls
import converter.urls
from converter.admin import admin_site

urlpatterns = [
    # Examples:
    # url(r'^$', 'portal.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin_site.urls)),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^portal/', include(converter.urls)),
    url(r'^auth/', include(authorization.urls, "auth")),
]