# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/01_core.ipynb.

# %% auto 0
__all__ = ['IN_IPYTHON', 'tqdm', 'StreamlitPatcher']

# %% ../nbs/01_core.ipynb 2
import functools
import json
import logging
import time
import typing as tp
from datetime import datetime

import IPython.display
import ipywidgets as widgets
import pandas as pd
import streamlit as st
from fastcore.basics import in_ipython, listify, noop, patch, patch_to
from fastcore.test import test_eq, test_fail
from IPython.utils.capture import capture_output
from nbdev.showdoc import show_doc

from .utils import test_md_output

# %% ../nbs/01_core.ipynb 3
from logging import getLogger

logger = getLogger(__name__)

# %% ../nbs/01_core.ipynb 4
# module obljects that we will be importing
IN_IPYTHON = in_ipython()

# %% ../nbs/01_core.ipynb 7
if IN_IPYTHON:
    from tqdm.notebook import tqdm
else:
    from stqdm import stqdm as tqdm

tqdm = tqdm  # make this available in the module namespace

# %% ../nbs/01_core.ipynb 8
class StreamlitPatcher:
    """class to patch streamlit functions for displaying content in jupyter notebooks"""

    def __init__(self):
        self.is_registered: bool = False
        self.registered_methods: tp.Set[str] = set()

    def jupyter(self, verbose: bool = False):
        """patches streamlit methods to display content in jupyter notebooks"""
        # patch streamlit methods from MAPPING property dict
        for method_name, wrapper in self.MAPPING.items():
            self._wrap(method_name, wrapper, verbose=verbose)

        self.is_registered = True

    @staticmethod
    def _get_streamlit_methods():
        """get all streamlit methods"""
        return [attr for attr in dir(st) if not attr.startswith("_")]

# %% ../nbs/01_core.ipynb 11
@patch_to(StreamlitPatcher, cls_method=False)
def _wrap(
    cls,
    method_name: str,
    wrapper: tp.Callable,
    verbose: bool = False,
) -> None:
    """make a streamlit method jupyter friendly

    Parameters
    ----------
    method_name : str
        which method to jupyterify
    wrapper : tp.Callable
        wrapper function to use
    """
    if IN_IPYTHON:  # only patch if in jupyter
        if verbose:
            if hasattr(wrapper, "__name__"):
                print(
                    f"wrapping 'st.{method_name}' with 'streamlit_jupyter.core.{wrapper.__name__}'"
                )
            else:
                print(
                    f"wrapping 'st.{method_name}' with 'streamlit_jupyter.core.{wrapper}'"
                )

        trg = getattr(st, method_name)  # get the streamlit method
        setattr(st, method_name, wrapper(trg))  # patch the method
        cls.registered_methods.add(method_name)  # add to registered methods

# %% ../nbs/01_core.ipynb 16
def _display(arg: tp.Any) -> None:
    if isinstance(arg, str):
        IPython.display.display(IPython.display.Markdown(arg))
    else:
        IPython.display.display(arg)


def _st_write(func_to_decorate):
    """Decorator to display objects passed to Streamlit in Jupyter notebooks."""

    @functools.wraps(func_to_decorate)
    def wrapper(*args, **kwargs):
        for arg in args:
            _display(arg)

    return wrapper

# %% ../nbs/01_core.ipynb 22
def _st_heading(func_to_decorate: tp.Callable, tag: str) -> tp.Callable:
    """Decorator to display objects passed to Streamlit in Jupyter notebooks."""

    @functools.wraps(func_to_decorate)
    def wrapper(*args, **kwargs):
        if len(args) == 1:
            body = args[0]
        elif len(args) == 2:
            body, anchor = args
        elif len(args) > 2:
            raise ValueError(
                f"Too many positional arguments: {len(args)}, {func_to_decorate.__name__} only accepts 2"
            )
        elif len(args) == 0:
            if "body" not in kwargs:
                raise ValueError(
                    f"Missing required argument: body, {func_to_decorate.__name__} requires a body"
                )
            body = kwargs["body"]

        if isinstance(body, str):
            _display(f"{tag} {body}")
        else:
            raise TypeError(
                f"Unsupported type: {type(body)}, {func_to_decorate.__name__} only accepts strings"
            )

    return wrapper

