from cms.plugin_pool import plugin_pool
from cms.plugin_base import CMSPluginBase
from django.core.cache import cache
from django.utils.translation import ugettext_lazy as _
from cms.plugins.teaser.models import Teaser
from cms.plugins.text.settings import USE_TINYMCE
from django.forms.fields import CharField
from django.conf import settings
from cms.plugins.text.widgets.wymeditor_widget import WYMEditor



class TeaserPlugin(CMSPluginBase):
    model = Teaser
    name = _("Teaser")
    render_template = "cms/plugins/teaser.html"

    def get_editor_widget(self, request, plugins):
        """
        Returns the Django form Widget to be used for
        the text area
        """
        if USE_TINYMCE and "tinymce" in settings.INSTALLED_APPS:
            from cms.plugins.text.widgets.tinymce_widget import TinyMCEEditor
            return TinyMCEEditor(installed_plugins=plugins)
        else:
            return WYMEditor(installed_plugins=plugins)

    def get_form_class(self, request, plugins):
        """
        Returns a subclass of Form to be used by this plugin
        """
        # We avoid mutating the Form declared above by subclassing
        class TextPluginForm(self.form):
            pass
        widget = self.get_editor_widget(request, plugins)
        TextPluginForm.declared_fields["description"] = CharField(widget=widget, required=False)
        return TextPluginForm

    def get_form(self, request, obj=None, **kwargs):
        plugins = plugin_pool.get_text_enabled_plugins(self.placeholder, self.page)
        form = self.get_form_class(request, plugins)
        kwargs['form'] = form # override standard form
        return super(TeaserPlugin, self).get_form(request, obj, **kwargs)

    def render(self, context, instance, placeholder):
        link = cache.get(instance._cache_key)
        if link is None:
            if instance.url:
                link = instance.url
            elif instance.page_link:
                link = instance.page_link.get_absolute_url()
            else:
                link = ""
            cache.set(instance._cache_key, link, 60 * 60 * 24)

        context.update({
            'object':instance,
            'placeholder':placeholder,
            'link':link
        })
        return context

plugin_pool.register_plugin(TeaserPlugin)
