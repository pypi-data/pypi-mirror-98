__version__ = "0.1.0"
__all__ = ["gen_timer"]


from gentimer._typed import CancelFuncType, DoneCallbackType, GeneratorType
import sched


def gen_timer(
    scheduler: sched.scheduler,
    gen: GeneratorType,
    done: DoneCallbackType = None,
) -> CancelFuncType:
    """

    Parameters
    -----------
        scheduler : scheduler
        gen : generator
        done : callable

    Returns
    --------
        cancel : callable
    """

    _event = None
    _priority = 1

    def _next() -> None:
        nonlocal _event
        interval = next(gen, None)
        if interval is not None:
            _event = scheduler.enter(max(0, int(interval)), _priority, _next)
        elif done:
            done()

    def _cancel() -> None:
        nonlocal _event
        if _event:
            scheduler.cancel(_event)
            _event = None

    def _start() -> None:
        nonlocal _event
        _event = scheduler.enter(0, _priority, _next)

    _start()

    return _cancel


def main() -> None:
    import logging

    logging.basicConfig(
        level=logging.DEBUG, format="[%(levelname)-8s] %(message)s"
    )
    logger = logging.getLogger(__name__)

    scheduler = sched.scheduler()

    def count_timer(count: int = 5) -> GeneratorType:
        for num in range(count):
            logger.info("num: %d", num)
            yield 1

    def done_callback():
        logger.info("done")

    gen_timer(scheduler, count_timer(5), done=done_callback)
    scheduler.run()
