import sys
import signal
import enum
import time
import re
import copy
import logging
import xml.etree.ElementTree as ET

from blessed import Terminal
import schedule

from pazgui import characters as _c
from pazgui.paz_behaviour import PazBehaviour
from pazgui.accessories import Bunch, DeepDict, init_logger, logger


class FrameBuffer(object):
    """
    Holds character frame and styling information.
    """

    def __init__(self, term):
        """
        Initialize FrameBuffer.

        :arg term Terminal: :class:``Terminal`` object from ``blessed``.
        """

        self._term = term
        self.height = 0
        self.width = 0
        self._frame = [u' '] * self.height * self.width
        self._style = DeepDict()
        self._tmp_style = DeepDict()
        self.resize()
        self.clear()
        self._flush_stream()

    def _pos1(self, x, y):
        """
        Transform terminal coordinates to buffer index.

        :arg int x: Column position (x axis)
        :arg int y: Row position (y axis)

        :return: Returns index.
        """

        return self.width * y + x

    def _pos2(self, ind):
        """
        Transform buffer index to terminal coordinates.

        :arg int ind: Buffer index.

        :return: Tuple (x, y).
        """

        y = ind // self.width
        x = ind % self.width

        return (x, y)

    def _print_c(self, ind):
        """
        Wrapper function for the print directive.

        :arg int ind: Index in the character buffer.
        """

        c = self._frame[ind]
        self._write_to_stream(u'{}'.format(c))

    def _resized(self):
        """
        Checks if the terminal is resized.

        :return bool: ``True`` if terminal is resized.
        """

        resized = False
        if self.height != self._term.height:
            resized |= True

        if self.width != self._term.width:
            resized |= True

        return resized

    def _write_style(self, x, y):
        """
        Writes style to the point (``x``, ``y``) on the terminal.
        """

        style = self.get_style(x, y)
        if style != None:
            if style.startswith('normal'):
                self._write_to_stream(getattr(self._term, 'normal'))
                style = style[len('normal')+1:]

            self._write_to_stream(getattr(self._term, style))

    def _write_to_stream(self, s):
        """
        Print is wrapped in this function because the output stream
        can be something other than stdout.
        """

        self._term.stream.write(s)

    def _flush_stream(self):
        self._term.stream.flush()

    def clear(self):
        """
        Clears the terminal.
        """

        self._write_to_stream(u'{}'.format(self._term.clear))
        self._write_to_stream(u'{}'.format(self._term.home))

    def resize(self):
        """
        Is called when terminal is resized.
        """

        if self._resized():
            self.clear()
            self.height = self._term.height
            self.width = self._term.width
            self._frame = [u' '] * self.height * self.width

    def set_xy(self, x, y, c):
        """
        Sets the character at terminal position (``x``, ``y``) to ``c``.

        :arg int x: x position on the terminal.
        :arg int y: y position on the terminal.
        :arg chr c: Character to be printed.
        """

        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            logger().warning(
                'x < 0 or y < 0 or x >= self.width or y >= self.height')
            return

        if type(c) == int:
            c = chr(c)

        ind = self._pos1(x, y)
        self._frame[ind] = c

    def set_style(self, x, y, z, style):
        """
        Set style of the character at point (``x``, ``y``) and z-index ``z``.
        Style with the largest z-index is printed.

        :arg int x: x position on the terminal.
        :arg int y: y position on the terminal.
        :arg int z: z-index of the style.
        :arg str style: Stype to be printed.
        """

        self._style[y][x][z] = style

    def set_tmp_style(self, x, y, z, style):
        """
        Temporary styles are planned to use for
        instantaneous style chages. Currently it is only
        used for highlighting cursor.

        :arg int x: Column position.
        :arg int y: Row position.
        :arg str style: Style string
        """

        current_style = self.get_style(x, y, z)
        self._tmp_style[y][x][z] = current_style
        self.set_style(x, y, z, style)

    def rm_tmp_style(self, x, y, z):
        if [y, x, z] in self._tmp_style:
            self._style[y][x][z] = self._tmp_style[y][x][z]
            del self._tmp_style[y][x][z]

    def get_style(self, x, y, z=None):
        """
        Get style information at terminal position (``x``, ``y``) with z-index
        ``z``. If ``z`` is not given, the style with the larges z-index is
        returned.

        :arg int x: x position on the terminal.
        :arg int y: y position on the terminal.
        :arg int z: z-index of the style.

        :return str: Style string.
        """
        if [y, x] in self._style:
            if z == None:
                style_xy = self._style[y][x]
            elif z in self._style[y][x]:
                return self._style[y][x][z]

            z_max = 0
            for z in self._style[y][x]:
                if z == 'tmp':
                    z_max = 'tmp'
                    break
                if z > z_max:
                    z_max = z

            if z_max in self._style[y][x]:
                return self._style[y][x][z_max]
            else:
                return None
        else:
            return None

    def update(self):
        """
        Print character buffer and style to the terminal after clearing
        everything.
        """

        self.clear()
        ind = 0
        for y in range(self.height):
            for x in range(self.width):
                ind = self._pos1(x, y)

                self._term.move(x, y)
                self._write_style(x, y)

                self._print_c(ind)

        self._flush_stream()


