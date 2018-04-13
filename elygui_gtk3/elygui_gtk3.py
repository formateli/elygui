# This file is part of ElyGui project.
# The COPYRIGHT file at the top level of this repository
# contains the full copyright notices and license terms.

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk


class ElyGuiGtk3(object):
    def __init__(self, gui_def):

        css = self._get_css(gui_def)
        style_provider = Gtk.CssProvider()
        style_provider.load_from_data(css.encode('utf8'))
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        win = WindowForm(gui_def, 'main.main_form')
        win.show_all()
        Gtk.main()

    def _get_css(self, gui_def):
        css = ''
        for st in gui_def.styles_list:
            c = '.' + st.name + '{'
            c += self._get_css_pair('color', 'font_color', st)
            c += self._get_css_pair('font-size', 'font_size', st)
            css += c + '}'
        return css

    def _get_css_pair(self, css_name, st_name, st):
        val = getattr(st, st_name)
        if val is None:
            return ''
        return ' ' + css_name + ': ' + val + ';'


class WindowForm(Gtk.Window):

    hide_forms = {}

    def __init__(self, gui_def, form_id):
        self.gui_def = gui_def
        self.controls = {}
        self.id = form_id

        frm = gui_def.get_form(form_id)

        if frm is None:
            raise Exception("Form '{0}' not found.".format(
                form_id))

        Gtk.Window.__init__(self, title=frm.title)

        for ctl in frm.controls:
            wg = self.get_widget(ctl)
            self.controls[ctl.id] = wg
            self.add(wg)

        self.set_decorated(False)
        self.set_destroy_with_parent(True)
        # TODO in config: self.set_keep_above(True)
        self.set_resizable(False)
        self.set_modal(True)

        #self.connect("delete-event", Gtk.main_quit)
        #self.show_all()

    def get_widget(self, wg_def):
        wg = None
        if wg_def.type_ in ['HBox', 'VBox']:
            if wg_def.type_ == 'HBox':
                wg = Gtk.HBox(spacing=6)
            else:
                wg = Gtk.VBox(spacing=6)
            for ctl in wg_def.controls:
                ch = self.get_widget(ctl)
                if ch:
                    wg.pack_start(ch, True, True, 0)
        if wg_def.type_ == 'Button':
            wg = Gtk.Button(label=wg_def.label)
            wg.connect("clicked", self.on_button_clicked)
        if wg_def.type_ == 'Entry':
            wg = Gtk.Entry()

        if wg:
            wg.set_property('name',
                wg_def.get_full_name())

            ctx = wg.get_style_context()
            if wg_def.style:
                ctx.add_class(wg_def.style)

            if wg_def.height is not None:
                wg.set_property("height-request", float(wg_def.height))
            if wg_def.width is not None:
                wg.set_property("width-request", float(wg_def.width))
            self.controls[wg_def.id] = wg

        return wg

    def on_button_clicked(self, widget):
        module, model, name = self.defrag_name(
            widget.get_property('name'))

        cls = self.gui_def.get_model_class(model)
        if cls is None:
            raise Exception(
                "Class for model '{0}' not found.".format(model))
        func = getattr(cls, 'button_' + name + '_clicked')
        res = func(self.gui_def._context)

        for r in res['next']:
            if r[0] == 'SHUTDOWN':
                Gtk.main_quit()
            if r[0] == 'OPEN_FORM':
                if r[1] in self.hide_forms:
                    frm = self.hide_forms[r[1]]
                else:
                    frm = WindowForm(self.gui_def, r[1])
                frm.set_transient_for(self)
                frm.show_all()
            if r[0] == 'CONTROL':
                ctl = self.controls[r[1]]
                if r[2] == 'append_text':
                    txt = ctl.get_text()
                    txt += r[3]
                    ctl.set_text(txt)
                elif r[2] == 'clear_text':
                    ctl.set_text('')
            if r[0] == 'HIDE_FORM':
                self.hide_forms[self.id] = self
                self.hide()
            if r[0] == 'CLOSE_FORM':
                self.close()
            if r[0] == 'NOTHING':
                pass

    @staticmethod
    def defrag_name(name_to_defrag):
        names = name_to_defrag.split('.')
        i = 0
        module = None
        model = None
        name = None
        for m in names:
            if i == 0:
                module = names[0]
            elif i == len(names) - 1:
                name = names[i]
            else:
                if model is None:
                    model = names[i]
                else:
                    model += '.' + names[i]
            i += 1
        return module, model, name
