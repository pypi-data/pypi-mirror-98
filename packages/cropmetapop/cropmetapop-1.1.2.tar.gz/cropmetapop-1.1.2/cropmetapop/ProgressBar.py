#!/usr/bin/env python3

""" This file contains the code for the progress bar"""


class ProgressBar:
    '''
    Progress bar
    '''
    def __init__(self, valmax, maxbar, title):
        if valmax == 0:
            valmax = 1
        if maxbar > 200:
            maxbar = 200
        self.valmax = valmax
        self.maxbar = maxbar
        self.title = title

    def update(self, val):
        """Function that updates the progress bar"""
        import sys
        # format
        if val > self.valmax:
            val = self.valmax

        # process
        perc = round((float(val) / float(self.valmax)) * 100)
        scale = 100.0 / float(self.maxbar)
        barre = int(perc / scale)

        # render
        out = '\r %20s [%s%s] %3d %%' % (self.title, '=' * barre, ' ' * (self.maxbar - barre), perc)
        sys.stdout.write(out)
        sys.stdout.flush()
