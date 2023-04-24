"""Internal configuration of this alignment runner

deduces variables on first input and then holds them for
later access
"""

import os
import shutil
import json

class cfg :
    __instance = None
    def __init__(self, plot_list_file = None) :
        self._plot_list_file = plot_list_file
        with open(plot_list_file) as f :
            self._plot_list = json.load(f)

    def plot_list() :
        if cfg.__instance is None :
            raise ValueError('Attempting to access value before configuration.')
        return cfg.cfg()._plot_list

    def __str__(self) :
        return self._plot_list_file

    def cfg(**kwargs) :
        if cfg.__instance is None :
            cfg.__instance = cfg(**kwargs)
        return cfg.__instance
