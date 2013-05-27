from django.core.cache import cache
from django.db import models
from django.utils.translation import ugettext_lazy as _
from cms.models import CMSPlugin, Page

class Link(CMSPlugin):
    """
    A link to an other page or to an external website
    """

    name = models.CharField(_("name"), max_length=256)
    url = models.URLField(_("link"), blank=True, null=True)
    page_link = models.ForeignKey(
        Page, verbose_name=_("page"), blank=True, null=True,
        help_text=_("A link to a page has priority over a text link."))
    mailto = models.EmailField(
        _("mailto"), blank=True, null=True,
        help_text=_("An email adress has priority over a text link."))
    target = models.CharField(
        _("target"), blank=True, max_length=100, choices=((
        ("", _("same window")),
        ("_blank", _("new window")),
        ("_parent", _("parent window")),
        ("_top", _("topmost frame")),
    )))

    @property
    def _cache_key(self):
        return "%s_id_%d" % (self.__class__.__name__, self.id)

    def save(self, *args, **kwargs):
        super(Link, self).save(*args, **kwargs)
        cache.delete(self._cache_key)
    
    def __unicode__(self):
        return self.name

    search_fields = ('name',)
