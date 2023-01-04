# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/00_core.ipynb.

# %% auto 0
__all__ = ['IN_IPYTHON', 'StreamlitPatcher']

# %% ../nbs/00_core.ipynb 2
import logging 
import time
import typing as tp

import streamlit
from fastcore.basics import in_ipython, listify, noop
from fastcore.test import test_fail
from IPython.utils.capture import capture_output


# %% ../nbs/00_core.ipynb 3
# module obljects that we will be importing
IN_IPYTHON = in_ipython()

# %% ../nbs/00_core.ipynb 5
import inspect

class StreamlitPatcher:
    """class to patch streamlit functions for displaying content in jupyter notebooks"""
    def __init__(self):
      pass

    def patch(self):
        """
        Registers the current `tqdm` class with
            streamlit.
            ( write 
              markdown

            )
            """

        pass

        # patch streamlit

        # patch stqdm

    def echo(self):
      print("hello")

    @property
    def methods(self):
      for attr in dir(self):
          if attr == "methods":
            continue

          m = getattr(self, attr)
          if inspect.ismethod(m) and not attr.startswith("_"):
              print(attr)

    @staticmethod
    def _get_streamlit_methods():
      """get all streamlit methods"""
      return [attr for attr in dir(streamlit) if not attr.startswith("_")]
