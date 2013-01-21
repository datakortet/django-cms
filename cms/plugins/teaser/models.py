from django.core.cache import cache
from django.db import models
from django.utils.translation import ugettext_lazy as _
from cms.models import CMSPlugin, Page

class Teaser(CMSPlugin):
    """
    A Teaser
    """
    title = models.CharField(_("title"), max_length=255)
    image = models.ImageField(_("image"), upload_to=CMSPlugin.get_media_path, blank=True, null=True)
    page_link = models.ForeignKey(
        Page, 
        verbose_name=_("page"), 
        help_text=_("If present image will be clickable"), 
        blank=True, 
        null=True, 
        limit_choices_to={'publisher_is_draft': True}
    )
    url = models.CharField(_("link"), max_length=255, blank=True, null=True, help_text=_("If present image will be clickable."))
    description = models.TextField(_("description"), blank=True, null=True)

    @property
    def _cache_key(self):
        return "%s_id_%d" % (self.__class__.__name__, self.id)

    def save(self, *args, **kwargs):
        super(Teaser, self).save(*args, **kwargs)
        cache.delete(self._cache_key)

    def __unicode__(self):
        return self.title
    
    search_fields = ('description',)
