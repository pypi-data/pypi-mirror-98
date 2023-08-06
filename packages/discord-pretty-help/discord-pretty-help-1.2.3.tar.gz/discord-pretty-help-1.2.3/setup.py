# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pretty_help']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['test = tests.test_discord_pretty_help:run']}

setup_kwargs = {
    'name': 'discord-pretty-help',
    'version': '1.2.3',
    'description': 'And nicer looking interactive help menu for discord.py',
    'long_description': '![version](https://img.shields.io/pypi/v/discord-pretty-help) ![python](https://img.shields.io/badge/python-3.6+-blue)\n\n# discord-pretty-help\n\nAn embed version of the built in help command for discord.py\n\nInspired by the DefaultHelpCommand that discord.py uses, but revised for embeds and additional sorting on individual pages that can be "scrolled" through with reactions.\n\n## Installation\n\n`pip install discord-pretty-help`\n\n## Usage\n\nExample of how to use it:\n\n```python\nfrom discord.ext import commands\nfrom pretty_help import PrettyHelp\n\nbot = commands.Bot(command_prefix="!", help_command=PrettyHelp())\n```\n\n### Added Optional Args\n\n- `active_time` - Set the time (in seconds) that the message will be active default is 30s\n- `color` - Set the default embed color\n- `ending_note` - Set the footer of the embed. Ending notes are fed a `commands.Context` (`ctx`) and a `PrettyHelp` (`help`) instance for more advanced customization.\n- `index_title` - Set the index page name default is *"Categories"*\n- `navigation` - Set the emojis that will control the help menu. Uses a `pretty_help.Navigation()` instance.\n- `no_category` - Set the name of the page with commands not part of a category. Default is "*No Category*"\n- `sort_commands` - Sort commands and categories alphabetically\n- `show_index` - Show the index page or not\n\n\nBy default, the help will just pick a random color on every invoke. You can change this using the `color` argument:\n\n```python\nimport discord\nfrom discord.ext import commands\nfrom pretty_help import PrettyHelp, Navigation\n\n\n\nbot = commands.Bot(command_prefix="!")\n\n# custom ending note using the command context and help command formatters\nending_note = "The ending not from {ctx.bot.user.name}\\nFor command {help.clean_prefix}{help.invoked_with}"\n\n# ":discord:743511195197374563" is a custom discord emoji format. Adjust to match your own custom emoji.\nnav = Navigation(":discord:743511195197374563", "👎", "\\U0001F44D")\ncolor = discord.Color.dark_gold()\n\nbot.help_command = PrettyHelp(navigation=nav, color=color, active_time=5, ending_note=ending_note)\n\n```\n\nThe basic `help` command will break commands up by cogs. Each cog will be a different page. Those pages can be navigated with\nthe arrow embeds. The message is unresponsive after 30s of no activity, it\'ll remove the reactions to let you know.\n\n![example](https://raw.githubusercontent.com/stroupbslayen/discord-pretty-help/master/images/example.gif)\n\n# Changelog\n\n## [1.2.3]\n- Allowed for more customized ending notes.\n\n\n# Notes:\n\n- discord.py must already be installed to use this\n- `manage-messages` permission is recommended so reactions can be removed automatically\n\n',
    'author': 'StroupBSlayen',
    'author_email': '29642143+stroupbslayen@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/stroupbslayen/discord-pretty-help',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
