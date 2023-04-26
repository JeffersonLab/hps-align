"""Internal configuration of this alignment runner

deduces variables on first input and then holds them for
later access
"""

import os
import shutil
import json


class cfg:
    __instance = None

    def __init__(self,
                 input_files=[],
                 legend_labels=[],
                 out_dir=None,
                 html=True,
                 is2016=False,
                 ext='.png',
                 plot_list_file=None):
        self._plot_list_file = plot_list_file
        with open(plot_list_file) as f:
            self._plot_list = json.load(f)
        self.input_files = input_files
        self.legend_labels = legend_labels
        self.out_dir = out_dir
        self.html = html
        self.is2016 = is2016
        self.ext = ext

    def plot_list(name = None):
        if cfg.__instance is None:
            raise ValueError(
                'Attempting to access value before configuration.')
        if name is None :
            # provide whole plot list
            return cfg.cfg()._plot_list
        elif name not in cfg.cfg()._plot_list :
            raise ValueError(
                f'{name} not a category in plot listing.')
        else :
            # provide currently-configured year of that category
            year = '2016' if self.is2016 else 'not2016'
            return cfg.cfg()._plot_list[name][year]

    def make_plotter(cls, **kwargs):
        if cfg.__instance is None:
            raise ValueError(
                'Attempting to access value before configuration.')
        return cls(
            infile_names=cfg.cfg().input_files,
            legend_names=cfg.cfg().legend_labels,
            outdir=cfg.cfg().out_dir,
            do_HTML=cfg.cfg().html,
            oFext=cfg.cfg().ext,
            **kwargs
        )

    def __str__(self):
        return self._plot_list_file

    def cfg(**kwargs):
        if cfg.__instance is None:
            cfg.__instance = cfg(**kwargs)
        return cfg.__instance
