from sd_utils.plugins.plugin_base import PluginBase
from typing import ClassVar


class PluginManager:
    def __init__(self):
        self._plugins = {}

    def register(self, name: str, **kwargs):
        """
        decorator for registering a plugin to this instance of a
        plugin manager
        """

        def decorator(plugin: ClassVar[PluginBase]):
            if name in self._plugins:
                raise ValueError(f"Plugin with name [{name}] already exists")

            class Wrapper:
                def __init__(self, plugin):
                    self.name = name
                    self.plugin = plugin

            w = Wrapper(plugin(**kwargs))

            self._plugins[name] = w
            w.plugin.on_register()

            return w

        return decorator

    def run(self, name: str):
        """
        runs a given plugin
        """

        to_run = None
        for plugin_name, wrapper in self._plugins.items():
            if name == plugin_name:
                to_run = wrapper
            try:
                wrapper.plugin.on_search()
            except NotImplementedError:
                # just skip if its not implemented
                pass

        if to_run is None:
            raise ValueError(f"Unable to find plugin with name [{name}]")

        to_run.plugin.on_find()
