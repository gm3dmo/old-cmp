from django.conf.urls.defaults import *
from django.contrib import admin
from cmpm.views import *

admin.autodiscover()

urlpatterns = patterns('',


    # Working pages:
    (r'^$',  main_page),
    # Individual Soldier Details:
    (r'^soldier/(\d+)/$', soldier_detail),
    # Admin page
    (r'^blm2393/(.*)',  admin.site.root),
    (r'^browse/$', browse_page),

    (r'^country/$', browse_countries),
    (r'^country/([a-zA-Z]{2})/$', country_page),

    (r'^cemetery/(\d+)/$', cemetery_page),
    (r'^cemetery/$', browse_cemeteries),

    # Search Page
    (r'^search/$', search_page),

    ######################
    # In progress pages:
    #(r'^casualties/year/(\d+)$', casualties_page),
    (r'^tools/armynumber$',  army_number_page),
)
