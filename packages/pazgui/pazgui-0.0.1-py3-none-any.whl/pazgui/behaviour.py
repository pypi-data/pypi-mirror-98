class PazBehaviour(object):
    def __init__(self, ctx, mood='normal', attr={ }):
        self._mood = mood
        self._attributes = dict(attr)
        self._ctx = ctx

    def mood(self, m=None):
        if m == None:
            return self._mood
        else:
            self._mood = m

    def attribute(self, n, a=None):
        if n in self._attributes:
            if a == None:
                return self._attributes[n]
            else:
                self._attributes[n] = a
        else:
            return None

    def setup_draw(self, params=None):
        pass

    def cleanup_draw(self, params=None):
        pass

    def pre_draw_border(self, params):
        pass

    def post_draw_border(self, params):
        return
        clip_pos = self._ctx.position_helper('clip').area

        if params.x == clip_pos[0]:
            self._ctx.draw_style(params.x, params.y, 'normal')
        elif params.y == clip_pos[1] or params.y == clip_pos[0] + clip_pos[3] - 1:
            self._ctx.draw_style(params.x, params.y, 'normal')

    def pre_draw_background(self, params):
        pass

    def post_draw_background(self, params):
        pass

    def pre_draw_text(self, params):
        pass

    def post_draw_text(self, params):
        pass

    def pre_create(self, params=None):
        pass

    def post_create(self, params=None):
        pass

    def pre_resize(self, params=None):
        pass

    def post_resize(self, params=None):
        pass

    def pre_event(self, params):
        pass

    def post_event(self, params):
        active = self._ctx.get_style('active')
        if active:
            ev = params['ev']

            if ev.cmp('KEY_UP'):
                self._ctx.scroll((-1, 0))
            elif ev.cmp('KEY_DOWN'):
                self._ctx.scroll((1, 0))


class CheckboxBehaviour(PazBehaviour):
    def __init__(self, ctx):
        super().__init__(ctx, mood='checkbox')
        self._checkbox_text = u'[ ]'
        self._checkbox_formatter = u'[{}]'
        self._checkbox_checker = u'x'
        self._checkbox_trigger = u' '

    def post_create(self, params=None):
        box_margin = self._ctx.get_style('margin')
        self._ctx.set_style('margin', (box_margin[0], box_margin[1], box_margin[2], box_margin[3] + 4))

        checker = self._ctx.get_style('checkbox.checker')
        if checker != None:
            self._checkbox_checker = checker
        else:
            self._ctx.set_style('checkbox.checker', self._checkbox_checker)

        # ~ print("checkkk")
        self.checked(not not self._ctx.get_style('checkbox.checked'))

        trigger = self._ctx.get_style('checkbox.trigger')
        if trigger != None:
            self._checkbox_trigger = trigger
        else:
            self._ctx.set_style('checkbox.trigger', self._checkbox_trigger)

    def checked(self, c=None):
        if c == None:
            return self._ctx.get_style('checkbox.checked')
        else:
            self._ctx.set_style('checkbox.checked', c)
            if c == True:
                self._checkbox_text = self._checkbox_formatter.format(self._checkbox_checker)
            else:
                self._checkbox_text = self._checkbox_formatter.format(u' ')
            return c

    def toggle(self):
        return self.checked(not self._ctx.get_style('checkbox.checked'))

    def setup_draw(self, params=None):
        clip = self._ctx.position_helper('clip')
        margin = self._ctx.get_margin()
        (sx, sy) = self._ctx.get_style('scroll-pos')

        xstart = clip.area[0] - clip.clipped[0] - sx
        ystart = clip.area[1] - clip.clipped[1] + margin[0] - sy

        self._ctx.draw_xy(xstart, ystart, self._checkbox_text[0])
        self._ctx.draw_xy(xstart + 1, ystart, self._checkbox_text[1])
        self._ctx.draw_xy(xstart + 2, ystart, self._checkbox_text[2])

    def post_event(self, params):
        ev = params['ev']

        if self._ctx.get_style('active') == True:
            if ev.cmp(self._checkbox_trigger):
                self.toggle()
                self._ctx.draw_flag('text', 1)
                return True


