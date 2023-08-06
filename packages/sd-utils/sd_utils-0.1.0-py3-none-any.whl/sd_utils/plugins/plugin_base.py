from typing import Any


class PluginBase:
    """
    """

    def __init__(self, **kwargs):
        """
        """
        pass

    def on_register(self):
        """
        runs when this plugin is registered with
        the plugin manager
        """
        raise NotImplementedError

    def on_search(self, data: Any = None):
        """
        runs when the manager begins a query for
        any plugin.
        """
        raise NotImplementedError

    def on_find(self, data: Any = None):
        """
        runs when the manager specifically queries this plugin
        """
        raise NotImplementedError
