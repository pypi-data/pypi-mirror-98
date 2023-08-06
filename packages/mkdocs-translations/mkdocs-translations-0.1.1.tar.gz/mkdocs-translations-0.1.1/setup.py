# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mkdocs_translations']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.5.3,<0.6.0', 'mkdocs>=1.1.2,<2.0.0']

entry_points = \
{'mkdocs.plugins': ['translations = mkdocs_translations.plugin:Translator']}

setup_kwargs = {
    'name': 'mkdocs-translations',
    'version': '0.1.1',
    'description': 'Internationalization plugin for mkdocs',
    'long_description': "# Mkdocs translations plugin\n\nThis plugin is inspired by [mkdocs-static-i18n](https://github.com/ultrabug/mkdocs-static-i18n) plugin,\nbut it solves problem with tabs. With it, you can use nested documentation file structure.\n\nAlso, it's integrated with mkdocs-material theme features.\nSuch as [search](https://squidfunk.github.io/mkdocs-material/setup/setting-up-site-search/),\n[language switcher](https://squidfunk.github.io/mkdocs-material/setup/changing-the-language/),\nand [tabs](https://squidfunk.github.io/mkdocs-material/setup/setting-up-navigation/#navigation-tabs).\n\nFor example, with the following configuration:\n```yaml\n# Add this plugin in your mkdocs.yml\nplugins:\n  - translations:\n      default_language: ru\n      languages:\n        en: english\n        ru: русский\n```\n\nIt will turn this.\n```\ndocs\n├── Dir1\n│   ├── index.md\n│   ├── index.en.md\n│   ├── Theme1.md\n│   ├── Theme1.en.md\n│   ├── Theme2.md\n│   └── Theme2.en.md\n├── index.en.md\n├── index.md\n└── Dir2\n    ├── index.md\n    ├── index.en.md\n    ├── Theme1.md\n    └── Theme1.en.md\n```\n\nInto this:\n```\nsite\n├── 404.html\n├── index.html\n├── Dir1\n│   ├── Theme1\n│   │   └── index.html\n│   ├── index.html\n│   └── Theme2\n│       └── index.html\n├── Dir2\n│   ├── Theme1\n│   │   └── index.html\n│   └── index.html\n├── en\n│   ├── Dir1\n│   │   ├── Theme1\n│   │   │   └── index.html\n│   │   ├── index.html\n│   │   └── Theme2\n│   │       └── index.html\n│   ├── index.html\n│   └── Dir2\n│       ├── Theme1\n│       │   └── index.html\n│       └── index.html\n└── ru\n    ├── Dir1\n    │   ├── Theme1\n    │   │   └── index.html\n    │   ├── index.html\n    │   └── Theme2\n    │       └── index.html\n    ├── index.html\n    └── Dir2\n        ├── Theme1\n        │   └── index.html\n        └── index.html\n```\n",
    'author': 'Pavel Kirilin',
    'author_email': 'win10@list.ru',
    'maintainer': 'Pavel Kirilin',
    'maintainer_email': 'win10@list.ru',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