# %% ../nbs/01_core.ipynb 29
def _st_caption(func_to_decorate):
    """Decorator to display json"""

    @functools.wraps(func_to_decorate)
    def wrapper(*args, **kwargs):
        if len(args) == 0:
            raise ValueError(f"at least one positional argument is required")
        elif len(args) == 1:
            body = args[0]

        if isinstance(body, str):
            body_caption = "\n".join([f"> {line}" for line in body.split("\n")])
            _display(body_caption)
        else:
            raise TypeError(f"Unsupported type: {type(body)}")

    return wrapper

# %% ../nbs/01_core.ipynb 33
def _st_type_check(
    func_to_decorate: tp.Callable,
    allowed_types: tp.Union[tp.Type, tp.Collection[tp.Type]],
) -> tp.Callable:
    """Decorator to display objects passed to Streamlit in Jupyter notebooks."""
    allowed_types = listify(allowed_types)  # make sure it's a list

    @functools.wraps(func_to_decorate)
    def wrapper(*args, **kwargs):
        if len(args) == 1:
            body = args[0]
        elif len(args) > 1:
            raise ValueError(
                f"Too many positional arguments: {len(args)}, {func_to_decorate.__name__} only accepts 2"
            )
        elif len(args) == 0:
            if kwargs:
                raise NotImplementedError(
                    f"kwargs not supported yet, 'streamlit_data_science.utils._wrap_st_type_check' only accepts positional arguments"
                )
            else:
                raise ValueError(f"at least one positional argument is required")

        if type(body) in allowed_types:
            _display(body)
        else:
            raise TypeError(
                f"Unsupported type: {type(body)}, {func_to_decorate.__name__} only accepts {allowed_types}"
            )

    return wrapper

# %% ../nbs/01_core.ipynb 37
def _jupyter_display_code(body: str, language: str = "python") -> None:
    _display(f"```{language}\n{body}\n```")

# %% ../nbs/01_core.ipynb 39
def _st_code(func_to_decorate):
    @functools.wraps(func_to_decorate)
    def wrapper(*args, **kwargs):
        if len(args) == 1:
            body = args[0]
            language = kwargs["language"] if "language" in kwargs else "python"
        elif len(args) == 2:
            body, language = args

        if isinstance(body, str):
            _jupyter_display_code(body, language=language)
        else:
            raise TypeError(
                f"Unsupported type: {type(body)}, {func_to_decorate.__name__} only accepts strings"
            )

    return wrapper

# %% ../nbs/01_core.ipynb 48
def _st_text(func_to_decorate):
    """Decorator to display mono-spaced text"""

    @functools.wraps(func_to_decorate)
    def wrapper(*args, **kwargs):
        if len(args) == 0:
            raise ValueError(f"at least one positional argument is required")
        elif len(args) == 1:
            body = args[0]
        elif len(args) >= 2:
            raise ValueError("Only one positional argument is supported")

        if isinstance(body, str):
            _jupyter_display_code(body, language=None)
        else:
            raise TypeError(
                f"Unsupported type: {type(body)}, {func_to_decorate.__name__} only accepts strings and dicts"
            )

    return wrapper

# %% ../nbs/01_core.ipynb 51
from IPython.display import Latex


def _st_latex(func_to_decorate):
    """Decorator to display latex equations"""

    @functools.wraps(func_to_decorate)
    def wrapper(*args, **kwargs):
        if len(args) == 0:
            raise ValueError(f"at least one positional argument is required")
        elif len(args) == 1:
            body = args[0]
        elif len(args) >= 2:
            raise ValueError("Only one positional argument is supported")

        if isinstance(body, str):
            body = rf"\begin{{equation}}{body}\end{{equation}}"
            display(Latex(body))
        else:
            raise TypeError(
                f"Unsupported type: {type(body)}, {func_to_decorate.__name__} only accepts strings and dicts"
            )

    return wrapper

