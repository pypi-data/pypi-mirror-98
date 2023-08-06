from django.contrib import admin
from django import forms
from django.utils.translation import ugettext_lazy as _, gettext
from django.conf import settings
from django.utils.html import format_html

from parler.admin import TranslatableAdmin
from parler.forms import TranslatableModelForm

from .utils import get_html_field_widget
from .models import Attachment, Log
from .entities import Template, Letter
from .utils import to_list


__all__ = (
    'TemplateAdmin',
    'LetterAdmin'
)


class TemplateForm(TranslatableModelForm):
    html = forms.CharField(
        widget=get_html_field_widget(), required=False
    )
    context = forms.CharField(
        label=_('Context'), widget=forms.Textarea(), disabled=True,
        required=False
    )

    class Meta:
        model = Template.model
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance:
            self.fields['context'].initial = Template(self.instance).legend


class AddTemplateForm(TranslatableModelForm):
    class Meta:
        model = Template.model
        fields = ['name', 'event']


@admin.register(Template.model)
class TemplateAdmin(TranslatableAdmin):
    """
    Admin interface for mail.
    """
    list_display = ['event', 'subject']
    form = TemplateForm
    add_form = AddTemplateForm
    fieldsets = (
        (None, {
            'fields': [
                'name', 'event',
            ]
        }),
        (_('Template'), {
            'fields': [
                'subject', 'html', 'context', 'plain'
            ]
        }),
    )
    tilda_fieldsets = (
        (None, {
            'fields': [
                'name', 'event',
            ]
        }),
        (_('Template'), {
            'fields': [
                'subject', 'html', 'context', 'plain'
            ]
        }),
        (_('Integrations'), {
            'fields': [
                'tilda_id'
            ]
        })
    )
    add_fieldsets = (
        (None, {
            'fields': [
                'name', 'event'
            ]
        }),
    )

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets

        if 'postie.integrations.tilda' in settings.INSTALLED_APPS:
            return self.tilda_fieldsets

        return super().get_fieldsets(request, obj)

    def get_form(self, request, obj=None, **kwargs):
        """
        Use special form during user creation
        """
        defaults = {}

        if obj is None:
            defaults['form'] = self.add_form

        defaults.update(kwargs)

        return super().get_form(request, obj, **defaults)


class AttachmentInline(admin.TabularInline):
    model = Attachment
    extra = 0


class LogInline(admin.StackedInline):
    model = Log
    extra = 0

    def has_add_permission(self, *args, **kwargs):
        return False

    def has_change_permission(self, *args, **kwargs):
        return False


def send_letters(modeladmin, request, queryset) -> None:
    """
    Sends selected letters.
    """

    for letter in queryset:
        Letter(letter).send()


send_letters.short_description = "Send letters"


@admin.register(Letter.model)
class LetterAdmin(admin.ModelAdmin):
    """
    Admin interface for mail.
    """

    list_display = ['subject', 'status', 'event', 'created', 'get_recipients']
    list_filter = ['status', 'event']
    search_fields = ['subject', 'recipients']

    inlines = [AttachmentInline, LogInline]
    actions = [send_letters]

    def get_recipients(self, obj):
        recipients_list = to_list(obj.recipients)
        recipients = "<br />".join(recipients_list[:10])

        if len(recipients_list) > 10:
            recipients += gettext('<br />...remaining elements trancated...')

        return format_html(recipients)
    get_recipients.short_description = _('Recipients')
