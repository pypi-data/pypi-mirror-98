"""juc2.art.tools"""

from juc2.art.meta import _Meta


class Tools:

    class Eraser(_Meta):
        def __init__(self, width=0, height=0, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.figure = self._get_eraser(width, height)

        def _get_eraser(self, width, height):
            return ''.join([' '*width+'\n' for row in range(height)])
