"""
Implementation referred from segment analytics-python
https://github.com/segmentio/analytics-python/tree/master/analytics
"""
import atexit
import logging
import queue

try:
    import sentry_sdk
except ImportError:
    pass
from .consumer import Consumer


class Client(object):
    """Create a new celery-queue client."""

    log = logging.getLogger("python-celery-queue")
    threshold_size = 10_000

    def __init__(self, max_queue_size=1_00_000, send=True):
        self.queue = queue.Queue(max_queue_size)
        self.send = send
        self.threshold_exceeded = False
        # Pauses polling the queue and processes left tasks
        if send:
            atexit.register(self.join)

        self.consumer = Consumer(self.queue)
        if send:
            self.consumer.start()

    def enqueue(self, task_func, countdown=0, args=[], kwargs={}):
        """Publishes the task into the queue.
        Drops the task if queue size reaches max limit"""
        msg = {
            "task_func": task_func,
            "countdown": countdown,
            "args": args,
            "kwargs": kwargs,
        }
        if not self.send:
            return True, msg

        # Raise alert everytime queue size exceeds the threshold size
        size = self.queue.qsize()
        if size > self.threshold_size and not self.threshold_exceeded:
            self.threshold_exceeded = True
            if sentry_sdk:
                sentry_sdk.capture_message(
                    f"Celery task queue size exceeded threshold. Size:{size}"
                )
        if size <= self.threshold_size:
            self.threshold_exceeded = False
        # add to queue
        try:
            self.queue.put(msg, block=False)
            return True, msg
        except queue.Full:
            if sentry_sdk:
                sentry_sdk.capture_message(
                    "Task dropped, internal queue max limit reached", msg
                )
            return False, msg

    def join(self):
        """Exits the consumer thread once queue is empty.
        Blocks main thread until secondary thread completes
        """
        self.consumer.pause()
        try:
            self.consumer.join()
        except RuntimeError:
            # consumer thread not running
            pass
