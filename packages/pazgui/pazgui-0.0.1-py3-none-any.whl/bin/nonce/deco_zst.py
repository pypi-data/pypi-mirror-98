# -*- coding: utf-8 -*-
import sys
from pathlib import Path

import paz_gui.paz_gui as pg
import paz_gui.paz_behaviour as pb

class MyPazBox(pg.PazBox):
    name = "1"
    style = {
        'border': True,
        'rect': (0, 0, 15, 15),
        'visible': True,
        'margin': (0, 0, 0, 0),
        'scroll-pos': (0, 0),
        'active': True,
        'background': 'g'
        # ~ 'behaviour': [pb.TextEditBehaviour],
    }
    text = ""
    def children(self):
        class MyInnerPazBox(pg.PazBox):
            name = "2"
            # text = "aaabcc @green(amaa ) @bold_red(Lorem Lörem)Lorem Lorem L"
            # text = "aaaa bbbb"
            style = {
                'border': True,
                'rect': (0, 0, 1.0, 1.0),
                'margin': (0, 0, 0, 0),
                'scroll-pos': (0, 0),
                'active': False,
                'background': ord('*'),
                # 'behaviour': [pb.RichTextLabelBehaviour],
                # 'behaviour': [pb.HBoxBehaviour],
            }
            def children(self):
                class MyInnerInnerPazBox(pg.PazBox):
                    name = "3"
                    style = {
                        'visible': True,
                        'rect': (0, 0, 1.0, 1.0),
                        'border': True,
                        'background': ord('x'),
                        # 'margin': (3, 0, 2, 0),
                        # 'behaviour': [pb.CheckboxBehaviour],
                        # ~ 'behaviour': [pb.RichTextLabelBehaviour],
                        'scroll-pos': (0, 0),
                        'stretch-ratio': 1,
                    }
                    # text = "lala @green(lala) lalal"
                    text = "abc"
                    def children(self):
                        class MyInnestPazBox(pg.PazBox):
                            style = {
                                'visible': True,
                                'rect': (0, 0, 1.0, 1.0),
                                'border': True,
                                'background': ord('o'),
                                # 'margin': (3, 0, 2, 0),
                                # 'behaviour': [pb.CheckboxBehaviour],
                                # ~ 'behaviour': [pb.RichTextLabelBehaviour],
                                'scroll-pos': (0, 0),
                                'stretch-ratio': 1,
                            }

                        # ~ return []
                        return [MyInnestPazBox]

                class MyInnerInnerPazBox2(pg.PazBox):
                    style = {
                        'visible': True,
                        'rect': (0.5, 0, 0.5, 1.0),
                        'border': False,
                        'background': ord('y'),
                        # 'margin': (3, 0, 2, 0),
                        # 'behaviour': [pb.CheckboxBehaviour],
                        'behaviour': [pb.RichTextLabelBehaviour],
                        'scroll-pos': (0, 0),
                        'stretch-ratio': 1,
                    }
                # ~ return []
                return [MyInnerInnerPazBox]
                return [MyInnerInnerPazBox, MyInnerInnerPazBox2]

            def event(self, ev):
                if ev.cmp('KEY_DELETE'):
                    self.clear_text()
                    return True

        # ~ return []
        return [MyInnerPazBox]


def main():
    paz_gui = pg.PazGui(MyPazBox)
    paz_gui.run()


if __name__ == "__main__":
    main(len(sys.argv), sys.argv)
