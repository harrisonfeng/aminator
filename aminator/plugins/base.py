# -*- coding: utf-8 -*-

#
#
#  Copyright 2013 Netflix, Inc.
#
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.
#
#

"""
aminator.plugins.base
=====================
Base class(es) for plugin implementations
"""
import abc
import logging
import os

from aminator.config import PluginConfig


__all__ = ()
log = logging.getLogger(__name__)


class BasePlugin(object):
    """ Base class for plugins """

    __metaclass__ = abc.ABCMeta

    def __init__(self, *args, **kwargs):
        self._enabled = True

    @property
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, enable):
        self._enabled = enable

    @property
    def entry_point(self):
        return self._entry_point

    @property
    def name(self):
        return self._name

    @abc.abstractmethod
    def configure(self, config, parser):
        """ Configure the plugin and contribute to command line args """
        log.debug("Configuring plugin {0} for entry point {1}".format(self.name, self.entry_point))
        self.config = config
        self.parser = parser
        self.load_plugin_config()

    def load_plugin_config(self):
        entry_point = self.entry_point
        name = self.name
        key = '.'.join((entry_point, name))

        plugin_conf_dir = os.path.join(self.config.config_root,
                                       self.config.plugins.config_root)
        plugin_conf_files = (
            os.path.join(plugin_conf_dir, '.'.join((key, 'yml'))),
        )

        self.config.plugins[key] = PluginConfig.from_defaults(entry_point, name)
        self.config.dict_merge(self.config.plugins[key],
                               PluginConfig.from_files(plugin_conf_files))
