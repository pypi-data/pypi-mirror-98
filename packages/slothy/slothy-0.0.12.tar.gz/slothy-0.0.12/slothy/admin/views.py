# -*- coding: utf-8 -*-

import json
from django.conf import settings
from django.http import JsonResponse, HttpResponse, FileResponse
from django.contrib.staticfiles import finders

from slothy.db import utils
from slothy.admin import METADATA
from django.shortcuts import redirect


def index(request):
    return redirect('/static/app/index.html', permanent=True)


def manifest(request):
    path = finders.find('app/manifest.json')
    with open(path) as file:
        data = json.load(file)
        data['name'] = settings.PROJECT_NAME
        data['short_name'] = settings.PROJECT_NAME
        data['background_color'] = settings.THEME['BAR_BACKGROUND_COLOR']
        data['theme_color'] = settings.THEME['BAR_BACKGROUND_COLOR']
        for icon in data['icons']:
            icon['src'] = 'icons/logo.png'
    return HttpResponse(json.dumps(data))


def logo(request):
    path = finders.find('logo.png')
    return FileResponse(open(path, 'rb'))


def public(request):
    data = {}
    links = [dict(icon='apps', url='/api/login/', label='')]
    for metadata in METADATA.get('public', ()):
        links.append(utils.get_link(metadata['func']))
    data['type'] = 'public'
    data['links'] = links
    return JsonResponse(data)

