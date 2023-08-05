# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import django
from distutils.version import StrictVersion

DJANGO_VERSION = django.get_version()

strict_django = StrictVersion(DJANGO_VERSION)
strict_django_20 = StrictVersion('2.0')

if strict_django >= strict_django_20:
    from django.urls import (
        get_resolver,
        URLResolver,
        URLPattern
    )
else:
    from django.core.urlresolvers import (
        get_resolver,
        RegexURLResolver as URLResolver,
        RegexURLPattern as URLPattern
    )


def regex_pattern_to_url(pattern):
    """
    Take a url regex pattern from urlconf and return a url that matches it
    """
    url = pattern.replace('^', '').rstrip('$')
    if not url.startswith('/'):
        return '/' + url
    return url


def get_url_patterns(patterns, namespace=None, parent_regex=None,
                     filter_namespaces=None):
    """
    Build a dictionary with url_name:regex_pattern pairs
    Names also include namespace, e.g. {'accounts:login': '^login/$'}
    """
    matches_namespace = not filter_namespaces or namespace in filter_namespaces

    pattern_dict = {}
    for pattern in patterns:

        if isinstance(pattern, URLResolver):  # included namespace
            # Recursively call self with parent namespace name and parent regex
            if strict_django >= strict_django_20:
                reg_pattern = pattern.pattern.regex.pattern
            else:
                reg_pattern = pattern.regex.pattern
            include_namespace = ":".join(filter(None, [namespace, pattern.namespace]))
            include_regex = "".join(filter(None, [parent_regex, reg_pattern]))
            included_patterns = get_url_patterns(
                pattern.url_patterns,
                namespace=include_namespace,
                parent_regex=include_regex,
                filter_namespaces=filter_namespaces
            )
            pattern_dict.update(included_patterns)

        elif isinstance(pattern, URLPattern) and matches_namespace:
            # Join own name with parent namespace name,
            # if one is passed as namespace keyword argument
            # Join own regex with parent regex,
            # if one is passed as parent_regex keyword argument
            name = ":".join(filter(None, [namespace, pattern.name]))
            if strict_django >= strict_django_20:
                reg_pattern = pattern.pattern.regex.pattern
            else:
                reg_pattern = pattern.regex.pattern
            regex = "".join(filter(None, [parent_regex, reg_pattern]))
            pattern_dict[name] = regex_pattern_to_url(regex)

    return pattern_dict


def get_urls(namespaces=None):
    """
    Load urlconf from settings.ROOT_URLCONF attribute
    """
    root_resolver = get_resolver(None)
    return get_url_patterns(
        root_resolver.url_patterns, filter_namespaces=namespaces)
