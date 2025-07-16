"""
NOTE: This module is considered private and is subject to abrupt breaking
changes without prior announcement. Please do not use it directly.
"""

import importlib
import logging

log = logging.getLogger(__name__)


def load_client_plugins(client, plugins):
    for plugin_name, module_name in plugins.items():
        log.debug(
            "Importing client plugin %s from module %s",
            plugin_name,
            module_name,
        )
        try:
            module = importlib.import_module(module_name)
            module.initialize_client_plugin(client)
        except ModuleNotFoundError:
            log.debug(
                "Failed to locate the following plugin module: %s.",
                plugin_name,
            )
        except Exception as e:
            log.debug(
                "Error raised during the loading of %s: %s", plugin_name, e
            )
