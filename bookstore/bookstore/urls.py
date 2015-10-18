from django.conf.urls import patterns, include, url
from django.contrib import admin
from store.views._base import *

urlpatterns = patterns('',
    url(r'^$', home),
    url(r'^logout/$', logout_page),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'), # If user is not login it will redirect to login page
    url(r'^register/$', register),
    url(r'^home/$', home),
    url(r'^submitbid/$', submit_bid),
    url(r'^mydeals/$', mydeals),
    url(r'^finalizeddeals/$', finalized_deals),
    url(r'^updatedeal/$', update_deal),
    url(r'^adddeal/$', add_deal),
    url(r'^admin/', include(admin.site.urls)),
)
