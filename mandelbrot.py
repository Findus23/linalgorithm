import os.path
from multiprocessing.dummy import Pool as ThreadPool

import matplotlib.pyplot as plt
import numpy as np


def f(x):
    return 2 ** (1 - x)


def mandelbrot(zoomlevel):
    print(zoomlevel)
    zoom = f(zoomlevel)
    maxit = 30 + 10 * zoomlevel
    xmin = center[0] - zoom
    xmax = center[0] + zoom
    ymin = center[1] - zoom
    ymax = center[1] + zoom

    loadfile = str(zoomlevel) + ".npy"
    if os.path.isfile(loadfile):
        divtime = np.load(loadfile)
        return [zoomlevel, divtime, [xmin, xmax, ymin, ymax]]

    """Returns an image of the Mandelbrot fractal of size (h,w)."""
    y, x = np.ogrid[ymin:ymax:h * 1j, xmin:xmax:w * 1j]
    c = x + y * 1j
    z = c
    divtime = maxit + np.zeros(z.shape, dtype=int)

    for i in range(maxit):
        z = z ** 2 + c
        diverge = z * np.conj(z) > 2 ** 2  # who is diverging
        div_now = diverge & (divtime == maxit)  # who is diverging now
        divtime[div_now] = i  # note when
        z[diverge] = 2  # avoid diverging too much
        plt.close()
    np.save(str(zoomlevel), divtime)
    return [zoomlevel, divtime, [xmin, xmax, ymin, ymax]]


h = w = 1024
# center = [-0.73, -0.205]
center = [-0.7768816266387022, -0.13675506794031342]

pool = ThreadPool(3)

results = pool.map(mandelbrot, range(17))
pool.close()
pool.join()

for zl, dt, coordinates in results:
    print("Bild:{nr}".format(nr=zl))
    plt.imshow(dt, extent=coordinates)
    plt.ticklabel_format(style='sci', scilimits=(0, 0))

    # plt.axis("off")
    plt.tight_layout()
    plt.savefig("{img}.png".format(img=zl), dpi=350)

# for zoomlevel in range(20):
#     mandelbrot(zoomlevel)
