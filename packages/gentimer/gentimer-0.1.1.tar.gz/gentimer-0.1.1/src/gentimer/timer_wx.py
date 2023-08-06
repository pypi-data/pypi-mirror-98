__version__ = "0.1.0"
__all__ = ["gen_timer"]

from gentimer._typed import CancelFuncType, DoneCallbackType, GeneratorType
import wx  # type: ignore


def gen_timer(
    gen: GeneratorType, done: DoneCallbackType = None
) -> CancelFuncType:
    """

    Parameters
    -----------
        gen : generator
        done : callable

    Returns
    --------
        cancel : callable

    """

    _timer = None

    def _next() -> None:
        nonlocal _timer
        interval = next(gen, None)
        if interval is not None:
            _timer = wx.CallLater(max(0, int(interval * 1000)), _next)
        elif done:
            done()

    def _cancel(*_) -> None:  # XXX: argument
        nonlocal _timer
        if _timer:
            _timer.Stop()
            _timer = None

    def _start() -> None:
        nonlocal _timer
        _timer = wx.CallAfter(_next)

    _start()  # TODO: start later

    return _cancel


def main() -> None:
    app = wx.App()
    frame = wx.Frame(None, wx.ID_ANY, "Test")
    label = wx.StaticText(frame, wx.ID_ANY, "")

    def count_timer(count: int = 5) -> GeneratorType:
        """Count-up timer"""
        for num in range(count):
            label.SetLabel(str(num))
            yield 1  # instead of time.sleep(1)

    cancel = gen_timer(count_timer(5), frame.Close)

    button = wx.Button(frame, wx.ID_ANY, "cancel")
    button.Bind(wx.EVT_BUTTON, cancel)
    sizer = wx.BoxSizer(wx.VERTICAL)
    sizer.Add(label, flag=wx.ALIGN_CENTER, proportion=1)
    sizer.Add(button, flag=wx.ALIGN_CENTER)
    frame.SetSizer(sizer)
    frame.Show()
    app.MainLoop()
