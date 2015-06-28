
from django.conf.urls import include, url
from .views import test, recordAudioDemo, cameraDemo, control

urlpatterns = [
    url(r'^$', test),
    url(r'^audio$', recordAudioDemo),
    url(r'^camera$', cameraDemo),
    url(r'^control$', control),
]
