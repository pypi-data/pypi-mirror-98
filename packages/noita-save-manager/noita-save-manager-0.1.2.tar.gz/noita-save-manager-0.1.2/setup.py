# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['noita_save_manager']

package_data = \
{'': ['*']}

install_requires = \
['PySimpleGUI>=4.34.0,<5.0.0', 'psutil>=5.8.0,<6.0.0']

entry_points = \
{'console_scripts': ['noita_save_manager = '
                     'noita_save_manager.save_manager:main']}

setup_kwargs = {
    'name': 'noita-save-manager',
    'version': '0.1.2',
    'description': 'Noita Save Manager, allows for backup and restoring of save files',
    'long_description': "# Noita save manager\n\nSmall save-game manager written for usage with Noita works in Linux or Windows.\n\n# Screenshot\n\n![Noita save manager](https://raw.githubusercontent.com/mcgillij/noita_save_manager/main/images/noita_save_manager.png)\n\n# Features\n* Check to see if Noita is running\n* Backup active save\n* Restore from backup\n* Non destructive\n\n# Non Destructive\nCurrently you cannot use this tool to delete / remove saves or backups.\nIt will always create a backup in the Noita folder prior to restoring. So it won't overwrite / delete anything.\n\n# Installing with Pip, Pipenv or Poetry\n\n``` bash\npip install noita-save-manager\npipenv install noita-save-manager\npoetry add noita-save-manager\n```\n# Running\n\n``` bash\nnoita_save_manager\n```\n\n## Pre-Built Windows client\n\nYou can grab the latest release https://github.com/mcgillij/noita_save_manager/releases/download/0.1.0/save_manager_0.1.0.zip\n\n# Building from source\n\nIf you want to build your own binary/ source distribution / wheel, you can use the following steps. Uses **poetry** for dependency management.\n\n``` bash\npoetry install\npoetry run pyinstaller -F --noconsole src/noita_save_manager/save_manager.py\n```\n\nThis will plop out a binary for you in the `dist/` folder.\n",
    'author': 'mcgillij',
    'author_email': 'mcgillivray.jason@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mcgillij/noita_save_manager',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
