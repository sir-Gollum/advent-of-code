# coding: utf-8

class LineGrid:
    def __init__(self, lines):
        self.g = [
            [int(ch) for ch in line.strip()]
            for line in lines
        ]
        self.rows = len(self.g)
        self.cols = len(self.g[0])

    def __str__(self):
        return "\n".join([str(r) for r in self.g])

    def __unicode__(self):
        return str(self)

    def __repr__(self):
        return str(self)
