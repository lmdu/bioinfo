from django.templatetags.static import static
from django.urls import reverse

from django.utils import translation, timezone
from django.contrib.humanize.templatetags.humanize import apnumber, intcomma, intword, naturalday, naturaltime, ordinal
from django.template.defaultfilters import time, date, timesince, timeuntil

from crispy_forms.templatetags.crispy_forms_filters import as_crispy_form
from crispy_forms.utils import render_crispy_form

from jinja2 import Environment

def environment(**options):
	env = Environment(**options,
		extensions=['jinja2.ext.i18n'],
	)
	env.install_gettext_translations(translation)
	env.globals.update({
		'static': static,
		'url': reverse,
		'now': timezone.now(),
		'crispy': render_crispy_form,
	})

	env.filters.update({
		'crispy': as_crispy_form,
		'apnumber': apnumber,
		'intcomma': intcomma,
		'intword': intword,
		'naturalday': naturalday,
		'naturaltime': naturaltime,
		'ordinal': ordinal,
		'time': time,
		'date': date,
		'timesince': timesince,
		'timeuntil': timeuntil
	})

	return env

