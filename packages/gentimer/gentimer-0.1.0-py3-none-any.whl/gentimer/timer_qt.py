__version__ = "0.1.0"
__all__ = ["gen_timer"]


from PyQt5.QtCore import QObject, QTimer  # type: ignore
from gentimer._typed import CancelFuncType, DoneCallbackType, GeneratorType


def gen_timer(
    parent: QObject, gen: GeneratorType, done: DoneCallbackType = None
) -> CancelFuncType:
    """

    Parameters
    -----------
        parent : QObject
        gen : generator
        done : callable

    Returns
    -------
        cancel : callable

    """
    _timer = QTimer(parent)

    def _next() -> None:
        interval = next(gen, None)
        if interval is not None:
            _timer.setInterval(max(0, int(interval * 1000)))
        elif done:
            done()

    def _cancel() -> None:
        nonlocal _timer
        if _timer:
            _timer.stop()
            _timer = None

    def _start() -> None:
        _timer.timeout.connect(_next)
        _timer.start(0)

    _start()

    return _cancel


def main() -> None:
    from PyQt5.QtCore import Qt  # type: ignore
    from PyQt5.QtWidgets import (  # type: ignore
        QApplication,
        QLabel,
        QPushButton,
        QVBoxLayout,
        QWidget,
    )
    import sys

    app = QApplication(sys.argv)
    win = QWidget()
    label = QLabel("", win)
    label.setAlignment(Qt.AlignCenter)
    button = QPushButton("cancel", win)
    layout = QVBoxLayout(win)
    layout.addWidget(label)
    layout.addWidget(button)
    win.show()

    def count_timer(count: int = 5) -> GeneratorType:
        """Count-up timer"""
        for num in range(count):
            label.setText(str(num))
            yield 1  # instead of time.sleep(1)

    cancel = gen_timer(app, count_timer(5), app.quit)
    button.clicked.connect(cancel)

    # XXX: avoid to call sys.exit for test case
    app.exec_()
