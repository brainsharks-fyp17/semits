from __future__ import print_function, unicode_literals

import pyte


if __name__ == "__main__":
    screen = pyte.Screen(80, 24)
    stream = pyte.Stream(screen)
    stream.feed("Hello World!")

    for idx, line in enumerate(screen.display, 1):
        print("{0:2d} {1} ¶".format(idx, line))