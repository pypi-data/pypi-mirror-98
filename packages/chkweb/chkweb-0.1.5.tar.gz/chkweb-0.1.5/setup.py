# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['chkweb']
install_requires = \
['fire>=0.4.0,<0.5.0', 'prettyconf>=2.2.1,<3.0.0', 'requests>=2.25.1,<3.0.0']

entry_points = \
{'console_scripts': ['chkweb = chkweb:main']}

setup_kwargs = {
    'name': 'chkweb',
    'version': '0.1.5',
    'description': 'A very simple web crawler and checker',
    'long_description': '## ChkWeb\n\nThis is a very simple web crawler to check the public webpages\nin a webserver.\n\nto use, call the subcommand start with the URL to crawl:\n\n    chkweb start http://localhost/\n\nThis will create a sqlite3 database ``pages.db`` whith the urls being\ndetected by the spyder. It also checks this first page and add all the locals\nlinks to the database as pending url to be checked. Now you can run:\n\n    chkweb advance\n\nto continue the crawling process. This is going to take at most 10\npending url and repeat the process with each of then. You can define the maximun\namount of new urls to be checked setting the environment variable `CHKWEB_ADVANCE_LIMIT` or\n setting the `--limit` command line option, like in this example:\n\n    chkweb advance --limit 1000\n\n### Checking process status\n\nYou can check the current process status with the subcommand `status`, like this:\n\n    chkweb status\n\n### Logs\n\nA log file is stored in ``logs/chklog.log``. You can change the\nlog level either in the settings file or declaring a environment variable\nnamed ``CHKWEB_LOG_LEVEL`` to the desired level. It is set to ``ERROR``\nby default.\n\n### TODO things\n\n- Add a plugin system to perform custom checks\n\n- Add a new subcommand to make the tests from a given list of urls\n\n- Add an option to select the name and path of the database file. Alos include\n  in the `settings.py` file.\n\n### DONE things\n\n- add an option in the `advance` command to set the number of pages\n  being analized in every call. Set to 0 to indicate continue until all the\n  pages are analized [DONE 0.1.4]\n\n- logs stored in some other location [DONE 0.1.2]\n- Subcommand list to list the URLs in the database [DONE 0.1.2]\n- Subcommand init to delete the database and start a new crawl proces [DONE 0.1.2]\n- subcommand run to get a URL form the pending list and check it [DONE 0.1.2]\n',
    'author': 'Juan Ignacio Rodriguez de Leon',
    'author_email': 'euribates@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/euribates/chkweb.git',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