class PazEvent(object):
    """
    Event object created at the time an event occurs and
    propagated to gui elements.
    """

    def __init__(self, name, source=None, target='all'):
        """
        Constructor

        :arg str name: Event name ('DRAW', 'KEY_XXX', etc.)
        :arg PazBox_or_str object: The source which event originates from
        :arg PazBox_or_str target: The target of the events, event propagation
                                   sinks when it arrives a unique target
        """

        self.name = name
        self.is_char = (len(name) == 1)
        self.source = source
        self.target = target

        self.whitespace_chars = [ 'KEY_ENTER', 'KEY_TAB' ]

    def cmp(self, name):
        """
        Compare the name (type) of the event.

        :arg str name: The name to be compared to

        :return bool: ``True`` if same, otherwise ``False``
        """

        if name == self.name:
            return True
        else:
            return False

    def isprintable(self):
        """
        Check if the event is a printable character by pressing the keyboard.

        :return bool: ``True`` if it is printable.
        """

        if self.is_char and self.name.isprintable():
            return True
        elif self.is_char and self.name in self.whitespace_chars:
            return True
        else:
            return False

    def is_source(self, source):
        """
        Check if the event source same as the ``source`` provided.

        :arg PazBox_or_str source: Source to be compared to

        :return bool: ``True`` if same, otherwise ``False``
        """

        if type(self.source) == str and type(source) == str:
            if source == self.source:
                return True
            else:
                return False
        elif isinstance(self.source, PazBox) and isinstance(source, PazBox):
            if source == self.source:
                return True
            else:
                return False
        else:
            return False

    def is_target(self, target):
        """
        Check if the event's target same as the ``target`` provided.

        :arg PazBox_or_str target: Target to be compared to

        :return bool: ``True`` if same, otherwise ``False``
        """

        if type(self.target) == str and 'all' == self.target:
            return True

        if type(self.target) == str and type(target) == str:
            if target == self.target:
                return True
            else:
                return False
        elif isinstance(self.target, PazBox) and isinstance(target, PazBox):
            if target == self.target:
                return True
            else:
                return False
        else:
            return False

    def __eq__(self, ev):
        """
        Compare two events
        """

        if type(ev) != PazEvent:
            return False
        if self.name == ev.name \
            and self.source == ev.source \
            and self.target == ev.target:
            return True
        else:
            return False


