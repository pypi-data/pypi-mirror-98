# -*- coding: utf-8 -*-
import sys
from pathlib import Path

import paz_gui.paz_gui as pg
import paz_gui.paz_behaviour as pb

class MyPazBox(pg.PazBox):
    # ~ text = "@green(sfaw akofaw aaaaa bbbbbbbbb ccccccccc dddddddddddd) @on_blue(@red(wkoakfpawfkawp)) fkwaofaawfa  AFAWFA WA Awaw) "
    text = "@green(sfaw add) @on_blue(@red(wkoakfpawfkawp) vvv) fkwao@)@)faawfa  AFAWFA WA Awaw"
    # ~ text = "@green(sf) @on_blue(@red(wk) v)"
    # ~ text = "b @g(@l(a)c@p(@r(u)) @b(v)"
    # ~ text = "@@l(@f(a)) @(@) @l(@f(b@(@(@()@d(c)@ll(a@vv(lk@(lk) @kk(@@ol))))"
    # ~ text = " @(@) @l(@f(b@(@(@()@d(c)@ll(a@vv(lk@(lk) @)@)@( @kk(@@ol))))"
    # ~ text = "@(lk@) @)@@@)@(\n@green(lk) @)@@@)@("
    # ~ text = "@green(lk)a@)@@@)@("
    # TODO: See the part in str where red follows on_blue
    # While drawing style the first one is ignored
    # frame buffer's style list must support as many styles
    # as you want for one character position
    # ~ text = "@green(sfa) @on_blue(@red(wawp)) fkwaofa()))))awfa  AFAWFA WA Awaw) "
    style = {
        'rect': (0, 0, 30, 30),
        'text': { 'rich': True },
        # ~ 'background': '@on_red(.)',
        'background': u'.',
    }

    def children(self):
        class MyInnerPazBox(pg.PazBox):
            # ~ text = "@blue(1abc )@red_on_white(2abc)c\tüş\tş@@çç\n \n\n 4@cyan(gag@bold(w@(a)wf)a@red(fk)) kk"
            text = "@blue(sgag afwwafaş fkw fwfj kja kjjk)"
            name = "1"
            style = {
                'border': True,
                'rect': (0, 0, 20, 20),
                'margin': (0, 0, 0, 0),
                'scroll-pos': (0, 0),
                'background': '.',
                'text': { 'rich': True }
            }

        return []
        return [MyInnerPazBox]

    def schedule(self):
        self._lala = 0
        # ~ self.scheduler.every(0.25).seconds.do(self.periodic_job, what='text')

    def periodic_job(self, what='nothing'):
        self.set_text(what + str(self._lala))
        self._lala += 1


class GridBox(pg.PazBox):
    style = {
        'rect': [0, 0, 6, 8],
        'scroll-pos': (-1, -1),
        'behaviour': [pb.VBoxBehaviour],
    }
    def children(self):
        class Box1(pg.PazBox):
            style = {
                'behaviour': [pb.HBoxBehaviour],
                'stretch-ratio': 0.5,
            }
            def children(self):
                class Box11(pg.PazBox):
                    style = {
                        'background': '+',
                        'stretch-ratio': 0.5,
                    }
                class Box12(pg.PazBox):
                    style = {
                        'background': '-',
                        'stretch-ratio': 0.5,
                    }

                return [Box11, Box12]
                
        class Box2(pg.PazBox):
            style = {
                'behaviour': [pb.HBoxBehaviour],
                'stretch-ratio': 0.5,
            }
            def children(self):
                class Box21(pg.PazBox):
                    style = {
                        'background': '*',
                        'stretch-ratio': 0.5,
                    }
                class Box22(pg.PazBox):
                    style = {
                        'background': '/',
                        'stretch-ratio': 0.5,
                    }

                return [Box21, Box22]
                
        return [Box1, Box2]


