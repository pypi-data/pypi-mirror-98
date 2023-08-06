from unittest import mock
from dataclasses import dataclass

from ckeditor.widgets import CKEditorWidget
from codemirror2.widgets import AdminCodeMirrorEditor
from django.test import TestCase, override_settings
from django.conf import settings
from django.urls import reverse
from django.utils.translation import activate
from django_dynamic_fixture import G, N
from parler.utils.context import switch_language

from postie.models import Template as TemplateModel
from postie.entities import Template
from postie.integrations.tilda.models import Preferences
from postie.integrations.tilda.tasks import handle_webhook_task
from postie.integrations.tilda import services, utils


__all__ = (
    'TildaTemplateTestCase',
)


class TildaTemplateTestCase(TestCase):
    def test_template_with_tilda_returns_proper_html(self):
        activate('it')
        template = N(TemplateModel)
        template.tilda_id = 123
        template.html = "Html"
        template.tilda_html = "Tilda html"
        self.assertEqual(template.get_current_language(), 'it')

        self.assertEqual(template.get_html(), "Tilda html")

        entity = Template(template)
        self.assertEqual(entity.render({})['html'], "Tilda html")

        template.tilda_id = None

        self.assertEqual(template.get_html(), "Html")
        entity = Template(template)
        self.assertEqual(entity.render({})['html'], "Html")

        with switch_language(template, 'en'):
            template.tilda_id = 456
            template.tilda_html = "en html"
            self.assertEqual(template.get_current_language(), 'en')
            self.assertEqual(template.get_html(), "en html")
            entity = Template(template)
            self.assertEqual(entity.render({})['html'], "en html")


class TildaHookTestCase(TestCase):
    @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
    @mock.patch('postie.integrations.tilda.tasks.handle_webhook_task.delay')
    def test_hoop_view_response(self, mock):
        preferences = G(
            Preferences,
            public_key="public",
            private_key="private_key",
            project_id=1
        )
        response = self.client.get(reverse('webhook_receiver'))

        self.assertEqual(response.content.decode(), "")
        self.assertEqual(mock.called, False)

        preferences = G(
            Preferences,
            public_key="public",
            private_key="private_key",
            project_id=1
        )
        response = self.client.get(
            reverse('webhook_receiver'),
            {"publickey": "public", "projectid": 1, 'pageid': 1}
        )

        self.assertEqual(response.content.decode(), "ok")
        self.assertEqual(mock.called, True)


@dataclass
class MockPageResult:
    html: str


@dataclass
class MockPage:
    result: MockPageResult


class TildaServicesTestCase(TestCase):
    def test_get_template_by_page_id(self):
        activate('en')
        self.assertIsNone(services.get_template_by_page_id(1))

        template = G(TemplateModel)
        with switch_language(template, 'en'):
            template.tilda_id = 1
            template.html = "EN"
            template.save()

        self.assertEqual(services.get_template_by_page_id(1).id, template.id)
        self.assertEqual(services.get_template_by_page_id(1).html, "EN")

        activate('it')
        with switch_language(template, 'it'):
            template.tilda_id = 2
            template.html = "IT"
            template.save()

        self.assertEqual(services.get_template_by_page_id(2).id, template.id)
        self.assertEqual(services.get_template_by_page_id(2).html, "IT")

        self.assertEqual(services.get_template_by_page_id(1).id, template.id)
        self.assertEqual(services.get_template_by_page_id(1).html, "EN")

    @mock.patch('tilda_wrapper_api.client.Client.get_page_full', return_value=MockPage(result=MockPageResult('HTML')))
    def test_get_tilda_page_html(self, get_page_full_mock):
        preferences = G(
            Preferences,
            public_key="public",
            private_key="private_key",
            project_id=1
        )

        self.assertEqual(
            services.get_tilda_page_html(1, utils.get_tilda_credentials()),
            'HTML'
        )

    @mock.patch('tilda_wrapper_api.client.Client.get_page_full')
    def test_update_template_tilda_data(self, get_page_full_mock):
        preferences = G(
            Preferences,
            public_key="public",
            private_key="private_key",
            project_id=1
        )

        template = G(TemplateModel)
        template.set_current_language('en')
        template.tilda_id = 1
        template.save()

        get_page_full_mock.return_value = MockPage(
            result=MockPageResult('HTML')
        )

        services.update_template_tilda_data(template, 1)
        self.assertEqual(services.get_template_by_page_id(1).html, 'HTML')

        template.set_current_language('it')
        template.tilda_id = 2
        template.save()

        get_page_full_mock.return_value = MockPage(
            result=MockPageResult('IT HTML')
        )

        services.update_template_tilda_data(template, 2)
        self.assertEqual(services.get_template_by_page_id(2).html, 'IT HTML')
        self.assertEqual(services.get_template_by_page_id(1).html, 'HTML')


class TildaTaskTestCase(TestCase):
    def test_handle_webhook_task(self):
        preferences = G(
            Preferences,
            public_key="public",
            private_key="private_key",
            project_id=1
        )

        with self.assertRaises(ValueError):
            handle_webhook_task(1, 1)
