from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'fridgeit.views.home', name='home'),
    url(r'^login/$', 'fridgeit.views.userlogin', name="login"),
    url(r'^logout/$', 'fridgeit.views.logout_page'),
    url(r'^index', 'fridgeit.views.index', name='index'),
    url(r'^login', 'fridgeit.views.login', name='login'),
    url(r'^$', 'fridgeit.views.index', name='index'),
    url(r'^$', 'fridgeit.views.home', name='home'),
    url(r'^index', 'fridgeit.views.index', name='index'),
    url(r'^index/$', 'fridgeit.views.index', name='index'),
    url(r'^signup', 'fridgeit.views.signup', name='signup'),
    url(r'^recipes', 'fridgeit.views.get_recipe', name='recipes'),
    url(r'^$', 'fridgeit.views.index', name='index'),
    url(r'^signup', 'fridgeit.views.signup', name='signup'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
