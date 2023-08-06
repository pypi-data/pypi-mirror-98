import ctypes
import logging
import threading
import time
from typing import Callable

from openmodule.utils.schema import Schema


class InterruptTestMixin:
    """
    Helper class for testing interrupts and exceptions in code
    for usage, look at file tests/test_interrupt
    """

    def tearDown(self):
        super().tearDown()
        Schema.to_file()

    @classmethod
    def async_raise(cls, thread_obj, exception):
        found = False
        target_tid = 0
        for tid, tobj in threading._active.items():
            if tobj is thread_obj:
                found = True
                target_tid = tid
                break
        if not found:
            raise ValueError("Invalid thread object")

        ret = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(target_tid),
                                                         ctypes.py_object(exception))
        if ret == 0:
            raise ValueError("Invalid thread ID")
        elif ret > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(target_tid, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")

    def exception_in_function(self, f, exception, *, raise_exception_after: float = 3.0, shutdown_timeout: float = 3.0):
        thread = threading.Thread(target=f, daemon=True)
        thread.start()
        time.sleep(raise_exception_after)
        self.async_raise(thread, exception)
        t0 = time.time()
        while time.time() - t0 < shutdown_timeout:
            if thread.is_alive():
                time.sleep(0.5)
            else:
                return
        self.async_raise(thread, SystemExit)
        raise AssertionError("Thread took to long for shutdown")

    def custom_action_in_function(self, f, action, *, call_action_after: float = 3.0, shutdown_timeout: float = 3.0):
        thread = threading.Thread(target=f, daemon=True)
        thread.start()
        time.sleep(call_action_after)
        action(f)
        t0 = time.time()
        while time.time() - t0 < shutdown_timeout:
            if thread.is_alive():
                time.sleep(0.2)
            else:
                return
        self.async_raise(thread, SystemExit)
        raise AssertionError("Thread took to long for shutdown")
