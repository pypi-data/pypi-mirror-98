# -*- coding: utf-8 -*-

from django.conf.urls import url
from slothy.admin import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = []

urlpatterns += [
    url(r'^static/app/manifest.json$', views.manifest),
    url(r"^static/app/icons/Icon-512.png$", views.logo),
    url(r"^static/app/icons/Icon-192.png$", views.logo),
    url(r"^static/app/favicon.png$", views.logo),
    url(r"^favicon.ico$", views.logo),  # lambda request: redirect(settings.PROJECT_LOGO, permanent=True))
]

urlpatterns += staticfiles_urlpatterns()
