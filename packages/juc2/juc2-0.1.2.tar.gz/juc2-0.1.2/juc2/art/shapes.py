"""juc2.art.shapes"""

from juc2.art.meta import _Meta


class Shapes:

    class Rectangle(_Meta):
        def __init__(self, width=3, height=3, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.width = width
            self.height = height
            self.figure = self._get_rectangle(self.width, self.height)

        def _get_rectangle(self, width, height):
            top = '╔' + '═' * (width-2) + '╗' + '\n'
            mid = '║' + ' ' * (width-2) + '║' + '\n'
            bot = '╚' + '═' * (width-2) + '╝' + '\n'
            return top + mid * (height-2) + bot

    class Triangle(_Meta):
        def __init__(self, n=2, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.figure = self._get_triangle(n)

        def _get_triangle(self, n):
            n = max(n, 2)
            if n % 2 == 1: n += 1
            triangle = ['/' + '_'*n + '\\']
            count = 1
            for i in range(0, n-1, 2)[::-1]:
                triangle.append(' '*count + '/' + ' '*i + '\\' + '\n')
                count += 1
            return ''.join(triangle[::-1])
