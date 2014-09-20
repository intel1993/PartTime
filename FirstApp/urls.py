from django.conf.urls import patterns, include, url
import xadmin
from Camera.views import *
xadmin.autodiscover()
urlpatterns = patterns('',
    # Examples:
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(xadmin.site.urls)),
    url(r'^api/get/records', FetchUserRecords.as_view(), name='user-records'),
    url(r'^api/login', LoginView.as_view(), name='login'),
    url(r'^api/logout', LogoutView.as_view(), name='logout'),
    url(r'^api/signup', SignUp.as_view(), name='signup'),
    url(r'^api/create/', CreateRecord.as_view(), name='create-record'),
    url(r'^api/get/records', FetchUserRecords.as_view(), name='user-records'),
)
