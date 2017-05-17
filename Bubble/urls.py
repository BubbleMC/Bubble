from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings


aggregator = settings.PAYMENT['aggregator'] + '.urls'


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^redirect/', include(aggregator)),
    url(r'^payment/', include(aggregator)),
    url(r'^', include('basic.urls'))
]
