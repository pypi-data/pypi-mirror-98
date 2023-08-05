# -*- coding: utf-8 -*-
import sys
from pathlib import Path

import paz_gui.paz_gui as pg
import paz_gui.paz_behaviour as pb

class MyPazBox(pg.PazBox):
    text = "1abc 2abc 1abc 2abc@green(abc)"
    name = "1"
    style = {
        'border': False,
        'rect': (0, 0, 25, 15),
        'margin': (1, 1, 1, 1),
        'scroll-pos': (1, -1),
        'background': 'g',
        'behaviour': [pb.RichTextLabelBehaviour]
    }
    def children(self):
        class MyInnerPazBox(pg.PazBox):
            name = "2"
            style = {
                'border': True,
                'rect': (0, 0, 1.0, 1.0),
                'margin': (0, 0, 0, 0),
                'scroll-pos': (-1, 2),
                'background': '*',
            }
            def children(self):
                class MyInnerInnerPazBox(pg.PazBox):
                    text = "öçğüşİÜĞŞÖÇı öçğüşİÜĞŞÖÇı öçğüşİÜĞŞÖÇı öçğüşİÜĞŞÖÇı"
                    name = "3"
                    style = {
                        'visible': True,
                        'rect': (0, 0, 1.0, 1.0),
                        'border': True,
                    }
                return [MyInnerInnerPazBox]

        return [MyInnerPazBox]


def main():
    paz_gui = pg.PazGui(MyPazBox, config={ 'background-color': 'normal' })
    paz_gui.run()
