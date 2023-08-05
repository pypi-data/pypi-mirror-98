# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from django.template import Library
from django.core.exceptions import ImproperlyConfigured
from django.utils.safestring import mark_safe
from django_angular_url.core.urlresolvers import get_urls


register = Library()


@register.simple_tag(name='load_djng_urls', takes_context=True)
def djng_urls(context, *namespaces):
    def _replace_namespace(n):
        if n == 'SELF':
            request = context.get('request')
            if not request:
                raise ImproperlyConfigured(
                    "'SELF' was used in 'load_djng_urls' for request "
                    "namespace lookup, but there is no RequestContext.")
            return request.resolver_match.namespace
        elif n == '':
            return None
        return n

    urls = get_urls([_replace_namespace(x) for x in namespaces])
    return mark_safe(json.dumps(urls))
