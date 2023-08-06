from celery import shared_task

__all__ = (
    'send_letter'
)


@shared_task(bind=True, default_retry_delay=30, max_retries=15,)
def send_letter(self, letter_id: int):
    """
    Right now this task is used to send letter. It's the only
    difference between `EmailBackend` and `CeleryEmailBackend` in how
    they send emails

    Args:
        letter_id (int): Letter object id

    """
    from .entities import Letter

    try:
        letter = Letter.load_from_id(letter_id)
        letter._send()
    except Exception as e:
        raise self.retry(exc=e, countdown=2 ** self.request.retries)
