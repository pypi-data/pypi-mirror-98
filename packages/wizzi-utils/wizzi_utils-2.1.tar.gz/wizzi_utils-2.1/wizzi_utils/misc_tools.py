import sys
import os
import datetime
from timeit import default_timer as timer
from typing import Callable
import cProfile
import pstats
import io
import numpy as np

LINES = '-' * 80


def get_timer_delta(start_timer: float) -> datetime.timedelta:
    end_timer = get_timer()
    d = datetime.timedelta(seconds=(end_timer - start_timer))
    return d


def get_timer() -> float:
    return timer()


def get_current_date_hour() -> str:
    now = datetime.datetime.now()
    current_time = now.strftime('%d-%m-%Y %H:%M:%S')
    return current_time


def get_mac_address() -> str:
    from uuid import getnode as get_mac
    mac = get_mac()
    mac = ':'.join(("%012X" % mac)[i:i + 2] for i in range(0, 12, 2))
    return mac


def get_cuda_version() -> str:
    if 'CUDA_PATH' in os.environ:
        cuda_v = os.path.basename(os.environ['CUDA_PATH'])
    else:
        cuda_v = 'No CUDA_PATH found'
    return cuda_v


def make_cuda_invisible() -> None:
    """
        disable(the -1) gpu 0
        TODO support hiding multiple gpus
    """
    os.environ['CUDA_VISIBLE_DEVICES'] = '-1, 0'
    return


def start_profiler() -> cProfile.Profile:
    pr = cProfile.Profile()
    pr.enable()
    return pr


def end_profiler(pr: cProfile.Profile, rows: int = 10) -> str:
    pr.disable()
    s = io.StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
    ps.print_stats(rows)
    return s.getvalue()


def main_wrapper(
        main_function: Callable,
        cuda_off: bool = False,
        torch_v: bool = False,
        tf_v: bool = False,
        cv2_v: bool = False,
        with_profiler: bool = False
) -> None:
    """
    :param main_function: the function to run
    :param cuda_off: make gpu invisible and force run on cpu
    :param torch_v: print torch version
    :param tf_v: print tensorflow version
    :param cv2_v: print opencv version
    :param with_profiler: run profiler
    :return:
    """
    print(LINES)
    start_timer = get_timer()

    # make_cuda_invisible()
    print('main_wrapper:')
    print('* Run started at {}'.format(get_current_date_hour()))
    print('* Python Version {}'.format(sys.version))
    print('* Working dir: {}'.format(os.getcwd()))
    print('* Computer Mac: {}'.format(get_mac_address()))
    cuda_msg = '* CUDA Version: {}'.format(get_cuda_version())
    if cuda_off:
        make_cuda_invisible()
        cuda_msg += ' (Turned off)'
    print(cuda_msg)

    if torch_v:
        try:
            import torch
            print('* PyTorch Version {}'.format(torch.__version__))
        except (ImportError, ModuleNotFoundError, NameError) as err:
            print('* {}'.format(err))

    if tf_v:
        try:
            import tensorflow as tf
            print('* TensorFlow Version {}'.format(tf.__version__))
        except (ImportError, ModuleNotFoundError, NameError) as err:
            print('* {}'.format(err))

    if cv2_v:
        try:
            import cv2
            print('* Open cv version {}'.format(cv2.getVersionString()))
        except (ImportError, ModuleNotFoundError, NameError) as err:
            print('* {}'.format(err))

    print('Function {} started:'.format(main_function))
    print(LINES)
    pr = start_profiler() if with_profiler else None
    main_function()
    if with_profiler:
        print(end_profiler(pr))
    print(LINES)
    print('Total run time {}'.format(get_timer_delta(start_timer)))
    print(LINES)
    return


