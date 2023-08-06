# Django CMS Google Calendar Plugin

Django CMS Google Calendar Plugin is a set of plugins for Django CMS that allow you to implement Google Calendar into your website.

![Django CMS Google Calendar Example](./docs/img/preview.png "Django CMS Google Calendar Example")

## Quick Start

1. Install the easy way, using pip:

        $ pip install djangocms-googlecalendar-plugin

2. Add "djangocms\_googlecalendar" to your INSTALLED\_APPS setting like this:

        INSTALLED_APPS = [
            ...
            'djangocms_googlecalendar-plugin',
        ]

3. Run `python manage.py migrate djangocms_googlecalendar-plugin` to create the plugin models.

## Running Tests

You can run tests by executing:

``` shell
  virtualenv venv -p python3
  source venv/bin/activate
  pip install -r tests/requirements.txt
  python setup.py test
```

## License

This project is licensed under GPL 3.0 - see [LICENSE](LICENSE.md) for details.

