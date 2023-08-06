# django-postie

This project allows you to send emails and manage them in the admin panel.
By default package uses celery to send emails.

## Installation

Update INSTALLED_APPS

```python
INSTALLED_APPS = [
    ...
    'postie',
    'parler',
    'codemirror2',
    'ckeditor',
    'des',
    ...
]
```

Run migrations

```
$ python manage.py migrate
```


### Available settings

`POSTIE_TEMPLATE_CHOICES` - Tuple of tuples. Where the first value is the
value to use in code and second is is verbose(translated).

`POSTIE_TEMPLATE_CONTEXTS` - dictionary with template choices as keys and
dictionaries as values

For example:
```python

POSTIE_TEMPLATE_CONTEXTS = {
    'mail_event': {
        'context_var1': _('Context variable 1 description'),
        'context_vae2': _('Context variable 2 user description'),
        ...
    },
    ...
}
```

`POSTIE_INSTANT_SEND` - whether to send letters instantly or to use celery
task. If `False` `celery` is required.

`POSTIE_HTML_ADMIN_WIDGET` - dictionary with default widget for HTML field
in Template model in django admin interface

For example:
```python

POSTIE_HTML_ADMIN_WIDGET = {
    'widget': 'TinyMCE',
    'widget_module': 'tinymce',
    'attrs': {'attrs': {'cols': 80, 'rows': 10}}
}
```

TODO:

* Send letter admin action
* etc

### Basic example to use:


```python
# your_module.py

from postie.shortcuts import send_mail

send_mail(
    event='MAIL_EVENT',
    recipients=['email@email.com', 'email1@email1.com'],
    context={
        'var1': 'variable context',
        'var2': 'another value'
    },
    from_email='noreply@email.com',
    attachments=[{
        'file_name': open('path-to-the-file')
    }]
)
```

Full documentation check here - https://cyberbudy.gitlab.io/django-postie/

### Integrations

#### Tilda

To use [Tilda](https://tilda.cc/) add integration to settings

```python
INSTALLED_APPS = [
    ...
    'postie.integrations.tilda',
    'solo',
    ...
]
```

Run migrations

```
$ python manage.py migrate
```

Now you can edit Tilda preferences and add corresponding tilda id to your mail templates in the admin.


#### TODO

1. Add optional setup.py installation of requirements
