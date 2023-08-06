import httpx
'''
from pathlib import Path
from typing import List, Optional
from PyInquirer import prompt

from ._config import TOMLConfig, JSONConfig
from ._pip import _call_pip_install, _call_pip_update, _call_pip_uninstall


def _get_plugin(package: Optional[str] = None , question: str) -> Optional[dict]:
    _package: str
    plugins = _get_plugins()
    plugin_exact = list(
        filter(
            lambda x: _package == x.id or _package == x.link or _package == x.name,
            plugins,
        )
    )
    if not plugin_exact:
        plugin = list(
            filter(
                lambda x: _package in x.id or _package in x.link or _package in x.name,
                plugins,
            )
        )
        if len(plugin) > 1:
            print_package_results(plugin)
            return
        elif len(plugin) != 1:
            return "Package not found!"
        else:
            plugin = plugin[0]
    else:
        plugin = plugin_exact[0]
    return plugin


def search_plugin(package: Optional[str] = None):
    _package: str
    if package is None:
        question = [
            {
                "type": "input",
                "name": "package",
                "message": "Plugin name you want to search?",
            }
        ]
        answers = prompt(question, qmark="[?]", style=list_style)
        if not answers or "package" not in answers:
            click.secho("Error Input! Missing 'package'", fg="red")
            return
        _package = answers["package"]
    else:
        _package = package
    plugins = _get_plugins()
    plugins = list(
        filter(lambda x: any(_package in value for value in x.dict().values()), plugins)
    )
    print_package_results(plugins)


def install_plugin(
    package: Optional[str] = None,
    file: str = "pyproject.toml",
    index: Optional[str] = None,
):
    plugin = _get_plugin(package, "Plugin name you want to install?")
    if not plugin:
        return
    status = _call_pip_install(plugin.link, index)
    if status == 0:  # SUCCESS
        try:
            if Path(file).suffix == ".toml":
                config = TOMLConfig(file)
            elif Path(file).suffix == ".json":
                config = JSONConfig(file)
            else:
                raise ValueError("Unknown config file format! Expect 'json' / 'toml'.")
            config.add_plugin(plugin.id)
        except Exception as e:
            click.secho(repr(e), fg="red")


def update_plugin(package: Optional[str] = None, index: Optional[str] = None):
    plugin = _get_plugin(package, "Plugin name you want to update?")
    if not plugin:
        return
    return _call_pip_update(plugin.link, index)


def uninstall_plugin(package: Optional[str] = None, file: str = "pyproject.toml"):
    plugin = _get_plugin(package, "Plugin name you want to uninstall?")
    if not plugin:
        return
    status = _call_pip_uninstall(plugin.link)
    if status == 0:  # SUCCESS
        try:
            if Path(file).suffix == ".toml":
                config = TOMLConfig(file)
            elif Path(file).suffix == ".json":
                config = JSONConfig(file)
            else:
                raise ValueError("Unknown config file format! Expect 'json' / 'toml'.")
            config.remove_plugin(plugin.id)
        except Exception as e:
            click.secho(repr(e), fg="red")
'''

def _get_plugins() -> list:
    res = httpx.get(
        "https://cdn.jsdelivr.net/gh/nonebot/nonebot2@master/docs/.vuepress/public/plugins.json"
    )
    return list(res.json())
