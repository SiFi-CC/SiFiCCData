from django import forms
from django.db import models
from django.conf import settings
from django.utils.html import mark_safe
class ImageWidget(forms.FileInput):
    """
    A ImageField Widget that shows a thumbnail.
    """

    def __init__(self, attrs={}):
        super(ImageWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None, renderer=None):
        output = []
        if value and hasattr(value, "url"):
            output.append(('<a rel="facebox" target="_blank" href="%s">'
                           '<img class="photo" src="%s" style="height: 100px;" /></a>'
                           % (value.url, value.url)))
        output.append(super(ImageWidget, self).render(name, value, attrs, renderer) )
        return mark_safe(u''.join(output))
class FileWidget(forms.FileInput):
    def __init__(self, attrs={}):
        super(FileWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None, renderer=None):
        output = []
        if value and hasattr(value, "url"):
            output.append(('<a href="%s">download'
                           '</a>'
                           % (value.url)))
        output.append(super(FileWidget, self).render(name, value, attrs, renderer) )
        return mark_safe(u''.join(output))
