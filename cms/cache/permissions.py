# -*- coding: utf-8 -*-
from cms.utils import get_cms_setting
from django.core.cache import cache


PERMISSION_KEYS = [
    'can_change', 'can_add', 'can_delete',
    'can_change_advanced_settings', 'can_publish',
    'can_change_permissions', 'can_move_page',
    'can_moderate', 'can_view']


def get_cache_key(username, key):
    return "%s:permission:%s:%s" % (
        get_cms_setting('CACHE_PREFIX'), username, key)


def get_permission_cache(user, key):
    """
    Helper for reading values from cache
    """
    return cache.get("CMS_PERM" + get_cache_key(user.username, key))


def set_permission_cache(user, key, value):
    """
    Helper method for storing values in cache. Stores used keys so
    all of them can be cleaned when clean_permission_cache gets called.
    """
    # store this key, so we can clean it when required
    cache_key = "CMS_PERM" + get_cache_key(user.username, key)
    cache.set(cache_key, value, get_cms_setting('CACHE_DURATIONS')['permissions'])


def clear_user_permission_cache(user):
    """
    Cleans permission cache for given user.
    """
    for key in PERMISSION_KEYS:
        cache.delete(get_cache_key(user.username, key))


def clear_permission_cache():
    # ED 19.09.2014: Clear the permission cache by deleting according to 
    # a pattern instead of looping through all users.
    #users_dict = User.objects.filter(is_active=True).values('username')
    # for user in users_dict:
    cache.delete_pattern("CMS_PERM*")
    #cache.clear()
