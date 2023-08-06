from setuptools import setup, Extension
from setuptools.config import read_configuration
import numpy as np


config = read_configuration('./setup.cfg')

ext_hmm = Extension('chainsaddiction',
    sources = ['hmm/stats.c',
               'hmm/fwbw.c',
               'hmm/em.c',
               'hmm/hmm.c',
               'hmm/hmm_module.c'],
    include_dirs = ['include', np.get_include()])

setup(ext_modules = [ext_hmm])
