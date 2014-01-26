from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'fridgeit.views.home', name='home'),
    url(r'^logout/$', 'fridgeit.views.logout_page',name='logout'),
    url(r'^index', 'fridgeit.views.index', name='index'),
    url(r'^login', 'fridgeit.views.userlogin', name='login'),
    url(r'^signup', 'fridgeit.views.signup', name='signup'),
    url(r'^validate/$', 'fridgeit.views.validate', name='validate'),
    url(r'^recipes', 'fridgeit.views.get_recipe', name='recipes'),
    url(r'^signup', 'fridgeit.views.signup', name='signup'),
    url(r'^get_food', 'fridgeit.views.get_food', name='get_food'),
    url(r'^add_food', 'fridgeit.views.add_food', name='add_food'),
    url(r'^delete_food', 'fridgeit.views.delete_food', name='delete_food'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
