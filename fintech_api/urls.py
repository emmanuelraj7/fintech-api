from django.contrib import admin
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from accounting import api_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^scheme/', api_views.Scheme_API.as_view()),
    url(r'^transactions/', api_views.Transactions_API.as_view()),
    url(r'^balances/', api_views.Balances_API.as_view()),

]


urlpatterns = format_suffix_patterns(urlpatterns)