def to_str(var, title: str, data_chars: int = 100) -> str:
    """
    :param var: the variable
    :param title: the title (usually variable name)
    :param data_chars: how many char to print.
        -1: all
         0: none
        +0: maximum 'data_chars' (e.g. data_chars=50 and |str(var)|=100 - first 50 chars)

    examples:
        print(to_str(var=3, title='my_int'))
        print(to_str(var=3.2, title='my_float'))
        print(to_str(var='a', title='my_str'))
        print(to_str(var=[], title='my_empty_list'))
        print(to_str(var=[1, 3, 4], title='1d list of ints'))
        print(to_str(var=[1, 3], title='1d list of ints no data', data_chars=0))  # no data
        print(to_str(var=[15] * 1000, title='1d long list'))
        print(to_str(var=(19, 3, 9), title='1d tuple'))
        print(to_str(var=[[11.2, 15.9], [3.0, 7.55]], title='2d list'))
        print(to_str(var=[(11.2, 15.9), (3.0, 7.55)], title='2d list of tuples'))
        b = np.array([[11.2, 15.9], [3.0, 7.55]])
        print(to_str(var=b, title='2d np array'))
        cv_img = np.zeros(shape=[480, 640, 3], dtype=np.uint8)
        print(to_str(var=cv_img, title='cv_img'))
        print(to_str(var={'a': [1, 2]}, title='dict of lists'))
        print(to_str(var={'a': [{'k': [1, 2]}, {'c': [7, 2]}]}, title='nested dict'))
    :return: informative string of the variable
    """

    def add_data(var_l, data_chars_l: int) -> str:
        data_str_raw = str(var_l)
        data_str = ''
        if data_chars_l < 0:  # all data
            data_str = ': {}'.format(data_str_raw)
        elif data_chars_l > 0:  # first 'data_chars' characters
            data_str = ': {}'.format(data_str_raw[:data_chars_l])
            if len(data_str_raw) > data_chars_l:
                data_str += '...too long'
        return data_str

    type_s = str(type(var)).replace('<class \'', '').replace('\'>', '')  # clean type name
    string = '{}({})'.format(title, type_s)  # base: title and type

    if isinstance(var, (int, float, str)):
        if hasattr(var, "__len__"):
            string = string.replace(')', ',len={}'.format(var.__len__()))
        string += add_data(var, data_chars)

    elif isinstance(var, (list, tuple)):
        string = string.replace(')', ',len={})'.format(var.__len__()))
        string += add_data(var, data_chars)
        if len(var) > 0:  # recursive call
            string += '\n\t{}'.format(to_str(var=var[0], title='{}[0]'.format(title), data_chars=data_chars))

    elif isinstance(var, np.ndarray):
        string = string.replace(')', ',shape={},dtype={})'.format(var.shape, var.dtype))
        string += add_data(var.tolist(), data_chars)
        if len(var) > 0:  # recursive call
            string += '\n\t{}'.format(to_str(var=var[0], title='{}[0]'.format(title), data_chars=data_chars))

    elif isinstance(var, dict):
        string = string.replace(')', ',len={},keys={})'.format(var.__len__(), var.keys()))
        string += add_data(var, data_chars)
        if len(var) > 0:  # recursive call
            first_key = next(iter(var))
            string += '\n\t{}'.format(
                to_str(var=var[first_key], title='{}[{}]'.format(title, first_key), data_chars=data_chars))

    else:  # all unidentified elements get default print (title(type): data)
        string += add_data(var, data_chars)
    return string


def main():
    print('TESTING misc.py:')
    print(to_str(var=3, title='my_int'))
    print(to_str(var=3.2, title='my_float'))
    print(to_str(var='a', title='my_str'))
    print(to_str(var=[], title='my_empty_list'))
    print(to_str(var=[1, 3, 4], title='1d list of ints'))
    print(to_str(var=[1, 3], title='1d list of ints no data', data_chars=0))  # no data
    print(to_str(var=[15] * 1000, title='1d long list'))
    print(to_str(var=(19, 3, 9), title='1d tuple'))
    print(to_str(var=[[11.2, 15.9], [3.0, 7.55]], title='2d list'))
    print(to_str(var=[(11.2, 15.9), (3.0, 7.55)], title='2d list of tuples'))
    b = np.array([[11.2, 15.9], [3.0, 7.55]])
    print(to_str(var=b, title='2d np array'))
    cv_img = np.zeros(shape=[480, 640, 3], dtype=np.uint8)
    print(to_str(var=cv_img, title='cv_img'))
    print(to_str(var={'a': [1, 2]}, title='dict of lists'))
    print(to_str(var={'a': [{'k': [1, 2]}, {'c': [7, 2]}]}, title='nested dict'))
    return


if __name__ == '__main__':
    main_wrapper(
        main_function=main,
        cuda_off=True,
        torch_v=True,
        tf_v=False,
        cv2_v=True,
        with_profiler=False
    )