# %% ../nbs/01_core.ipynb 58
def _st_json(func_to_decorate):
    """Decorator to display json"""

    @functools.wraps(func_to_decorate)
    def wrapper(*args, **kwargs):
        if len(args) == 0:
            raise ValueError(f"at least one positional argument is required")
        elif len(args) == 1:
            body = args[0]
            expanded = kwargs.get("expanded", True)
        elif len(args) >= 2:
            raise ValueError("Only one positional argument is supported")

        if isinstance(body, str) and not expanded:
            _jupyter_display_code(body, language="json")
        elif isinstance(body, str) and expanded:
            body = json.dumps(json.loads(body), indent=2)
            _jupyter_display_code(body, language="json")
        elif isinstance(body, dict) and not expanded:
            body = json.dumps(body)
            _jupyter_display_code(body, language="json")
        elif isinstance(body, dict) and expanded:
            body = json.dumps(body, indent=2)
            _jupyter_display_code(body, language="json")
        else:
            raise TypeError(
                f"Unsupported type: {type(body)}, {func_to_decorate.__name__} only accepts strings and dicts"
            )

    return wrapper

# %% ../nbs/01_core.ipynb 68
def _dummy_wrapper_noop(func_to_decorate):
    @functools.wraps(func_to_decorate)
    def wrapper(*args, **kwargs):
        return noop  # castrate the function to do nothing

    return wrapper

# %% ../nbs/01_core.ipynb 74
class _DummyExpander:
    __doc__ = st.expander.__doc__

    def __init__(self, label: str, expanded: bool = False):
        self.label = label
        self.expanded = expanded

    def __enter__(self):
        _display(f">**expander starts**: {self.label}")

    def __exit__(self, *args):
        _display(f">**expander ends**")


def _st_expander(cls_to_replace: st.expander):
    return _DummyExpander

# %% ../nbs/01_core.ipynb 78
def _st_text_input(func_to_decorate):
    """Decorator to display date input in Jupyter notebooks."""

    @functools.wraps(func_to_decorate)
    def wrapper(*args, **kwargs):
        if len(args) == 1:
            description = args[0]
            if "value" in kwargs:
                value = kwargs["value"]
            else:
                value = None

        elif len(args) == 2:
            description, value = args

        text = widgets.Textarea(
            description=description,
            value=value,
            disabled=False,
            placeholder="Type something",
        )

        display(text)
        return text.value

    return wrapper

# %% ../nbs/01_core.ipynb 83
def _st_date_input(func_to_decorate):
    """Decorator to display date input in Jupyter notebooks."""

    @functools.wraps(func_to_decorate)
    def wrapper(*args, **kwargs):
        if len(args) == 1:
            description = args[0]
            if "value" in kwargs:
                value = pd.to_datetime(kwargs["value"]).date()
            else:
                value = datetime.now()

        elif len(args) == 2:
            description = args[0]
            value = pd.to_datetime(args[1])

        date = widgets.DatePicker(
            description=description,
            value=value,
            disabled=False,
        )

        display(date)
        return date.value

    return wrapper

# %% ../nbs/01_core.ipynb 89
def _st_checkbox(func_to_decorate):
    """Decorator to display checkbox in Jupyter notebooks."""

    @functools.wraps(func_to_decorate)
    def wrapper(*args, **kwargs):
        if len(args) == 1:
            description = args[0]
            if "value" in kwargs:
                value = kwargs["value"]
            else:
                value = True

        elif len(args) == 2:
            description, value = args

        w = widgets.Checkbox(
            value=value, description=description, disabled=False, indent=False
        )

        display(w)
        return w.value

    return wrapper

# %% ../nbs/01_core.ipynb 94
def _st_single_choice(func_to_decorate, jupyter_widget: widgets.Widget):

    """Decorator to display single choice widget in Jupyter notebooks."""

    @functools.wraps(func_to_decorate)
    def wrapper(*args, **kwargs):
        if len(args) < 1:
            raise ValueError("You must provide at least 1 argument")
        if len(args) == 1:
            label = args[0]
            options = kwargs["options"]
            index = kwargs["index"] if "index" in kwargs else 0
        elif len(args) == 2:
            label, options = args
            index = kwargs["index"] if "index" in kwargs else 0
        elif len(args) == 3:
            label, options, index = args

        w = jupyter_widget(
            options=options,
            description=label,
            index=index,
        )

        display(w)
        return w.value

    return wrapper

# %% ../nbs/01_core.ipynb 99
def _st_multiselect(func_to_decorate):
    """Decorator to display multiple choice widget in Jupyter notebooks."""

    @functools.wraps(func_to_decorate)
    def wrapper(*args, **kwargs):
        if len(args) < 1:
            raise ValueError("You must provide at least 1 argument")
        if len(args) == 1:
            label = args[0]
            options = kwargs.get("options")
        elif len(args) == 2:
            label, options = args
            index = kwargs["index"] if "index" in kwargs else 0
        else:
            raise ValueError("Too many positional arguments, provide at most 2")

        w = widgets.SelectMultiple(
            options=options,
            description=label,
            value=kwargs.get("default", []),
        )

        display(w)
        return w.value

    return wrapper

