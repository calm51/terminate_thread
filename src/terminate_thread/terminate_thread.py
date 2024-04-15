import ctypes
import os
import sys
from threading import Thread


def terminate(thread: Thread) -> None:
    if isinstance(thread, Thread) and thread.is_alive():
        _lib.main(ctypes.c_longlong(thread._ident))


def kill(thread: Thread) -> bool:
    if isinstance(thread, Thread) and thread.is_alive():
        # InterruptedError SystemExit
        return ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(thread._ident),
                                                          ctypes.py_object(InterruptedError)) == 1
    return False


def _find_lib():
    paths = [os.path.dirname(__file__),
             os.path.join(os.path.dirname(__file__), "terminate_thread", ),
             os.path.dirname(os.path.abspath(sys.argv[0])),
             os.getcwd(),
             ]
    for i in paths:
        p = os.path.join(i, _lib_name)
        if os.path.isfile(p):
            return p
    else:
        raise ModuleNotFoundError(f'Dynamic library "{_lib_name}" not found.')


_lib_name = 'libterminate.dll' if os.name == "nt" else 'libterminate.so'
_lib = ctypes.CDLL(_find_lib())
