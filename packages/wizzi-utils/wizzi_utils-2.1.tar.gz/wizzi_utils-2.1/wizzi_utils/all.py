from wizzi_utils.misc_tools import main_wrapper
from wizzi_utils.misc_tools import to_str
from wizzi_utils.open_cv_tools import cv_first_func
from wizzi_utils.pyplot_tools import pyplot_first_func
from wizzi_utils.torch_tools import torch_first_func


def main():
    print('big program output')
    print(to_str(var=3, title='x', data_chars=-1))
    cv_first_func()
    pyplot_first_func()
    torch_first_func()
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
