import os
import pytest
import inspect

from pazgui import gui as pg
from pazgui import accessories as acc
from tests import basic_guis


def test_txt_output():
    script_filename = __file__
    output_filename = os.path.splitext(script_filename)[0] + '.txt'

    basic_guis.auto_quit()

    with open(output_filename, 'w') as fh:
        for name, obj in inspect.getmembers(basic_guis):
            if inspect.isclass(obj) and name.startswith('PazBox'):
                fh.write('* PazBox name: {}\n\n'.format(name))

                stream = acc.TestOut()

                gui = pg.PazGui(obj, stream=stream)
                gui.run()

                size = (gui.width, gui.height)
                frame_size = (min(30, gui.width), min(20, gui.height))
                stream.write_frame(fh, frame_size, size)


    assert True

