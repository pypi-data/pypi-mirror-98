"""GenTimer module

This root module provides

  * version infomation
  * load sub-module function lazily
"""


__version__ = "0.1.0"


_SUB_MODULES = ["tk", "wx", "qt", "sched"]


def __getattr__(name):
    """Alias for sub-module lazy import

    This import hook requires
    python v3.7 (PEP562 module __getattr__)

    ```python

        # Python ^3.7
        import gentimer
        gentimer.wx(root, gen)

        # Python v3.6
        from gentimer.timer_wx import gen_timer
        gen_timer(root, gen)
    ```

    Avoid module path conflict inside `gentimer/wx.py`
    `import wx` may resolves as self module import.

    Cons: IDE may not follow correct file path.

    """
    from importlib import import_module

    if name in _SUB_MODULES:
        module = import_module(f".timer_{name}", __name__)
        return getattr(module, "gen_timer")  # noqa: B009

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
