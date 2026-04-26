from django.templatetags.static import static
from django.urls import reverse

from django.utils.timesince import timesince
from django.utils import translation, dateformat, timezone

from jinja2 import Environment

def environment(**options):
	env = Environment(**options,
		extensions=['jinja2.ext.i18n'],
	)
	env.install_gettext_translations(translation)
	env.globals.update({
		'static': static,
		'url': reverse,
		'time_format': dateformat.format,
		'time_since': timesince,
		'now': timezone.now(),
	})
	return env

