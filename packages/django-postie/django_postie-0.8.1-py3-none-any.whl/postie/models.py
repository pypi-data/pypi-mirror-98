from ckeditor.fields import RichTextField
from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel
from parler.models import TranslatableModel, TranslatedFields

from .const import EVENTS, LETTER_STATUSES
from .querysets import LetterQuerySet

__all__ = (
    'Template',
    'Letter',
    'Attachment',
    'Log',
)


class Template(TranslatableModel):
    """
    Template model.

    Attributes:
        name (models.CharField): Template system name.
        event (models.CharField): Template event to send email on.
        subject (models.CharField): Letter subject.
        html (RichTextField) Letter html text version.
        plain (mdoels.
    """

    name = models.CharField(verbose_name=_('Name'), max_length=255)

    event = models.CharField(
        verbose_name=_('Event'), max_length=255, choices=EVENTS
    )

    translations = TranslatedFields(
        subject=models.CharField(
            verbose_name=_('Subject'),
            help_text=_('Write variables inside {{  }}.'),
            max_length=255, null=True
        ),
        html=models.TextField(
            verbose_name=_('HTML text'),
            help_text=_('Write variables inside {{  }}.'),
            blank=True, null=True
        ),
        plain=models.TextField(
            verbose_name=_('Plain text'),
            help_text=_(
                'Alternative version of html text.'
                'Write variables inside {{  }}.',
            ),
            blank=True, null=True
        ),
        # Tilda integration fields
        tilda_id=models.PositiveIntegerField(
            verbose_name=_('Tilda id'), blank=True, null=True,
            help_text=_(
                'If not empty `HTML` field will be not used anymore, '
                'intead tilda page will be'
            )
        ),
        tilda_html=models.TextField(
            verbose_name=_('Tilda HTML'), editable=False, blank=True,
            null=True
        )
    )

    class Meta:
        verbose_name = _('Mail template')
        verbose_name_plural = _('Mail templates')

    def __str__(self) -> str:
        return self.name

    def get_html(self) -> str:
        if self.tilda_id:
            return self.tilda_html or self.html

        return self.html


class Letter(TimeStampedModel, models.Model):
    """Mail letter model.

    Attributes:
        subject (CharField): Letter's subject.
        html (RichTextField): Letter's html text.
        text (TextField): Letter's plain text
        email_from (EmailField): Letter's email from(sender).
        recipients (TextField): Letter's list of recipients.
        event (CharField): Letter's event.
        language (CharField): Letter's language was send.
        status (CharField): Letter's send status.
        created (DateTimeField): Log's creation timestamp.
        modified (DateTimeField): Log's updating timestamp.
    """

    subject = models.CharField(max_length=255, verbose_name=_('Subject'))
    html = RichTextField(verbose_name=_('HTML'), blank=True, null=True)
    plain = models.TextField(
        verbose_name=_('Plain text'), blank=True, null=True
    )

    email_from = models.EmailField(
        verbose_name=_('Email from'),
        max_length=255, blank=True, null=True
    )
    recipients = models.TextField(
        verbose_name=_('Letter recipients'),
        help_text=_('Enter email address separated by commas')
    )
    event = models.CharField(
        verbose_name=_('Event'), max_length=255, blank=True, null=True
    )

    status = models.CharField(
        verbose_name=_('Status'), max_length=255,
        choices=LETTER_STATUSES, default=LETTER_STATUSES.draft
    )
    language = models.CharField(
        verbose_name=_('Language'), max_length=127, blank=True, null=True
    )

    objects = LetterQuerySet.as_manager()

    class Meta:
        verbose_name = _('Mail letter')
        verbose_name_plural = _('Mail letters')

    def __str__(self) -> str:
        return f'{self.subject}'


class Attachment(TimeStampedModel, models.Model):
    """Letter attachment.

    Attributes:
        letter (ForeignKey): Attachment's letter relation.
        attachment (FileField): Attachment's file.
        created (DateTimeField): Log's creation timestamp.
        modified (DateTimeField): Log's updating timestamp.
    """

    letter = models.ForeignKey(
        Letter, verbose_name=_('Letter'), on_delete=models.CASCADE,
        related_name='attachments'
    )

    attachment = models.FileField(verbose_name=_('Letter attachment'))

    class Meta:
        verbose_name = _('Letter attachment')
        verbose_name_plural = _('Letter attachments')


class Log(TimeStampedModel, models.Model):
    """Mail log.

    Attributes:
        message (CharField): Log's message.
        traceback (TextField): Log's detailed traceback.
        letter (ForeignKey): Log's letter relation.
        created (DateTimeField): Log's creation timestamp.
        modified (DateTimeField): Log's updating timestamp.
    """

    message = models.CharField(verbose_name=_('Log message'), max_length=255)
    traceback = models.TextField(
        verbose_name=_('Traceback'), blank=True, null=True
    )

    letter = models.ForeignKey(
        Letter, verbose_name=_('Letter'), on_delete=models.CASCADE,
        related_name='letter_logs'
    )

    class Meta:
        verbose_name = _('Log')
        verbose_name_plural = _('Logs')

    def __str__(self) -> str:
        return f'{self.message} at {self.created}'