# %% ../nbs/01_core.ipynb 104
def _plot_metric(*, label, value, delta=None, label_visibility="visible"):
    import plotly.graph_objects as go

    if delta is None:
        mode = "number"
        template = {
            "data": {
                "indicator": [
                    {
                        "title": {"text": label},
                    }
                ]
            }
        }
    else:
        mode = "number+delta"
        template = {
            "data": {
                "indicator": [
                    {
                        "title": {"text": label},
                        "delta": {"reference": value - delta},
                    }
                ]
            }
        }

    fig = go.Figure()
    fig.add_trace(
        go.Indicator(
            mode=mode,
            value=value,
        )
    )

    fig.update_layout(width=300, height=300, template=template)

    if label_visibility != "hidden":
        fig.show()


def _st_metric(func_to_decorate):
    """wrapper for st.metric"""

    @functools.wraps(func_to_decorate)
    def wrapper(*args, **kwargs):
        # some unsupported kwargs, None by default
        delta_color = kwargs.get("delta_color")
        help = kwargs.get("help")
        label_visibility = kwargs.get("label_visibility")

        allowed_values = {
            "label_visibility": ["visible", "hidden", "collapsed", None],
            "delta_color": ["normal", "inverse", "off", None],
        }
        for k, v in allowed_values.items():
            if not eval(f"{k} in v"):
                got = eval(f"{k}")
                raise ValueError(
                    f"f'{got}' is not an accepted value. {k} only accepts: {v}"
                )

        if len(args) == 0:
            label = kwargs.get("label")
            value = kwargs.get("value")
            delta = kwargs.get("delta")
        if len(args) == 1:
            label = args[0]
            value = kwargs.get("value")
            delta = kwargs.get("delta")
        elif len(args) == 2:
            label, value = args
            delta = kwargs.get("delta")
        elif len(args) == 3:
            label, value, delta = args
        elif len(args) == 4:
            label, value, delta, delta_color = args
        elif len(args) == 5:
            label, value, delta, delta_color, help = args
        elif len(args) == 6:
            label, value, delta, delta_color, help, label_visibility = args
        else:
            raise ValueError("Too many positional arguments, provide at most 6")

        for kwarg in ["delta_color", "help", "label_visibility"]:
            if eval(f"{kwarg} is not None"):
                logger.warning(
                    f"`{kwarg}` argument is not supported in Jupyter notebooks, but will be applied in Streamlit"
                )

        _plot_metric(label=label, value=value, delta=delta)

    try:
        import plotly.graph_objects as go

        return wrapper
    except ImportError:
        msg = "plotly is not installed, falling back to default st.metric implementation\n"
        msg += "To use plotly, run `pip install plotly`"
        logger.warning(msg)
        return func_to_decorate

# %% ../nbs/01_core.ipynb 111
@patch_to(StreamlitPatcher, as_prop=True)
def MAPPING(cls) -> tp.Dict[str, tp.Callable]:
    """mapping of streamlit methods to their jupyter friendly versions"""
    return {
        "write": _st_write,
        "title": functools.partial(_st_heading, tag="#"),
        "header": functools.partial(_st_heading, tag="##"),
        "subheader": functools.partial(_st_heading, tag="###"),
        "caption": _st_caption,
        "markdown": functools.partial(_st_type_check, allowed_types=str),
        "dataframe": functools.partial(_st_type_check, allowed_types=pd.DataFrame),
        "date_input": _st_date_input,
        "text": _st_text,
        "latex": _st_latex,
        "json": _st_json,
        "cache": _dummy_wrapper_noop,
        "expander": _st_expander,
        "text_input": _st_text_input,
        "text_area": _st_text_input,
        "code": _st_code,
        "checkbox": _st_checkbox,
        "radio": functools.partial(
            _st_single_choice, jupyter_widget=widgets.RadioButtons
        ),
        "selectbox": functools.partial(
            _st_single_choice, jupyter_widget=widgets.Dropdown
        ),
        "multiselect": _st_multiselect,
        "metric": _st_metric,
    }
