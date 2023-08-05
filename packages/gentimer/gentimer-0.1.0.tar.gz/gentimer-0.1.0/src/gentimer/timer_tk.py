__version__ = "0.1.0"
__all__ = ["gen_timer"]


from gentimer._typed import CancelFuncType, DoneCallbackType, GeneratorType
from tkinter import Misc as _tkMisc


def gen_timer(
    root: _tkMisc, gen: GeneratorType, done: DoneCallbackType = None
) -> CancelFuncType:
    """

    Parameters
    -----------
        root : any tkinter widget
        gen : generator instance
        done : callable, optional

    Returns
    --------
        cancel : callbale

    """
    _task_id = None

    def _next() -> None:
        nonlocal _task_id
        interval = next(gen, None)
        if interval is not None:
            _task_id = root.after(max(0, int(interval * 1000)), _next)
        elif done:
            done()

    def _cancel() -> None:
        nonlocal _task_id
        if _task_id:
            root.after_cancel(_task_id)
            _task_id = None

    def _start() -> None:
        nonlocal _task_id
        _task_id = root.after_idle(_next)

    _start()  # TODO: start later

    return _cancel


def main() -> None:
    import tkinter

    root = tkinter.Tk()
    numVar = tkinter.IntVar(root, value=0)

    def count_timer(count: int = 5) -> GeneratorType:
        """Count-up timer"""
        for num in range(count):
            numVar.set(num)
            yield 1  # instead of time.sleep(1)

    cancel = gen_timer(root, count_timer(5), done=root.quit)

    tkinter.Label(root, textvar=numVar).pack()
    tkinter.Button(root, text="cancel", command=cancel).pack()
    root.mainloop()
    root.destroy()
