# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['deepl_scraper_pp']

package_data = \
{'': ['*']}

install_requires = \
['get-ppbrowser>=0.1.2,<0.2.0',
 'linetimer>=0.1.4,<0.2.0',
 'logzero>=1.6.3,<2.0.0',
 'pyquery>=1.4.3,<2.0.0']

setup_kwargs = {
    'name': 'deepl-scraper-pp',
    'version': '0.1.1',
    'description': 'scrape deepl via pyppeteer',
    'long_description': '# deepl-scraper-pp\n[![tests](https://github.com/ffreemt/deepl-scraper-pyppeteer/actions/workflows/routine-tests.yml/badge.svg)][![python](https://img.shields.io/static/v1?label=python+&message=3.7%2B&color=blue)](https://img.shields.io/static/v1?label=python+&message=3.7%2B&color=blue)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)[![PyPI version](https://badge.fury.io/py/deepl-scraper-pp.svg)](https://badge.fury.io/py/deepl-scraper-pp)\n\nscrape deepl using pyppeteer, cross platform (Windows/MacOS/Linux) \n\n## Installation\n\n```bash\npip install deepl-scraper-pp\n# pip install deepl-scraper-pp  # upgrade to the latest version\n```\nor\n```bash\npoetry add deepl-scraper-pp\n# poetry add deepl-scraper-pp@latest  # upgrade to the latest version\n```\n\nor clone the repo (``git clone https://github.com/ffreemt/deepl-scraper-pyppeteer.git``) and install from it.\n\n## Usage\n\n## In an `ipython` session:\n\n```python\n\n# ipython\n\nfrom deepl_scraper_pp.deepl_tr import deepl_tr\n\nres = await deepl_tr("test me")\nprint(res)\n# \'考我 试探我 测试我 试探\'\n\nprint(await deepl_tr("test me", to_lang="de"))\n# mich testen mich prüfen testen Sie mich\n\ntext = "Pyppeteer has almost same API as puppeteer. More APIs are listed in the document"\nprint(await deepl_tr(text, to_lang="zh"))\n# Pyppeteer的API与puppeteer几乎相同。更多的API在文档中列出。\n```\n\n## in `python`\n\n```python\nimport asyncio\nfrom deepl_scraper_pp.deepl_tr import deepl_tr\n\nasync def main():\n    text1 = "test me"\n    text2 = "Pyppeteer has almost same API as puppeteer. More APIs are listed in the document"\n\n    coros = [deepl_tr(elm) for elm in [text1, text2]]\n    res = await asyncio.gather(*coros, return_exceptions=True)\n    print(res)\n\nloop = asyncio.get_event_loop()\ntry:\n    loop.run_until_complete(main())\nfinally:\n    loop.close()\n\n# output: [\'考我 试探我 测试我 试探\', \'Pyppeteer的API与puppeteer几乎相同。更多的API在文档中列出\']\n\n```\n\n## Disclaimer\n\nThe pypi is beta and will likely remain beta -- use it at your own peril.',
    'author': 'freemt',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ffreemt/deepl-scraper-pyppeteer',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
