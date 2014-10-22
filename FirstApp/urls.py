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
    url(r'^api/update/password', UserDetail.as_view(), name='change-password'),
    url(r'^api/search',SearchedRecordsList.as_view() , name='search'),
    url(r'^api/change/password',PassChange.as_view() , name='pass-change'),
    url(r'^api/submit/cnic1',RecordDetail1.as_view() , name='cnic1'),
    url(r'^api/submit/cnic2',RecordDetail2.as_view() , name='cnic2'),
    url(r'^api/submit/signature',PassChange.as_view() , name='signature'),
    url(r'^api/get/records/(?P<pk>\d+)/$', FetchUserRecordsDetail.as_view(), name="record-detail"),
    url(r'^api/report1/(?P<month>\d+)/$',AdminReport1.as_view() , name='admin_month_report1'),
    url(r'^api/months',AdminWorkMonths.as_view() , name='admin_months'),
)
