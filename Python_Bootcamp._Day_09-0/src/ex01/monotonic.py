import ctypes
import os
from time import sleep  # Используется только для теста


class timespec(ctypes.Structure):
    """A representation of struct timespec in C."""
    #  Структура timespec указана в каталоге <time.h>.
    _fields_ = [
        ('tv_sec', ctypes.c_long),
        ('tv_nsec', ctypes.c_long)
    ]


def monotonic_time():
    CLOCK_MONOTONIC = 4
    # Экземпляры класса ctypes.CDLL() представляют собой загруженные библиотеки DLL.
    # Функции в этих библиотеках используют стандартное соглашение о вызовах языка C
    librt = ctypes.CDLL('libSystem.dylib', use_errno=True)
    # Функции clock_gettime() получают время указанных часов clk_id.
    # Он помещает в буфер, на который указывает timespec()
    clock_gettime = librt.clock_gettime
    clock_gettime.argtypes = [ctypes.c_int, ctypes.POINTER(timespec)]
    t = timespec()
    if clock_gettime(CLOCK_MONOTONIC, ctypes.pointer(t)) != 0:
        errno_ = ctypes.get_errno()
        raise OSError(errno_, os.strerror(errno_))
    return t.tv_sec + t.tv_nsec * 1e-9


if __name__ == "__main__":
    time_sleep = int(input('Please^ input waiting time: '))
    start1 = monotonic_time()
    print("hello world")
    sleep(time_sleep)
    print("by world")
    finish1 = monotonic_time()
    print(finish1 - start1)
