# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['itils']

package_data = \
{'': ['*']}

install_requires = \
['Wand>=0.6.6,<0.7.0', 'halo>=0.0.31,<0.0.32', 'plac>=1.3.2,<2.0.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=3.0,<4.0']}

entry_points = \
{'console_scripts': ['itils = itils.cli:console_scripts_main']}

setup_kwargs = {
    'name': 'itils',
    'version': '0.1.0',
    'description': 'A Python CLI for transforming images.',
    'long_description': '# itils\n\n[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\nA Python CLI for transforming images.\n\nPowered by [plac](https://github.com/ialbert/plac) (CLI), [Wand](https://github.com/emcconville/wand) (images), and [halo](https://github.com/ManrajGrover/halo) (spinners).\n\n## Usage\n\n### Interactive mode\n\n```text\nitils -i\n```\n\nRun `quit` to close `itils`.\n\n### `gslide` subcommand\n\n<!-- poetry run itils gslide -h | pbcopy -->\n\n```text\nusage: itils gslide [-h] [-r PCT] input_img\n\nResize an image to be smaller than 25 megapixels for Google Slides.\nThe image can be resized using an explicit percentage as well.\n\npositional arguments:\n  input_img             The path to the image to be transformed.\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -r PCT, --resize PCT  The (explicit) percentage value (e.g., 70) to scale\n                        both width and height. Values less than 100 reduce the\n                        image size.\n```\n\n## Development\n\n1. `poetry install`\n2. `poetry shell`\n\n## Notes\n\n- `convert image.png -resize 70% smaller_image.png` ([documentation](http://www.imagemagick.org/script/convert.php)).\n- ["Improve Windows Support"](https://github.com/manrajgrover/halo/issues/5) (open) issue (halo).\n',
    'author': 'João Palmeiro',
    'author_email': 'joaommpalmeiro@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/joaopalmeiro/itils',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
