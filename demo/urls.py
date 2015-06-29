
from django.conf.urls import include, url
from .views import audioDemo, cameraDemo, driveCar

urlpatterns = [
    url(r'^audio$', audioDemo),
    url(r'^camera$', cameraDemo),
    url(r'^drive_car$', driveCar),
]
