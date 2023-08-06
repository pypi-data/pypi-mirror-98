"""juc2.art.meta"""


class _Meta:
    def __init__(self, x=0, y=0, reverse_art=False, transparent=False):
        self.x = x
        self.y = y
        self.reverse_art = reverse_art
        self.transparent = transparent

    def reverse(self):
        if not self.reverse_art:
            self.reverse_art = True
