# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_manager']

package_data = \
{'': ['*']}

install_requires = \
['nonebot-adapter-cqhttp>=2.0.0a11.post2,<3.0.0',
 'nonebot2>=2.0.0-alpha.11,<3.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-manager',
    'version': '0.3.0.post3',
    'description': 'Nonebot Plugin Manager base on import hook',
    'long_description': '# Nonebot Plugin Manager\n\n*适用于 [nonebot2](https://github.com/nonebot/nonebot2) 以及 [go-cqhttp](https://github.com/Mrs4s/go-cqhttp) 的插件管理器*\n\n[![License](https://img.shields.io/github/license/Jigsaw111/nonebot_plugin_manager)](LICENSE)\n![Python Version](https://img.shields.io/badge/python-3.7.3+-blue.svg)\n![NoneBot Version](https://img.shields.io/badge/nonebot-2.0.0a11+-red.svg)\n![Pypi Version](https://img.shields.io/pypi/v/nonebot-plugin-manager.svg)\n\n### 安装\n\n* 使用nb-cli（推荐）  \n\n```bash\nnb plugin install nonebot_plugin_manager\n```\n\n* 使用poetry\n\n```bash\npoetry add nonebot_plugin_manager\n```\n\n### 开始使用\n\n**使用前请先确保命令前缀设置为空，否则请在以下命令前加上自己的命令前缀 (默认为 `/` )。**\n\n`npm list` 查看插件列表\n\n`npm block 插件名...` 屏蔽插件 （仅群管及超级用户可用）\n\n`npm unblock 插件名...` 启用插件 （仅群管及超级用户可用）\n\n`-a, --all` 可选参数，全选插件 （仅群管及超级用户可用）\n\n`-d, --default` 可选参数，管理默认设置 （仅超级用户可用）\n\n`-g, --group group_id` 可选参数，管理群设置（仅超级用户可用）\n\n### TO DO\n\n- [x] 分群插件管理\n- [ ] 调用 nb-cli 安装卸载插件\n\n<details>\n<summary>展开更多</summary>\n\n### 原理\n\n使用 `run_preprocessor` 装饰器，在 Matcher 运行之前检测其所属的 Plugin 判断是否打断。\n\n事实上 Nonebot 还是加载了插件，所以只能算是**屏蔽**而非**卸载**。\n\n### Bug\n\n- [ ] 无法停用 Matcher 以外的功能（也就是说无法屏蔽主动发消息的插件，例如 Harukabot ）。\n- [x] 目前任何人都可以管理插件\n\n</details>',
    'author': 'Jigsaw',
    'author_email': 'j1g5aw@foxmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Jigsaw111/nonebot_plugin_manager',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.3,<4.0.0',
}


setup(**setup_kwargs)