class PazBox(object):
    """
    Main GUI object.
    """

    class PazText(object):
        """
        Rich text object.
        """

        def __init__(self, ctx, text="", config={ }):
            """
            Constructor

            :arg PazBox ctx: The parent ``PazBox`` of the text object.
            :arg str text: Raw text with style info to be parsed.
            :arg dict config: Text properties.
            """

            #: Reference to the GUI element contains text.
            self._ctx = ctx
            #: Holds parsed text in which styling info is removed.
            self._text = ''
            #: Holds original text with style info.
            self._raw_text = ''
            self._style_map = dict()

            # Default configuration
            self._config = {
                'tab-length': 4,
                'rich': False,
            }

            for cfg in config:
                self._config[cfg] = config[cfg]

            # Rows of text are created after parsing.
            self._rows = list()
            # Bidirection mapping of the characters in parsed text.
            # It is used to get index of character from terminal position
            # and vice versa.
            self._pos_bimap = dict()
            # Text cursor position.
            self._cursor_pos2 = (-1, -1)

            # Set cursor style to default if it is not provided in ``config``.
            if type(self._config['cursor']) == dict:
                if 'bg' not in self._config['cursor']:
                    self._config['cursor']['bg'] = 'black'
                if 'fg' not in self._config['cursor']:
                    self._config['cursor']['fg'] = 'gray'

                self._cursor_style = self._config['cursor']['fg'] \
                    + '_on_' + self._config['cursor']['bg']
            else:
                self._cursor_style = 'normal'

            self._ws_re = re.compile(r'\s+')

            self.set(text)

        def _pos_bimapper(self, map_in, map_out=None):
            """
            Transform the text index to row column index and vice versa.

            :arg int_or_tuple map_in: Key which can be an index or
                                      (``x``, ``y``) coordinate.
            :arg int_or_tuple map_out: Value which is similar to ``map_in``.
            :return int_or_tuple: Returns ``None`` if ``map_out`` is not None.
                                  Returns the value in ``self._pos_bimap`` which
                                  corresponds to the key ``map_in``.
            """
            if map_out != None:
                if (type(map_in) == int and type(map_out) == tuple \
                    and len(map_out) == 2) \
                    or (type(map_out) == int and type(map_in) == tuple \
                    and len(map_in) == 2):
                    self._pos_bimap[map_in] = map_out
                    self._pos_bimap[map_out] = map_in
                else:
                    raise RuntimeError('Invalida argument is given'
                        ' to _pos_bimapper.')

                return None
            elif map_in in self._pos_bimap:
                return self._pos_bimap[map_in]
            else:
                return None

        def _update_rows(self):
            """
            Convert text string into rows which will be
            printed in the corresponding ``PazBox``.
            """

            self._rows.clear()
            rect = list(self._ctx.get_style('rect'))
            margin = self._ctx.get_margin()
            (w, h) = (
                rect[2] - margin[1] - margin[3],
                rect[3] - margin[0] - margin[2])

            lines = self._text.split('\n')

            text_ind = 0
            for line in lines:
                self._pos_bimapper(text_ind, (0, len(self._rows)))
                row = ''

                words = line.split(' ')
                for word in words:
                    word += ' '

                    lr = len(row)
                    lw = len(word)

                    remaining_cols = w - lr

                    if lw <= remaining_cols:
                        row += word
                    else:
                        self._rows.append(row)

                        self._pos_bimapper(text_ind, (0, len(self._rows)))
                        if lw <= w:
                            row = word
                        else:
                            row = word[:w]

                    text_ind += lw

                text_ind += 1

                self._rows.append(row)

        def set(self, text=''):
            """
            Set ``self._raw_text`` and parse the style information
            if ``PazText`` object is a rich text object.

            :arg str text: Raw text string.
            """

            self._raw_text = text

        def get(self, raw=True):
            """
            Returns ``_raw_text`` or parsed text.

            :arg bool raw: Returns ``_raw_text`` if it is ``True``.

            :return str: Text string.
            """

            if raw:
                return self._raw_text
            else:
                return self._text

        def rows(self, row_ind=None):
            if row_ind == None:
                return self._rows
            else:
                return self._rows[row_ind]

        def get_text_style(self, col, row):
            """
            Get style of the character at position (col, row).

            :arg col int: Column index.
            :arg row int: Row index.

            :return str: Style string.
            """

            style = 'normal'

            for i in range(row, -1, -1):
                text_ind = self._pos_bimapper((0, i))
                if text_ind == None:
                    continue

                for j in range(col, -1, -1):
                    text_ind2 = text_ind + j
                    if text_ind2 in self._style_map:
                        style = '_'.join(self._style_map[text_ind2])
                        if style == '':
                            style == 'normal'

            return style

        def modify_by_cursor(self, mod, overwrite=False):
            self.modify(mod, self.get_cursor_pos(False), overwrite)

        def modify(self, mod, pos, overwrite=False):
            """
            Modify the text at given position by appending,
            mergin or overwriting.

            NOTE: Rich text modification is not supported yet.

            :arg str mod: String to be added.
            :arg int_or_tuple pos: Position of the place to be modified
                                   in terms of string index (int) or screen
                                   position (``x``, ``y``) <=> (col, row).
            :arg bool overwrite: If True overwrite starting from `pos` else
                                 append text to `pos`.
            """

            if self._config['rich'] == True:
                raise RuntimeError('Rich texts are not modifiable.')

            ind = -1
            if type(pos) == int:
                ind = pos
            elif type(pos) == tuple and len(pos) == 2:
                row_start_ind = self._pos_bimapper((0, pos[1]))
                if row_start_ind == None:
                    # TODO: This means that new lines must be appended.
                    raise RuntimeError('Incorrect usage of \'PazText.modify\'.')
                else:
                    ind = row_start_ind + pos[0]
            else:
                raise RuntimeError('Incorrect usage of \'PazText.modify\'.')

            if ind < 0:
                raise RuntimeError('Incorrect usage of \'PazText.modify\'.')

            if not overwrite:
                self._raw_text = self._raw_text[:ind] + mod \
                    + self._raw_text[ind:]
            else:
                l1 = len(mod)
                self._raw_text = self._raw_text[:ind] + mod \
                    + self._raw_text[ind+len(mod):]

        def parse(self):
            """
            Parse formatted rich text and extract styling information.
            """

            def parse_recursion(el, text_len, style_stack):
                style = el.get('style')
                if style:
                    style_stack.append(style)
                else:
                    style_stack.append('')

                self._style_map[text_len] = list(style_stack)
                text = el.text if el.text else ''
                text_len += len(text)

                for child in el:
                    style_stack_size = len(style_stack)
                    text += parse_recursion(child, text_len, style_stack)
                    del style_stack[style_stack_size:]
                    text_len = len(text)

                self._style_map[text_len] = list(style_stack)
                text += el.tail if el.tail else ''

                return text

            if self._raw_text:
                tmp_raw_text = self._raw_text.replace('\t',
                    self._config['tab-length'] * ' ')

                tree = ET.fromstring('<t>' + tmp_raw_text + '</t>')
                self._text = parse_recursion(tree, 0, [])

                self._update_rows()

        def move_cursor(self, delta):
            """
            Move cursor by delta points.

            :arg tuple delta: Position change in (``x``, ``y``) coordinates
            :return tuple: New cursor position
            """

            # Global position of the cursor.
            pos = list(self.get_cursor_pos())
            z = self._ctx.get_style('z-index')

            frame_buffer = self._ctx.buffer()
            # Remove cursor style at current cursor position.
            frame_buffer.rm_tmp_style(pos[0], pos[1], z)

            # Change cursor position.
            pos[0] += delta[0]
            pos[1] += delta[1]
            # Set cursor style at new position.
            frame_buffer.set_tmp_style(pos[0], pos[1], z, self._cursor_style)

            self.set_cursor_pos(tuple(pos))

            return self.get_cursor_pos()

        def get_cursor_pos(self, abs_pos=True):
            pos = self._cursor_pos2
            if abs_pos:
                origin = self._ctx.position_helper('origin')

                return (pos[0] + origin[0], pos[1] + origin[1])
            else:
                return pos

        def set_cursor_pos(self, pos, abs_pos=True):
            if abs_pos:
                origin = self._ctx.position_helper('origin')

                self._cursor_pos2 = (pos[0] - origin[0], pos[1] - origin[1])
            else:
                self._cursor_pos2 = pos


    INF = float('inf')
    name = ""
    style = { }
    text = ""
    DRAW_ALL = 1
    DRAW_DIFF = 2
    DRAW_END_OF_TEXT = 3
    def __init__(self, buff, par=None, path=''):
        """
        Constructor.

        :arg pazgui.FrameBuffer buff: Reference to frame buffer object.
        :arg pazgui.PazBox par: Reference to parent box
        """

        self._buffer = buff
        self.scheduler = schedule
        self._children_list = []
        self._parent = par
        self._style = {
            'z-index': -self.INF,
            'visible': True,
            'border': False,
            'rect': (0, 0, 1, 1),
             # margin: (top, right, bottom, left)
            'margin': (0, 0, 0, 0),
            'active': False,
            'scroll-pos': (0, 0),
            'scroll-x': True,
            'scroll-y': True,
            'background': u' ',
            'text': {
                'rich': False,
                'cursor': None,
            },
        }
        for sty in self.style:
            self.set_style(sty, self.style[sty])

        self._path = path
        self._name = self.name
        # PazText object
        self._text = None
        self._behaviour = [PazBehaviour(self)]
        self._create()
        self._child_index = 1
        self._children()
        self.schedule()

    def _resize(self, box=None):
        if box == None:
            box = self

        box.resize()

        for child in box.child('all'):
            self._resize(child)

    def _create(self):
        """
        First section of this function iterates through `PazBehaviour`
        based classes in the style dictionary and creates instances of
        them. Then, it appends those instances into `self._behaviour`
        list. By this way, different type of behaivour can be possesed
        by a base `PazBox` object. This is the method to extend `PazBox`
        class to give it different attributes: textarea attribute,
        button attribute etc.

        Second section...
        """

        # 1)
        #
        behaviour = self.get_style('behaviour')
        if type(behaviour) == list:
            # Iterate through `PazBehaviour` classes.
            for bhv in behaviour:
                # Create an instance of `PazBehaviour` class.
                bhv_instance = bhv(self)
                # Append to the behaviour list.
                self._behaviour.append(bhv_instance)

        # 2)
        #
        # This is the first behaviour call in `PazBox` object.
        self._run_behaviour('pre_create')

        # Everything must be drawn initially.
        self.__draw_flags = { 'all': 1 }

        # Copy the info in `self.style` to `self._style`.
        style_keys = list(self._style.keys())
        for sty in style_keys:
            if sty == 'rect':
                # Before style info, 'rect', will be modified, it is saved
                # to 'original-rect'.
                self.set_style('original-rect', self.get_style(sty))
            elif sty == 'margin':
                self.set_style('original-margin', self.get_style(sty))
            elif sty == 'active':
                if self.get_style(sty):
                    self.activate()
            elif sty == 'z-index':
                zindex = self.get_style(sty)
                if zindex == -self.INF:
                    if self._parent != None:
                        pzindex = self._parent.get_style(sty)
                        # 'z-index' is parents 'z-index' plus 1, if it is
                        # not defined in the style.
                        self.set_style(sty, pzindex + 1)
                    else:
                        self.set_style(sty, 0)
            elif sty == 'background':
                bg = self.get_style(sty)

                # If bg is more than a character, it may hold style
                # info for the background.
                if len(bg) > 1:
                    at_ind = bg.find(u'@')
                    # There is no style info.
                    if at_ind < 0:
                        self.set_style('background-character', bg[0])
                        continue

                    paro_ind = bg[at_ind:].find(u'(')
                    if paro_ind < 0:
                        self.set_style('background-character', bg[0])
                        continue

                    self.set_style('background-character', bg[at_ind+paro_ind+1])
                    self.set_style('background-style', bg[at_ind+1:paro_ind])
                    # Text background also should have the same style
                    # ~ self.set_text(u'@' + bg[at_ind+1:paro_ind] + u'(' + self.text + u')')
                elif len(bg) == 1:
                    self.set_style('background-style', 'normal')
                    self.set_style('background-character', bg)
            elif sty == 'text':
                self._text = self.PazText(self, self.text, self.get_style(sty))

        self._run_behaviour('post_create')

    def _run_behaviour(self, fcn_name, params=None):
        ret = False
        for bhv in self._behaviour:
            if hasattr(bhv, fcn_name):
                 ret |= bool(getattr(bhv, fcn_name)(params))

        return ret

    def _children(self):
        child_classes = self.children()

        if child_classes == None:
            return None

        children = []
        for cls in child_classes:
            instance = cls(self._buffer, par=self, path=self.get_path())
            self.add_child(instance)

        return children

    def _draw_xy(self, x, y, val):
        self._buffer.set_xy(x, y, val)

    def _draw_text(self):
        self._text.parse()
        clip = self.position_helper('clip')

        '''Calculate screen coordinates of content area'''
        crect = self.get_style('content-rect')
        (sx, sy) = self.get_style('scroll-pos')
        margin = self.get_margin()

        dx = clip.clipped[0] - margin[3] + sx
        dy = clip.clipped[1] - margin[0] + sy

        xstart = clip.area[0] - dx
        ystart = clip.area[1] - dy
        xend = xstart + crect[2]
        yend = ystart + crect[3]

        rows = self._text.rows()
        _y = 0
        for row in rows:
            _x = 0
            for c in row:
                x = xstart + _x
                y = ystart + _y

                if x >= clip.area[0] and x < clip.area[2] \
                    and y >= clip.area[1] and y < clip.area[3]:
                    self.draw_xy(x, y, c, 'text')
                    self._draw_text_style(_x, _y, x, y)

                _x += 1
            _y += 1

    def _draw_text_style(self, col, row, x, y):
        style = self._text.get_text_style(col, row)
        if style != None:
            self.draw_style(x, y, style)
            self.__last_style = style
        else:
            try:
                self.draw_style(x, y, self.__last_style)
            except AttributeError:
                pass

    def _draw_border(self):
        """
        Draws border around the box if it is defined in the box style.
        """

        # Return if border style is not defined
        if self.get_style('border') == False:
            return

        # Get the rectangle in which the `PazBox` lays in local coordinates.
        rect = self.get_style('rect')
        # Get how many characters the rectangle clipped from all sides.
        clip = self.position_helper('clip')

        xb = (0, rect[2] - 1)
        yb = (0, rect[3] - 1)
        for x in range(rect[2]):
            # Do not print the clipped parts
            if x < clip.clipped[0] or x >= rect[2] - clip.clipped[2]:
                continue

            for y in range(rect[3]):
                # Do not print the clipped parts
                if y < clip.clipped[1] or y >= rect[3] - clip.clipped[3]:
                    continue

                # Transform it into global coordinates
                _x = clip.area[0] + x - clip.clipped[0]
                _y = clip.area[1] + y - clip.clipped[1]

                drawn = True
                # Upper left corner
                if x == xb[0] and y == yb[0]:
                    self.draw_xy(_x, _y, _c.ULCORNER, 'border')
                # Lower left corner
                elif x == xb[0] and y == yb[1]:
                    self.draw_xy(_x, _y, _c.LLCORNER, 'border')
                # Upper right corner
                elif x == xb[1] and y == yb[0]:
                    self.draw_xy(_x, _y, _c.URCORNER, 'border')
                # Lower right corner
                elif x == xb[1] and y == yb[1]:
                    self.draw_xy(_x, _y, _c.LRCORNER, 'border')
                # Left and right sides
                elif (x == xb[0] or x == xb[1]) and y != yb[0] and y != yb[1]:
                    self.draw_xy(_x, _y, _c.VLINE, 'border')
                # Top and bottom sides
                elif (y == yb[0] or y == yb[1]) and x != xb[0] and x != xb[1]:
                    self.draw_xy(_x, _y, _c.HLINE, 'border')
                else:
                    drawn = False

                # Border style has not been implemented yet.
                # TODO: Implement border style.
                if drawn == True:
                    self.draw_style(_x, _y, 'normal')

    def _draw_background(self):
        """
        Draws background of the `PazBox` object. Background is defined
        as a character and style information.
        """

        clip = self.position_helper('clip')
        # Get visible area of the box.
        # Area is a rectangle given by (x1, y1, x2, y2)
        area = list(clip.area)
        # Get the character will be printed as background.
        c = self.get_style('background-character')

        # If the box has border, then the background area is
        # shrinked for 1 character from all sides.
        if self.get_style('border') == True:
            if clip.clipped[0] == 0:
                area[0] += 1
            if clip.clipped[1] == 0:
                area[1] += 1
            if clip.clipped[2] == 0:
                area[2] -= 1
            if clip.clipped[3] == 0:
                area[3] -= 1

        # Get background style.
        bg_style = self.get_style('background-style')

        # Iterate through box area and print bg character and style.
        for y in range(area[1], area[3]):
            for x in range(area[0], area[2]):

                # `area[2]` is the x coordinate of the right
                # side of the rectangle. If bg is styled, style should
                # change back to normal when the box ends.
                if x == area[2] - 1:
                    self.draw_style(x + 1, y, 'normal')

                # TODO: Instead of printing style for each character
                # It can be done by printing in the beginning of line
                if bg_style != 'normal':
                    self.draw_style(x, y, bg_style)

                self.draw_xy(x, y, c, 'background')

    def _setup_draw(self):
        for bhv in self._behaviour:
            bhv.setup_draw()

        if self._text:
            self.__text_whitespace_pattern = re.compile(r'\s+')

    def _cleanup_draw(self):
        for bhv in self._behaviour:
            bhv.cleanup_draw()

        for flag in self.__draw_flags:
            self.__draw_flags[flag] = 0

    def _event(self, ev):
        ret = self._run_behaviour('pre_event', { 'ev': ev })
        #
        if ev.is_target(self):
            ret |= bool(self.event(ev))
        #
        ret |= self._run_behaviour('post_event', { 'ev': ev })

        return ret

    @staticmethod
    def _scheduled(func):
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)
            # First item in `args` list is a reference to
            # the instance where the event is scheduled.
            _self = args[0]
            # Create an event and propagate.
            ev = PazEvent('SCHEDULED', _self, target='/root')
            _self.propagate_event(ev)

        return wrapper

    def child(self, index):
        if type(index) == str and index == 'all':
            return self._children_list
        elif index < 0 or index >= self.children_count():
            return None

        return self._children_list[index]

    def get_path(self):
        return self._path + '/' + self._name

    def follow_path(self, path):
        root = self
        while root._parent != None:
            root = root._parent

        names = path.split('/')
        for name in names[2:]:
            if len(name) == 0:
                continue
            children = root.child('all')
            found = False
            for child in children:
                if name == child.get_name():
                    root = child
                    found = True
                    break

            if found == False:
                return None

        return root

    def set_name(self, name):
        self._name = name

    def get_name(self):
        return self._name

    def children_count(self):
        return len(self._children_list)

    def resize(self):
        """
        Adjust size of the box according to *rect* in *style* data.

        Calculates content rectangle with respect to its parent object.
        """

        self._run_behaviour('pre_resize')

        orect = self.get_style('original-rect')

        if self._parent != None:
            par_content_rect = self._parent.get_style('content-rect')
        else:
            par_content_rect = (0, 0, 0, 0)

        rect_tmp = [0] * 4
        for i in range(len(orect)):
            v = orect[i]
            par_content_rect_i = par_content_rect[(i % 2) + 2]
            if type(v) == float:
                v = max(0.0, v)
                u = int(round(par_content_rect_i * v))
            else:
                u = v

            rect_tmp[i] = u

        rect = tuple(rect_tmp)
        self.set_style('rect', rect)

        margin = self.get_margin()

        content_rect = (
            rect[0] + margin[3], rect[1] + margin[0],
            rect[2] - margin[1] - margin[3],
            rect[3] - margin[2] - margin[0]
        )
        self._style['content-rect'] = content_rect

        self.__row_length = content_rect[2]

        # Recalculate these after resize
        # To save computation time
        self.__clip = self.clip()
        self.__origin = self.to_global(0, 0)

        self.draw_flag('background', 1)
        self.draw_flag('border', 1)

        self._run_behaviour('post_resize')

    def to_global(self, x, y):
        """
        Translate local position in a box to global terminal
        coordinates.

        :arg int x: Position in horizontal direction
        :arg int y: Position in vertical direction
        :arg bool margin: Default value is False. If True, adds box margin.

        :return tuple: Global (`x`,`y`) coordinates.
        """

        rect = self.get_style('rect')
        if self._parent != None:
            pscroll = self._parent.get_style('scroll-pos')
            pmargin = self._parent.get_margin()
        else:
            pscroll = (0, 0)
            pmargin = (0, 0, 0, 0)

        x += rect[0] - pscroll[0] + pmargin[3]
        y += rect[1] - pscroll[1] + pmargin[0]


        if self._parent != None:
            (gx, gy) = self._parent.to_global(x, y)
        else:
            (gx, gy) = (x, y)

        return (gx, gy)

    def add_child(self, children):
        self._children_list.append(children)
        if 0 == len(children.name):
            children.set_name('child:{0}'.format(self._child_index))
            self._child_index += 1

    def get_style(self, name):
        if name in self._style:
            return self._style[name]
        else:
            return None

    def get_margin(self, wborder=True,wscroll=False):
        tot_margin = list(self.get_style('margin'))

        if wborder == True:
            border = self.get_style('border')
            if border == True:
                tot_margin = [val + 1 for val in tot_margin]

        if wscroll == True:
            scroll_pos = self.get_style('scroll-pos')
            tot_margin[3] -= scroll_pos[0]
            tot_margin[0] -= scroll_pos[1]

        return tuple(tot_margin)

    def set_style(self, name, sty):
        self._style[name] = sty

    def modify_text(self, mod, pos=None, overwrite=False):
        """
        Modify the text at given position by appending,
        mergin or overwriting.

        Actual implementation is in :meth:``self.PazText.modify``.
        """

        if pos == None:
            self._text.modify_by_cursor(mod, overwrite)
        else:
            self._text.modify(mod, pos, overwrite)

        self.draw_flag('background', 1)
        self.draw_flag('text', 1)

    def set_text(self, text):
        self._text.set(text)
        self.draw_flag('text', 1)
        self.draw_flag('background', 1)

    def get_text(self, raw=True):
        return self._text.get(raw)

    def move_text_cursor(self, delta):
        return self._text.move_cursor(delta)

    def buffer(self):
        return self._buffer

    def scroll(self, count):
        scroll_pos = self.get_style('scroll-pos')
        self.set_style('scroll-pos', (scroll_pos[0] + count[0], \
                                      scroll_pos[1] + count[1]))

        self._resize()

    def children(self):
        pass

    def schedule(self):
        pass

    def draw_style(self, x, y, style):
        """
        Add drawing style to for the character at (`x`, `y`)
        into the frame buffer.

        :arg int x: `x` position
        :arg int y: `y` position
        :arg str style: Style information
        """

        z = self.get_style('z-index')
        current_style = self._buffer.set_style(x, y, z, style)

    def draw_xy(self, x, y, val, w='', params=None):
        """
        Draw character in `val` to the point (`x`, `y`) on the terminal.

        :arg int x: `x` position
        :arg int y: `y` position
        :arg chr val: Character to be printed
        :arg str w: Indicates which drawing function it is called from.
        :arg dict params: Extra parameters for the behaviour function
        """

        self._run_behaviour('pre_draw_' + w, Bunch(x=x, y=y, val=val, extra=params))
        # **
        self._draw_xy(x, y, val)
        # **
        self._run_behaviour('post_draw_' + w, Bunch(x=x, y=y, val=val, extra=params))

    def position_helper(self, pos_type='origin'):
        """
        In order to make screen refreshing faster, important global
        positions on the terminal is saved to these variables. They
        will only change when screen is resized, after scrolling or
        adding/removing boxes etc.

        :arg str pos_type: The name of the important position.
        :return tuple: A tuple (`x`, `y`) representing the coordinates
                       on the terminal screen.
        """
        result = None
        try:
            if pos_type == 'origin':
                result = self.__origin
            elif pos_type == 'clip':
                result = self.__clip
        except AttributeError:
            if pos_type == 'origin':
                result = self.to_global(0, 0)
            elif pos_type == 'clip':
                result = self.clip()

        return result

    def draw_flag(self, f, v=None):
        """
        Set draw flags to trigger draw action for gui parts
        in the next turn.

        :arg str f: Flag name which can be
            'background', 'border', 'text', 'all'.
        :arg int v: Setting it to `1` triggers draw action in the next turn.
        """

        if v == None:
            if self.__draw_flags['all'] > 0:
                return self.__draw_flags['all']
            elif f in self.__draw_flags:
                return self.__draw_flags[f]
            else:
                return 0
        elif type(v) == int:
            self.__draw_flags[f] = v
            if v > 0:
                ev = PazEvent('DRAW', source=self, target='/root')
                self.event_queue(ev)
        else:
            return 0

    def event_queue(self, ev):
        root = self.follow_path('/root')
        root.event_queue(ev)

    def exit(self):
        self._parent.exit()

    def clipped_pos(self):
        '''
        Returns visible rectangle of the box in global (screen) coordinates.

        :rtype: tuple
        :returns: Returns 4 tuple holds start and end points of rectangle
        '''
        clip_rect = self.clip()
        if clip_rect == None:
            return (-1, -1, -1, -1)

        pos = self.to_global(0, 0)
        rect = self.get_style('rect')

        c = self.get_style('background')

        xstart = pos[0] + clip_rect[0]
        xend = xstart + clip_rect[2] - clip_rect[0]

        ystart = pos[1] + clip_rect[1]
        yend = ystart + clip_rect[3] - clip_rect[1]

        return (xstart, ystart, xend, yend)

    def clip(self, add_margin=False):
        """
        Calculate intersection of box rect and parent box rect.

        :arg bool add_margin: Calculate clipped area by considering
                              margin if `add_margin` is `True`.
        :return tuple: Returns 4 tuple reprsents the intersection
        """

        rect = self.get_style('rect')

        if add_margin == True:
            margin = self.get_margin()
        else:
            margin = (0, 0, 0, 0)

        if self._parent == None:
            origin = (rect[0] + margin[3], rect[1] + margin[0])

            size = (
                rect[2] - margin[3] - margin[1],
                rect[3] - margin[2] - margin[0])

            area = (
                origin[0], origin[1],
                origin[0] + size[0], origin[1] + size[1])

            clipped = (0, 0, 0, 0)

            return Bunch(area=area, clipped=clipped)
        else:
            pclip = self._parent.clip(True)
            if not pclip:
                # This means the parent is not in the visible area.
                return None

            parea = pclip.area
            pscroll = self._parent.get_style('scroll-pos')

        gorigin = list(self.position_helper('origin'))

        gend = [
            gorigin[0] + rect[2] - margin[1],
            gorigin[1] + rect[3] - margin[2]]

        gorigin[0] += margin[3]
        gorigin[1] += margin[0]

        if gend[0] < parea[0] or gend[1] < parea[1] \
            or gorigin[0] > parea[2] or gorigin[1] > parea[3]:
                return None

        dx1 = abs(min(gorigin[0] - parea[0], 0))
        dy1 = abs(min(gorigin[1] - parea[1], 0))
        dx2 = abs(max(gend[0] - parea[2], 0))
        dy2 = abs(max(gend[1] - parea[3], 0))

        # area is defined as a rectangle (x1, y1, x2, y2)
        # Coordinates of top left corner is (x1, y1)
        # and right bottom corner is (x2, y2)
        area = (
            max(gorigin[0], parea[0]), max(gorigin[1], parea[1]),
            min(gend[0], parea[2]), min(gend[1], parea[3]))

        clipped = (dx1, dy1, dx2, dy2)

        return Bunch(area=area, clipped=clipped)

    def draw(self):
        self._setup_draw()
        if self.get_style('visible'):
            if self.draw_flag('background') > 0:
                self._draw_background()

            if self.draw_flag('text') > 0:
                self._draw_text()

            if self.draw_flag('border') > 0:
                self._draw_border()

        self._cleanup_draw()

    def deactivate(self):
        self._style['active'] = False

    def activate(self, box=None):
        """
        Activates box and declares it to main :class:`PazGui` object recursively.
        It is used without an argument.

        :arg PazGui box: Not used. It is only used for recursion.
        """

        if box == None:
            self._style['active'] = True
            self._parent.activate(self)
        else:
            self._style['active'] = False
            self._parent.activate(box)

    def propagate_event(self, ev):
        ret = self._event(ev)
        if ret == True:
            return True

        for child in self.child('all'):
            ret = child.propagate_event(ev)
            if ret == True:
                return True

    def event(self, ev):
        pass


