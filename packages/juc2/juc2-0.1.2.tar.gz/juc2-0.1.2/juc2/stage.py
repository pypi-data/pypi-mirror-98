"""juc2.stage"""

import os
import time

from juc2 import art

mirror_ascii = [
    ('(', ')'),
    ('[', ']'),
    ('>', '<'),
    ('{', '}'),
    ('/', '\\')
]


def _tick(FPS):
    """Sleep desired frames per second."""
    time.sleep(1/FPS)


def _clear_terminal():
    """Cross-platform terminal clear."""
    os.system('cls' if os.name == 'nt' else 'clear')
    # print("%c[2J%c[;H" % (27, 27))


class Stage:
    """juc2 Stage object"""

    def __init__(self, width=40, height=20, frame=False):
        self.width = width
        self.height = height
        self.frame = frame
        self.grid = [list(' '*width) for i in range(height)]

    @staticmethod
    def _prep_figure(figure):
        """Remove blank lines from figure."""
        return '\n'.join([row for row in figure.split('\n') if row != ''])

    @staticmethod
    def _reverse_figure(figure):
        """Reverses an ascii art figure."""
        li = figure.splitlines()
        longest_line = max([len(l) for l in li])

        for n in range(len(li)):
            for i, j in mirror_ascii:
                li[n] = li[n].replace(i, '!TMP!').replace(j, i).replace('!TMP!', j)
            li[n] = li[n].ljust(longest_line)[::-1]

        return '\n'.join(li)

    def display(self):
        """Displays the grid to the terminal."""
        for row in self.grid:
            print(''.join(row))

    def stage_eraser(self):
        """Get the stage eraser."""
        return art.Tools.Eraser(width=self.width, height=self.height)

    def stage_frame(self):
        """Get the stage frame."""
        return art.Shapes.Rectangle(
            width=self.width, height=self.height, transparent=True
        )

    def clear_stage(self):
        """Clear the stage."""
        self.load(self.stage_eraser())

    def load_frame(self):
        """Load the frame."""
        self.load(self.stage_frame())

    def load(self, artwork):
        """Loads artwork onto the grid."""
        y = artwork.y
        x = initial_x = artwork.x
        if artwork.reverse_art:
            artwork.figure = self._reverse_figure(artwork.figure)
            artwork.reverse_art = False
        chars = self._prep_figure(artwork.figure)

        for c in chars:
            if c == '\n':
                y += 1
                x = initial_x
                continue
            if c == ' ' and artwork.transparent:
                x += 1
                continue
            self.grid[y][x] = c
            x += 1

    def draw(self, art_queue=None, FPS=None):
        """Draws a figure or figures onto the terminal."""

        # 1 - Clear Terminal
        _clear_terminal()

        # 2 - Clear Stage
        self.clear_stage()

        # 3 - Load Art
        if isinstance(art_queue, list):
            for artwork in art_queue:
                self.load(artwork)
        else:
            if art_queue:
                artwork = art_queue
                self.load(artwork)
        if self.frame:
            self.load_frame()

        # 4 - Display Art
        self.display()

        # 5 - Wait
        if FPS:
            _tick(FPS)
