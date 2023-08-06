import pkg_resources

from kikyo.analytic import Analytic
from kikyo.datahub import DataHub
from kikyo.objstore import ObjStore
from kikyo.search import Search
from kikyo.settings import Settings


class Kikyo:
    datahub: DataHub
    objstore: ObjStore
    search: Search
    analytic: Analytic

    settings: Settings

    def __init__(self, _settings: dict = None, **kwargs):
        self.settings = Settings(_settings)
        self.settings.merge(kwargs)
        self._init()

    def _init(self):
        self._init_plugins()

    def _init_plugins(self):
        plugins = {
            entry_point.name: entry_point.load()
            for entry_point in pkg_resources.iter_entry_points('kikyo.plugins')
        }

        active_plugins = self.settings.getlist('active_plugins')
        if active_plugins:
            active_plugins = set(active_plugins)
            for name in list(plugins.keys()):
                if name not in active_plugins:
                    del plugins[name]

        for name, plugin in plugins.items():
            if hasattr(plugin, 'configure_kikyo'):
                plugin.configure_kikyo(self)