class HBoxBehaviour(PazBehaviour):
    def __init__(self, ctx, mood='hbox'):
        super().__init__(ctx, mood=mood)
        self._next_child_rect_start = None
        self._rect = None
        self._spacing = None
        self._children_count = None
        self._rect_index = 0

    def post_resize(self, params=None):
        self._rect = self._ctx.get_style('rect')
        c_cnt = self._ctx.children_count()
        self._children_count = c_cnt
        self._next_child_rect_start = self._rect[self._rect_index]

        ratios = []
        for i in range(c_cnt):
            ratio = self._ctx.child(i).get_style('stretch-ratio')
            ratios.append(ratio)

        total_ratio = 0.0
        for i in range(c_cnt):
            ratio = ratios[i]
            if type(ratio) == float or type(ratio) == int:
                ratios[i] = max(0.0, float(ratio))
                total_ratio += ratios[i]
            else:
                ratios[i] = 0.0

        if total_ratio == 0.0:
            total_ratio = 1.0

        spacing = self._ctx.get_style('spacing')
        if spacing == None:
            self._spacing = 0
        else:
            self._spacing = spacing

        i = 0
        for ratio in ratios:
            scaled_ratio = ratio / total_ratio
            self.set_size(i, scaled_ratio)
            i += 1

    def set_size(self, index, ratio):
        crect = [0] * 4
        width = round(ratio * self._rect[2])

        if index == self._children_count - 1:
             width += self._rect[2] - (self._next_child_rect_start + width)

        crect[0] = self._next_child_rect_start / self._rect[2]
        crect[2] = width / self._rect[2]
        crect[1] = 0.0
        crect[3] = 1.0

        self._next_child_rect_start += width

        self._ctx.child(index).set_style('original-rect', crect)


class VBoxBehaviour(HBoxBehaviour):
    def __init__(self, ctx, mood='vbox'):
        super().__init__(ctx, mood=mood)
        self._rect_index = 1

    def set_size(self, index, ratio):
        crect = [0] * 4
        width = round(ratio * self._rect[3])

        if index == self._children_count - 1:
             width += self._rect[3] - (self._next_child_rect_start + width)

        crect[1] = self._next_child_rect_start / self._rect[3]
        crect[3] = width / self._rect[3]
        crect[0] = 0.0
        crect[2] = 1.0

        self._next_child_rect_start += width

        self._ctx.child(index).set_style('original-rect', crect)


class TextBoxBehaviour(PazBehaviour):
    def __init__(self, ctx, mood='textbox'):
        super().__init__(ctx, mood=mood)

    def post_create(self, params=None):
        self.set_style('border', True)
        rect = self.get_style('original-rect')
        self.set_style('original-rect', (rect[0], rect[1], rect[2], 1))
        self.set_style('margin', (0, 0, 0, 0))
        self.set_style('background', u' ')


class TextEditBehaviour(PazBehaviour):
    def __init__(self, ctx, mood='textedit'):
        super().__init__(ctx, mood=mood)
        self.__cursor_pos = (0, 0)
        self._accepted_nonprintable_keys = [
            'KEY_UP', 'KEY_DOWN', 'KEY_RIGHT', 'KEY_LEFT',
            'KEY_ENTER', 'KEY_TAB']

    def pre_create(self, params=None):
        text_style = self._ctx.get_style('text')
        text_style['rich'] = False

    def _filter_input(self, ev):
        """
        Filter keyboard inputs. Only accepts
        printable characters and the ones in
        :py:attr:`self._accepted_nonprintable_keys`.

        :arg PazEvent ev: Event object.
        :return PazEvent: Same event if passes from filter, returns None otherwise.
        """

        if ev.name:
            if ev.name.isprintable():
                return ev
            elif ev.name in self._accepted_nonprintable_keys:
                return ev
            else:
                return None

    def pre_event(self, params):
        raw_ev = params['ev']
        ev = self._filter_input(raw_ev)

        if ev:
            if ev.cmp('KEY_DOWN'):
                self._ctx.move_text_cursor((0, 1))
            elif ev.cmp('KEY_LEFT'):
                self._ctx.move_text_cursor((-1, 0))
            elif ev.cmp('KEY_RIGHT'):
                self._ctx.move_text_cursor((1, 0))
            elif ev.cmp('KEY_UP'):
                self._ctx.move_text_cursor((0, -1))
            elif ev.isprintable():
                self._ctx.modify_text(ev.name)

            return True

