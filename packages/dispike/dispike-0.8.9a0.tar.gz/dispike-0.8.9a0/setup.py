# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dispike',
 'dispike.errors',
 'dispike.eventer_helpers',
 'dispike.followup',
 'dispike.followup.storage',
 'dispike.helper',
 'dispike.middlewares',
 'dispike.models',
 'dispike.models.discord_types',
 'dispike.register',
 'dispike.register.models']

package_data = \
{'': ['*']}

install_requires = \
['PyNaCl>=1.4.0,<2.0.0',
 'async-timeout>=3.0.1,<4.0.0',
 'fastapi>=0.63.0,<0.64.0',
 'httpx>=0.16.1,<0.17.0',
 'loguru>=0.5.3,<0.6.0',
 'pydantic>=1.7.3,<2.0.0',
 'typing-extensions>=3.7.4,<4.0.0',
 'uvicorn>=0.13.2,<0.14.0']

setup_kwargs = {
    'name': 'dispike',
    'version': '0.8.9a0',
    'description': 'library for interacting with discord slash commands via an independently hosted server. Powered by FastAPI',
    'long_description': '# dispike\n\n***\n[![codecov](https://codecov.io/gh/ms7m/dispike/branch/master/graph/badge.svg?token=E5AXLZDP9O)](https://codecov.io/gh/ms7m/dispike) ![Test Dispike](https://github.com/ms7m/dispike/workflows/Test%20Dispike/badge.svg?branch=master) [![PyPi Link](https://img.shields.io/badge/Available%20on%20PyPi-Dispike-blue?logo=pypi&link=%22https://pypi.org/project/dispike%22)](http://pypi.org/project/dispike) ![PyPiVersion](https://img.shields.io/badge/dynamic/json?color=blue&label=PyPi%20Version&query=%24.info.version&url=https%3A%2F%2Fpypi.org%2Fpypi%2Fdispike%2Fjson) [![Docs](https://img.shields.io/badge/Docs-Available-lightgrey?link=https://dispike.ms7m.me/)\n](http://dispike.ms7m.me)\n\n***\n\n\n\nan *extremely* early WIP library for easily creating REST-based webhook bots for discord using the new Slash Commands feature.\n\nPowered by [FastAPI](https://github.com/tiangolo/fastapi).\n\n\n***\n\n\n## Install\n\n```\npip install dispike\n```\n\n## Learn more\n- Read documentation [here](https://dispike.ms7m.me)\n- See an example bot [here](https://github.com/ms7m/dispike-example)\n\n## Example Code\n\n```python\n\nfrom dispike import Dispike\nbot = Dispike(..)\n\n@bot.interaction.on("stock"):\nasync def handle_stock_request(stockticker: str, ctx: IncomingDiscordInteraction) -> DiscordResponse:\n  get_price = function(stockticker...)\n  \n  embed=discord.Embed()\n  embed.add_field(name="Stock Price for {stockticker}.", value="Current price is {get_price}", inline=True)\n  embed.set_footer(text="Request received by {ctx.member.user.username}")\n  return DiscordResponse(embed=embed)\n\n\n\nif __name__ == "__main__":\n    bot.run()\n```\n\n\n\n## Caveats\n\n- Python 3.6+\n- Does not speak over the discord gateway. [discord-py-slash-command is what you are looking for.](https://github.com/eunwoo1104/discord-py-slash-command)\n\n<details><summary>Resolved Caveats</summary>\n<p>\n\n- ~~Does not handle registring new commands.~~\n- ~~Does not handle anything other then string responses. (However you are free to return any valid dict in your handler.)~~\n- ~~Not on PyPi~~\n- ~~Handling followup messages.~~\n\n</p>\n</details>\n\n\n\n\n# Development\n\nHelp is wanted in mantaining this library. Please try to direct PRs to the ``dev`` branch, and use black formatting (if possible).\n\n![Test Dispike](https://github.com/ms7m/dispike/workflows/Test%20Dispike/badge.svg?branch=dev)\n\n# Special Thanks\n- [Squidtoon99](https://github.com/Squidtoon99)\n',
    'author': 'Mustafa Mohamed',
    'author_email': 'ms7mohamed@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ms7m/dispike',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
