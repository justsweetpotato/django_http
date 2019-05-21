#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path("delete/<str:file_name>/", views.tools_rm_files),
    path("open/", views.tools_open_dir),
]
