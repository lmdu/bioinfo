#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.staticfiles.storage import staticfiles_storage
from django.template import defaultfilters
from django.urls import reverse

from jinja2 import Environment

def environment(**options):
	env = Environment(**options)
	env.globals.update({
		'static': staticfiles_storage.url,
		'url': reverse,
		'dj': defaultfilters,
	})
	return env

