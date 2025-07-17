"""
NOTE: This module is considered private and is subject to abrupt breaking
changes without prior announcement. Please do not use it directly.
"""

import importlib
import logging
import os
from contextvars import ContextVar
from dataclasses import dataclass
from typing import Optional

log = logging.getLogger(__name__)


@dataclass
class PluginContext:
    """
    Encapsulation of plugins tracked within the `_plugin_context` context variable.
    """

    plugins: Optional[str] = None


_plugin_context = ContextVar("_plugin_context")


def get_plugin_context():
    """Get the current `_plugin_context` context variable if set, else None."""
    return _plugin_context.get(None)


def set_plugin_context(ctx):
    """Set the current `_plugin_context` context variable."""
    token = _plugin_context.set(ctx)
    return token


def reset_plugin_context(token):
    """Reset the current `_plugin_context` context variable."""
    _plugin_context.reset(token)


def get_botocore_plugins():
    context = get_plugin_context()
    if context is not None:
        plugins = context.plugins
        if plugins is not None:
            return plugins
    return os.environ.get('BOTOCORE_EXPERIMENTAL__PLUGINS')


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
