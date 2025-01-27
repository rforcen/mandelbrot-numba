import math
from canvas import view_mandelbrot
import numpy as np
import numba as nb

WIDTH = 600
MAX_ITER = 1000


@nb.vectorize(cache=True, fastmath=True)
def get_max_iter(x, y, width, max_iter, r1, i1, r2, i2):
    c0 = complex(r1 + (r2 - r1) * x / width,
                 i1 + (i2 - i1) * y / width)
    c = 0
    for i in range(1, max_iter):
        if abs(c) > 2:
            break
        c = c * c + c0
    return i


def mandelbrot(bbox, width, max_iter):
    grid1D = np.arange(0, width)
    xv, yv = np.meshgrid(grid1D, grid1D)
    r1, i1, r2, i2 = bbox
    iters = get_max_iter(xv, yv, width, max_iter, r1, i1, r2, i2).reshape((width, width, 1))
    pixels = np.where(iters == np.array([max_iter - 1]),
                      np.array([0, 0, 0]),
                      255 * (1 + np.cos(np.log(iters) * np.array([3.32, 0.774, 0.412]))) / 2)
    return pixels


view_mandelbrot(WIDTH, MAX_ITER, mandelbrot)
