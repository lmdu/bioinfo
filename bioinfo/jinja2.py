from django.templatetags.static import static
from django.urls import reverse

from django.utils.timesince import timesince
from django.utils import translation, dateformat, timezone

from crispy_forms.templatetags.crispy_forms_filters import as_crispy_form

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
		'crispy': as_crispy_form,
	})

	env.filters.update({
		'crispy': as_crispy_form,
	})

	return env

