from typing import Optional

from django.conf import settings
from tilda_wrapper_api.client import Client
from postie.models import Template
from .utils import get_tilda_credentials


def get_template_by_page_id(page_id: int) -> Optional[Template]:
    template: Template = Template.objects.filter(
        translations__tilda_id=page_id
    ).prefetch_related('translations').first()

    if not template:
        return None

    # We have to return template with activated language for a given page_id
    for translation in template.translations.all():
        if translation.tilda_id == page_id:
            template.set_current_language(translation.language_code)

    return template


def get_tilda_page_html(page_id: int, credentials) -> str:
    client = Client(
        public=credentials.public_key, secret=credentials.private_key
    )

    page_data = client.get_page_full(page_id)

    return page_data.result.html


def update_template_tilda_data(template: Template, page_id: int):
    credentials = get_tilda_credentials()
    page_html = get_tilda_page_html(page_id, credentials)

    # NOTE: template must be with an activated translation that has
    # corresponding page_id, like it's done in `get_template_by_page_id`
    template.html = page_html
    template.save()


def update_page(project_id: int, page_id: int):
    template = get_template_by_page_id(page_id)

    if not template:
        raise ValueError(
            f'Template with tilda page_id {page_id} does not exists')

    update_template_tilda_data(template, page_id)
