from celery import shared_task
from .services import update_page


@shared_task(bind=True)
def handle_webhook_task(self, project_id: int, page_id: int):
    update_page(project_id, page_id)
