# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cookiebanner', 'cookiebanner.templatetags']

package_data = \
{'': ['*'],
 'cookiebanner': ['locale/de/LC_MESSAGES/*', 'templates/cookiebanner/*']}

install_requires = \
['django>=1.11']

setup_kwargs = {
    'name': 'django-cookiebanner',
    'version': '0.2.4',
    'description': '',
    'long_description': '# Django-Cookiebanner\n\n## Installation\n\n`pip install django-cookiebanner`\n\n\n## Usage\n\n* Add `cookiebanner` to your `INSTALLED_APPS`\n\n* in your settings (`settings.py`) specify the different Cookie Groups:\n```python\nfrom django.utils.translation import ugettext_lazy as _\n\nCOOKIEBANNER = {\n    "title": _("Cookie settings"),\n    "header_text": _("We are using cookies on this website. A few are essential, others are not."),\n    "footer_text": _("Please accept our cookies"),\n    "footer_links": [\n        {\n            "title": _("Imprint"),\n            "href": "/imprint"\n        },\n        {\n            "title": _("Privacy"),\n            "href": "/privacy"\n        },\n    ],\n    "groups": [\n        {\n            "id": "essential",\n            "name": _("Essential"),\n            "description": _("Essential cookies allow this page to work."),\n            "cookies": [\n                {\n                    "pattern": "cookiebanner",\n                    "description": _("Meta cookie for the cookies that are set."),\n                },\n                {\n                    "pattern": "csrftoken",\n                    "description": _("This cookie prevents Cross-Site-Request-Forgery attacks."),\n                },\n                {\n                    "pattern": "sessionid",\n                    "description": _("This cookie is necessary to allow logging in, for example."),\n                },\n            ],\n        },\n        {\n            "id": "analytics",\n            "name": _("Analytics"),\n            "optional": True,\n            "cookies": [\n                {\n                    "pattern": "_pk_.*",\n                    "description": _("Matomo cookie for website analysis."),\n                },\n            ],\n        },\n    ],\n}\n```\n\n* In your base template add the banner and the conditionals:\n```djangotemplate\n{% load cookiebanner %}\n...\n<body>\n{% cookiebanner_modal %}\n...\n\n\n{% cookie_accepted \'analytics\' as cookie_analytics %}\n{% if cookie_analytics %}\n<script>... javascript for matomo ...</script>\n{% endif %}\n</body>\n```\n\n\n',
    'author': 'Andreas Nüßlein',
    'author_email': 'andreas@nuessle.in',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
