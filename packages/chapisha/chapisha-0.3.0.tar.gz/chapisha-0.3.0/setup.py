# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['chapisha', 'chapisha.create', 'chapisha.helpers', 'chapisha.models']

package_data = \
{'': ['*'],
 'chapisha.helpers': ['data/css/*',
                      'data/fonts/*',
                      'data/images/*',
                      'data/xhtml/*']}

install_requires = \
['Pillow>=8.1.2,<9.0.0',
 'beautifulsoup4>=4.9.3,<5.0.0',
 'epubcheck>=0.4.2,<0.5.0',
 'filetype>=1.0.7,<2.0.0',
 'lxml>=4.6.2,<5.0.0',
 'pydantic>=1.7.3,<2.0.0',
 'pypandoc>=1.5,<2.0',
 'regex>=2020.11.13,<2021.0.0',
 'tomlkit>=0.7.0,<0.8.0']

setup_kwargs = {
    'name': 'chapisha',
    'version': '0.3.0',
    'description': 'Chapisha: docx to standards-compliant epub3 conversion',
    'long_description': "# Chapisha: docx to standards-compliant epub3 conversion\n\n[![Documentation Status](https://readthedocs.org/projects/chapisha/badge/?version=latest)](https://chapisha.readthedocs.io/en/latest/?badge=latest)\n[![Build Status](https://travis-ci.com/whythawk/chapisha.svg?branch=main)](https://travis-ci.com/whythawk/chapisha)\n\n## What is it?\n\n**Chapisha** provides an intuitive method for converting a well-formatted Microsoft Word `.docx` file into a \nstandards-compliant EPUB3 ebook.\n\nThere are only a small number of steps required to create your `.epub`, and **Chapisha** will provide an appropriate\nstylesheet and take care of document structure:\n\n- Set the working directory where you want to create your `.epub`,\n- Define and validate the metadata required for the creative work,\n- Copy the `docx` file to import into the working directory,\n- Copy the cover image to import into the working directory,\n- Define and add any contributors, such as cover artist,\n- Define your creative work's publication rights,\n- Add in an optional dedication,\n- Build your creative work as an EPUB3 standards-compliant ebook.\n\n[Read the docs](https://chapisha.readthedocs.io/en/latest/)\n\n## Why use it?\n\n**Chapisha** is easy-to-use, quick, and fits into your workflow.\n\nThere are a multitude of `.epub` conversion tools but few that support the day-to-day workflow and tools used by most\njobbing writers: Microsoft Word.\n\n**Chapisha** draws on [Pandoc](https://pandoc.org/epub.html) for document conversion and ebook creation, adding a \nsimple, stateless Python frame around it, which means you can also include it in a web application.\n\n## Installation and dependencies\n\nYou'll need at least Python 3.9, then:\n\n    pip install chapisha\n\nYou will also need to install `Pandoc` and `Java`:\n\n    sudo apt install pandoc default-jre\n\n## Changelog\n\nThe version history can be found in the [changelog](https://github.com/whythawk/chapisha/blob/master/CHANGELOG).\n\n## Background\n\n**Chapisha** was created to serve my needs as both a formally, and self-published, author. I have written two \nnovels - [Lament for the fallen](https://gavinchait.com/lament-for-the-fallen/) and \n[Our memory like dust](https://gavinchait.com/our-memory-like-dust/) - and a number of \n[short stories](https://gavinchait.com/). These works are available to read online, and to download\nas an ebook.\n\n[Chapisha](https://glosbe.com/sw/en/-chapisha) is the *Swahili* word for 'publish' or 'post'.\n\n## Licence\n[BSD 3](LICENSE)\n\nOther licenced elements:\n\n- [Samara logo](chapisha/helpers/images/logo.png) is copyright [Whythawk](https://whythawk.com) and [Qwyre](https://gavinchait.com).\n- [Cover photo](tests/data/cover.jpg) is copyright Rodd Halstead, licenced under commercial terms to Whythawk, and used here for test purposes.\n- [Usan Abasi's Lament](https://gavinchait.com/usan-abasis-lament/) is copyright Gavin Chait, licenced [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) and used here for test purposes.",
    'author': 'Gavin Chait',
    'author_email': 'gchait@whythawk.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/whythawk/chapisha',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9.1,<4.0.0',
}


setup(**setup_kwargs)
