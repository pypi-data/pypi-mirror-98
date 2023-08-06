# -*- coding: utf-8 -*-

import os

from lintwork.config.config import ConfigFile
from lintwork.printer.printer import Printer
from lintwork.work.aosp.sdk import Sdk


class WorkException(Exception):
    def __init__(self, info):
        super().__init__(self)
        self._info = info

    def __str__(self):
        return self._info


class Work(object):
    def __init__(self, config):
        if config is None:
            raise WorkException("config invalid")
        self._config = config
        self._spec = config.config_file.get(ConfigFile.SPEC, None)
        if self._spec is None:
            raise WorkException("spec invalid")
        self._instance = self._instantiate()

    def _dump(self, data):
        printer = Printer()
        printer.run(data=data, name=self._config.output_file, append=False)

    def _instantiate(self):
        return {
            "aosp": {
                Sdk.__name__.lower(): Sdk(self._spec["aosp"][Sdk.__name__.lower()])
            }
        }

    def routine(self, project):
        if not isinstance(project, str) or not os.path.exists(project):
            raise WorkException("project invalid")
        buf = []
        for key in self._spec.keys():
            b = self._instance.get(key, {})
            for k in self._spec[key].keys():
                if k in b.keys():
                    buf.extend(b[k].run(project))
        if len(self._config.output_file) != 0:
            self._dump(buf)
        return buf
