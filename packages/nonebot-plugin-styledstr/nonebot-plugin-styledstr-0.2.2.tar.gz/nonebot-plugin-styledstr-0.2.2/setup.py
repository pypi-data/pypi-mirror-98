# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_styledstr']

package_data = \
{'': ['*']}

install_requires = \
['nonebot2>=2.0.0-alpha.11,<3.0.0', 'pyyaml>=5.4.1,<6.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-styledstr',
    'version': '0.2.2',
    'description': 'A Styled String Managing Plugin for Nonebot 2',
    'long_description': '# nonebot-plugin-styledstr\n\nNonebot 2 风格化字符串管理插件。\n\n[![time tracker](https://wakatime.com/badge/github/jks15satoshi/nonebot_plugin_styledstr.svg)](https://wakatime.com/badge/github/jks15satoshi/nonebot_plugin_styledstr)\n![PyPI](https://img.shields.io/pypi/v/nonebot-plugin-styledstr)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/nonebot-plugin-styledstr)\n[![CodeFactor](https://www.codefactor.io/repository/github/jks15satoshi/nonebot_plugin_styledstr/badge)](https://www.codefactor.io/repository/github/jks15satoshi/nonebot_plugin_styledstr)\n[![codecov](https://codecov.io/gh/jks15satoshi/nonebot_plugin_styledstr/branch/main/graph/badge.svg?token=8M2AHA8J3M)](https://codecov.io/gh/jks15satoshi/nonebot_plugin_styledstr)\n![GitHub](https://img.shields.io/github/license/jks15satoshi/nonebot_plugin_styledstr)\n\n> 由于本人 Python 水平低下，因此源码可能会令人不适，烦请谅解。\n\n## 介绍\n\n风格化字符串管理，或称字符串资源管理，即通过字符串标签来标识和获取一个字符串内容。设计初衷是用于灵活控制机器人的输出内容。\n\n### 字符串标签\n\n字符串标签用以在风格预设文件中唯一标识一个字符串内容。字符串标签使用点记法表示层级结构。举个例子，如果一个字符串在预设文件中的层级结构是这样的：\n\n````json\n{\n    "one": {\n        "sample": {\n            "structure": "something"\n        }\n    }\n}\n````\n\n那么这个字符串 `something` 的标签即为 `one.sample.structure`。\n\n### 风格预设\n\n该插件可以通过不同的风格预设来切换相同字符串标签的内容，通过这种方式，你可以为你的 ~~GLADoS~~ 机器人加装各种“人格核心”，或者让它变成一个“语言通”（即国际化）。使用方法可以参考 [使用用例](docs/usage.md#用例为bot增添多种不同的语言风格)。\n\n> 这也是为何我将这个插件命名为“风格化字符串管理”而非诸如“字符串资源管理”一类的名称（虽然这名称依旧很烂）。\n\n## 安装\n\n> 注意：Python 版本不应低于 3.9。\n\n### 使用 `nb-cli` 安装\n\n````shell\nnb plugin install nonebot-plugin-styledstr\n````\n\n### 使用 Poetry 安装\n\n````shell\npoetry add nonebot-plugin-styledstr\n````\n\n### 使用 `pip` 安装\n\n````shell\npip install nonebot-plugin-styledstr\n````\n\n## 使用准备\n\n### 配置\n\n> 注意：使用该插件前，请务必在项目中创建存放字符串资源的目录，并通过下面的配置项指定其为资源目录。关于如何设置插件配置项，参考 Nonebot 2 官方文档的 [基本配置](https://v2.nonebot.dev/guide/basic-configuration.html) 章节。\n\n该插件可通过在配置文件中添加如下配置项对部分功能进行配置。\n\n- **`STYLEDSTR_RESPATH`**：字符串资源目录，默认为当前工作目录（建议在 `bot.py` 文件中使用 `pathlib` 进行配置或使用绝对路径，若使用相对路径请确保工作目录为项目根目录。**建议手动配置。**）；\n- **`STYLEDSTR_PRESET`**：风格预设，默认为 `default`。\n\n### 为项目添加风格预设文件\n\n在字符串资源目录下根据需要创建风格预设文件。风格预设文件以 YAML 或 JSON 文件存储，并需确保文件名与风格预设配置一致，文件名对大小写不敏感。例如若风格预设配置为 `default`，则需要保证字符串资源目录下存在文件名为 `default` 的 YAML 或 JSON 文件。\n\n如果在资源目录下同时存在多个满足同一预设的文件（例如同时存在 `default.yaml` 与 `default.json`），则会按 `.json` > `.yaml` > `.yml` 的优先级读取文件。\n\n### 加载插件并获取解析器对象\n\n参考 Nonebot 2 官方文档的 [加载插件](https://v2.nonebot.dev/guide/loading-a-plugin.html) 章节，在项目中加载该插件。\n\n该插件可以使用 `import` 或通过 `nonebot.plugin.require` 获取解析器。\n\n使用 `import` 获取解析器需自行创建解析器对象：\n\n````python\n>>> from nonebot_plugin_styledstr import styledstr\n# 使用 Nonebot 初始化时读取的配置\n>>> parser = styledstr.Parser()\n# 或使用自定义配置\n>>> parser = styledstr.Parser(styledstr_preset=\'custom\')\n````\n\n使用 `require` 方式获取解析器时，若无需自定义配置可直接获取解析器对象：\n\n````python\n>>> from nonebot import require\n>>> parser = require(\'nonebot_plugin_styledstr\').parser\n````\n\n若需要自定义配置也可通过以下方式创建解析器对象：\n\n````python\n>>> from nonebot import require\n# 方式 1\n>>> import nonebot\n>>> config = nonebot.get_driver().config\n>>> config.styledstr_preset = \'custom\'\n>>> parser = require(\'nonebot_plugin_styledstr\').init(config)\n# 方式 2\n>>> from pathlib import Path\n>>> config = {\n...     \'styledstr_respath\': Path(\'path/to/respath\'),\n...     \'styledstr_preset\': \'custom\'\n... }\n>>> parser = require(\'nonebot_plugin_styledstr\').init(config)\n````\n\n## 使用\n\n参见 [使用用例](docs/usage.md) 了解该插件的用法。\n\n## 许可协议\n\n该项目以 MIT 协议开放源代码，详阅 [LICENSE](LICENSE) 文件。\n',
    'author': 'Satoshi Jek',
    'author_email': 'jks15satoshi@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
