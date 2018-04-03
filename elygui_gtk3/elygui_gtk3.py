# This file is part of ElyGui project.
# The COPYRIGHT file at the top level of this repository
# contains the full copyright notices and license terms.

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class ElyGuiGtk3(object):
    def __init__(self, gui_def):
        win = MainWindow(gui_def)
        Gtk.main()


class MainWindow(Gtk.Window):
    def __init__(self, gui_def):
        self.gui_def = gui_def
        frm = gui_def.get_form('main', 'main_form')

        #TODO if not frm raise error

        Gtk.Window.__init__(self, title=frm.title)

        for ctl in frm.controls:
            wg = self.get_widget(ctl)
            self.add(wg)

        self.connect("delete-event", Gtk.main_quit)
        self.show_all()

    def on_button1_clicked(self, widget):
        print("Hello")

    def on_button2_clicked(self, widget):
        print("Goodbye")

    def on_button3_clicked(self, widget):
        Gtk.main_quit()

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

        if wg:
            wg.set_property('name',
                wg_def.get_full_name())

        return wg

    def on_button_clicked(self, widget):
        module, model, name = self.defrag_name(
            widget.get_property('name'))

        cls = self.gui_def.get_model_class(model)
        func = getattr(cls, 'button_' + name + '_clicked')
        res = func(self.gui_def._context)

        if res == 'SHUTDOWN':
            Gtk.main_quit()

    def defrag_name(self, name_to_defrag):
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