class BorderedGridBox(pg.PazBox):
    style = {
        'border': True,
        'rect': [0, 0, 8, 10],
        'scroll-pos': (0, 0),
        'behaviour': [pb.VBoxBehaviour],
    }
    def children(self):
        class Box1(pg.PazBox):
            style = {
                'border': False,
                'behaviour': [pb.HBoxBehaviour],
                'scroll-pos': (0, 0),
                'stretch-ratio': 0.6,
            }
            def children(self):
                class Box11(pg.PazBox):
                    style = {
                        'border': True,
                        'background': '+',
                        'stretch-ratio': 0.8,
                    }
                class Box12(pg.PazBox):
                    style = {
                        'background': '-',
                        'stretch-ratio': 0.2,
                    }

                return [Box11, Box12]
                
        class Box2(pg.PazBox):
            style = {
                'border': False,
                'behaviour': [pb.HBoxBehaviour],
                'stretch-ratio': 0.4,
            }
            def children(self):
                class Box21(pg.PazBox):
                    style = {
                        'background': '*',
                        'stretch-ratio': 0.5,
                    }
                class Box22(pg.PazBox):
                    style = {
                        'border': True,
                        'background': '/',
                        'stretch-ratio': 0.5,
                    }

                return [Box21, Box22]
                
        return [Box1, Box2]


class CheckboxedBox(pg.PazBox):
    style = {
        'rect': (0, 0, 15, 8),
    }
    def children(self):
        class Checkbox1(pg.PazBox):
            text = "@blue(Choose me!)"
            style = {
                'rect': (0, 0, 1.0, 1),
                'behaviour': [pb.CheckboxBehaviour],
                'active': True,
                'checkbox.checked': True,
                'text': { 'rich': True },
            }
        class Checkbox2(pg.PazBox):
            text = "Don't choose me!"
            style = {
                'rect': (0, 1, 1.0, 2),
                'behaviour': [pb.CheckboxBehaviour],
            }

        return [Checkbox1, Checkbox2]


class SimpleBox(pg.PazBox):
    name = "1"
    style = {
        'border': True,
        'rect': (0, 0, 15, 15),
        'margin': (0, 0, 0, 0),
        'scroll-pos': (2, -2),
        'background': '@on_red( )',
    }
    def children(self):
        class MyInnerPazBox(pg.PazBox):
            name = "2"
            text = "@red(abcdefg)"
            style = {
                'border': True,
                'rect': (0, 0, 1.0, 1.0),
                'margin': (0, 0, 0, 0),
                'scroll-pos': (0, 0),
                'background': '@blue(.)',
                'text': { 'rich': True },
            }
            def children(self):
                class MyInnerInnerPazBox(pg.PazBox):
                    name = "3"
                    style = {
                        'visible': True,
                        'rect': (0, 0, 1.0, 1.0),
                        'border': True,
                        'background': 'x',
                    }

                return []
                return [MyInnerInnerPazBox]

        return [MyInnerPazBox]
        

class ModifyTextBox(pg.PazBox):
    text = "aaa\taa\n\n bb  bbb"
    style = {
        'rect': (0, 0, 10, 15),
    }

    def event(self, ev):
        if ev.cmp('O'):
            # ~ import pdb; pdb.set_trace()
            self.modify_text('b', 2)

    def schedule(self):
        self.__job1 = self.scheduler.every(1).seconds.do(self.job1)

    @pg.PazGui._scheduled
    def job1(self):
        # ~ import pdb; pdb.set_trace()
        # ~ self.modify_text('ccc', 10, True)
        self.modify_text('ccc', (6, 1), False)
        self.scheduler.cancel_job(self.__job1)


class TextArea(pg.PazBox):
    text = "aaa  cc\nbbb\t f"
    style = {
        'rect': (0, 0, 10, 15),
        'behaviour': [pb.TextEditBehaviour],
        'text': {
            'cursor': { },
            # rich is overwritten by TextEditBehaviour
            'rich': True,
        },
    }


def main():
    from paz_gui import accessories as acc
    stream = acc.TestOut()

    paz_gui = pg.PazGui(TextArea, config={ })
    paz_gui.run()
    return

    paz_gui = pg.PazGui(ModifyTextBox, stream=stream, config={ 'background-color': 'normal' })
    paz_gui.run()
    frame_size = (paz_gui.width, paz_gui.height)
    print(stream.get_frame(frame_size, (paz_gui.width, paz_gui.height)))
