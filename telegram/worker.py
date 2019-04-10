import logging
import threading
from queue import Queue

logger = logging.getLogger(__name__)


class BaseWorker:
    """
    Base worker class.
    Each worker must implement the run method to start listening to the queue
    and calling handler functions
    """

    def __init__(self, queue: Queue):
        self._is_enabled = True
        self._queue = queue

    def run(self) -> None:
        raise NotImplementedError()


class SimpleWorker(BaseWorker):
    """Simple one-thread worker"""

    def run(self) -> None:
        self._thread = threading.Thread(  # pylint: disable=attribute-defined-outside-init
            target=self._run_thread
        )
        self._thread.daemon = True
        self._thread.start()

    def _run_thread(self) -> None:
        logger.info('[SimpleWorker] started')

        while self._is_enabled:
            handler, update = self._queue.get()
            handler(update)
            self._queue.task_done()
