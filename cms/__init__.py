# -*- coding: utf-8 -*-
__version__ = '2.4.0'

# patch settings
try:
    from django.conf import settings
    if 'cms' in settings.INSTALLED_APPS:
        from conf import patch_settings
        patch_settings()
except ImportError:  # pragma: no cover
    """
    This exception means that either the application is being built, or is
    otherwise installed improperly. Both make running patch_settings
    irrelevant.
    """
    pass

except:
    # django.core.exceptions.ImproperlyConfigured is raised if trying to
    # build django-cms without a DJANGO_SETTINGS_MODULE defined
    pass