class PazGui(PazBox):
    """
    Main GUI class. It inheriths :class:`.PazBox`.
    Holds the main loop. Checks inputs and events, redraws screen.
    """

    def __init__(self, box_cls, config={ }, name='', stream=None):
        """
        Initialize PazGui.

        :arg PazBox box_cls: Root PazBox class to be instanced.

        :arg dict config: Holds gui configuration.

        :arg str name: Name of the application.

        :arg io.StringIO stream: A stream object to redirect framebuffer output
            to a file or an other sink.
        """

        init_logger(__file__)

        if stream == None:
            self._term = Terminal()
        else:
            self._term = Terminal(stream=stream)

        self._config = {
            'key-timeout': 0.05,
            'loop-wait': 0.01,
        }
        for n in config:
            self._config[n] = config[n]

        self._frame_buffer = FrameBuffer(self._term)
        super().__init__(buff=self._frame_buffer, par=None)

        self.set_style('z-index', 0)
        self._event_queue = []
        self._active_box = None
        self._flags = {  }
        self._captured_sys_signals = [signal.SIGWINCH]
        self._set_sys_signals()

        self._path = '/'
        if len(name) == 0:
            self._name = 'root'

        box = box_cls(self._frame_buffer, self)
        self.add_child(box)
        self.gui_resize()

        self._terminate = False
        self.width = self._term.width
        self.height = self._term.height

    def get_config(self, name):
        if name in self._config:
            return self._config[name]
        else:
            return None

    def gui_resize(self):
        self.set_style('rect', (0, 0, self._term.width, self._term.height))
        self.set_style('original-rect', self.get_style('rect'))
        self.set_style('original-margin', self.get_style('margin'))

        self._resize()

    def _set_sys_signals(self):
        for sig in self._captured_sys_signals:
            signal.signal(sig, self._sys_signal_handler)

        self._captured_sys_signals.clear()

    def _sys_signal_handler(self, signum, frame):
        pending_signals = signal.sigpending()
        if signum in pending_signals:
            return

        self.event_queue(PazEvent(signal.Signals(signum).name, source='SYS', target=self))

    def _kbd_input(self):
        inp = self._term.inkey(timeout=self._config['key-timeout'])
        if not inp:
            ev = None
        elif inp.is_sequence:
            ev = PazEvent(inp.name, source='KBD')
        else:
            ev = PazEvent(str(inp), source='KBD')

        self.event_queue(ev)

    def event_queue(self, ev=None):
        if type(ev) == PazEvent:
            self._event_queue.append(ev)
        elif ev == None:
            if len(self._event_queue) > 0:
                return self._event_queue.pop(0)
            else:
                return None

    def _process_events(self):
        update = False
        ev = self.event_queue()

        if ev != None:
            update = self.propagate_event(ev)

        return update

    def _process_inputs(self):
        self._kbd_input()

    def _loop_cleanup(self):
        self._set_sys_signals()

    def exit(self):
        self._terminate = True

    def run(self):
        with self._term.fullscreen(), self._term.location(x=0, y=0),\
             self._term.raw(), self._term.keypad(),\
             self._term.hidden_cursor():
            self.draw()
            self.update()

            while not self._terminate:
                self._process_inputs()
                self.scheduler.run_pending()
                updated = self._process_events()

                if updated:
                    self.draw()
                    self.update()
                else:
                    time.sleep(self._config['loop-wait'])

                self._loop_cleanup()

    def update(self):
        self._frame_buffer.update()

    def draw(self, box=None):
        if box == None:
            box = self

        for child in box.child('all'):
            child.draw()
            self.draw(child)

    def activate(self, box=None):
        """
        Changes active box after deactivating current active box.

        :arg PazBox box: PazBox that is activated.
        """
        if self._active_box != None:
            self._active_box.deactivate()

        self._active_box = box

    def _event(self, ev):
        ret = self._run_behaviour('pre_event', { 'ev': ev })
        #
        if hasattr(self, '_gui_event'):
            ret |= bool(self._gui_event(ev))

        if ret == False and ev.is_target(self):
            ret |= bool(self.event(ev))
        #
        ret |= self._run_behaviour('post_event', { 'ev': ev })

        return ret

    def _gui_event(self, ev):
        if ev.cmp('SIGWINCH'):
            self._frame_buffer.resize()
            self.gui_resize()
            return True
        elif ev.cmp('DRAW'):
            self._flags['DRAW'] = True
            return True
        elif ev.cmp(_c.CTRL_C):
            print('Exiting!')
            self.exit()
            return True
