# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['incipit']

package_data = \
{'': ['*']}

install_requires = \
['PyPDF4>=1.27.0,<2.0.0',
 'click>=7.1.2,<8.0.0',
 'click_help_colors>=0.9,<0.10',
 'loguru>=0.5.3,<0.6.0',
 'opencv-python>=4.5.1,<5.0.0',
 'pillow>=8.1.2,<9.0.0']

entry_points = \
{'console_scripts': ['incipit = incipit.cli:main']}

setup_kwargs = {
    'name': 'incipit',
    'version': '2021.3.2',
    'description': 'CLI and Python package to extract systems of staves from musical scores.',
    'long_description': '# `incipit` — extract systems of staves from musical scores\n\nThis command-line tool (and Python package) allows for the easy extraction of\nsystems of staves from musical scores. In particular, it makes it easy to extract\nthe first system of any musical score that is in B&W format, and has a noiseless\nenough background\n\nThis tool was built to automatically generate incipits for large sets of scores,\nlike those downloaded from IMSLP. It was specifically built to create an index\nof the 555 keyboard sonatas by Domenico Scarlatti, in a related project.\n\n## Installation\n\nThe package is available on PyPI as `incipit` and so is available the usual way, i.e.,\n```\nsudo pip install incipit\n```\nIn addition to the Python package, this should also install a CLI binary that is\nrunnable, called `incipit`.\n\n## Usage\n\n```\nUsage: incipit [OPTIONS] INPUT\n\n  Extract the first (or any) system of staves from a black-and-white modern\n  musical score, either available as an image file or PDF. For instance,\n\n      $ incipit -o "555-incipit.png" ./input/pdf/555-gilbert.pdf\n\n  will extract the first system of staves of the sheet music\n  `555-gilbert.pdf\' as the image `555-incipit.png`. And,\n\n      $ incipit --output "1__{}.png" -# \'0,-1\' ./input/pdf/1-gilbert.pdf\n\n  will extract the first and last systems of staves of `1-gilbert.pdf` and\n  output these as the images `1__0.png\' (first system) and `1__10.png\' (last\n  system).\n\nOptions:\n  -a, --audit                   Visualize system detection across document\n  -c, --count                   Output number of detected systems\n  -p, --pages TEXT              List of pages to process (e.g., \'0\', \'0,-1\')\n  -#, --systems TEXT            List of systems to extract (e.g., \'0\', \'0,-1\')\n  -h, --height-threshold FLOAT  % of height threshold for system detection\n  -w, --width-threshold FLOAT   % of width threshold for system detection\n  -o, --output TEXT             Output file pattern\n  -v, --verbose                 Print debug information\n  --version                     Show the version and exit.\n  --help                        Show this message and exit.\n```',
    'author': 'Jérémie Lumbroso',
    'author_email': 'lumbroso@cs.princeton.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jlumbroso/incipit',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
