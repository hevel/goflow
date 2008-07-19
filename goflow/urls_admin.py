from django.conf.urls.defaults import *

urlpatterns = patterns('goflow.workflow.views',
    (r'^application/testenv/(?P<action>create|remove)/(?P<id>.*)/$', 'app_env'),
    (r'^application/teststart/(?P<id>.*)/$', 'test_start'),
)
