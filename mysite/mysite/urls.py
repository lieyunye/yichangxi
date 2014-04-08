from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'mysite.views.home', name='home'),
                       # url(r'^mysite/', include('mysite.foo.urls')),
                       
                       # Uncomment the admin/doc line below to enable admin documentation:
                       # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
                       
                       # Uncomment the next line to enable the admin:
                       #url(r'^admin/', include(admin.site.urls)),
                       url(r'^$', 'mysite.views.home', name='home'),

                       )
urlpatterns += patterns(
                        'mysite.grabsite',
                        url(r'^grablist/$','grablist'),
                        )
urlpatterns += patterns(
                        'mysite.views',
                        url(r'^search/$','search'),
                        url(r'^detail/$','detail'),
                        )
urlpatterns += patterns(
                        'mysite.jmdetail',
                        url(r'^testMemcache/$','testMemcache'),
                        url(r'^testMongoDB/$','testMongoDB'),
                        )
urlpatterns += patterns(
                        'mysite.push_ios',
                        url(r'^startPush/$','startPush'),
                        )