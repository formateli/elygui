# This file is part of ElyGui project.
# The COPYRIGHT file at the top level of this repository
# contains the full copyright notices and license terms.

import os
import sys
from importlib import import_module
from xml2classobject import Xml2ClassObject
from .elygui_config import ElyGuiConfig
from .model import Model 

DIRECTORY = os.path.dirname(os.path.realpath(__file__))


class ElyGui(object):
    def __init__(self, xml_config):
        self.config = ElyGuiConfig(xml_config)
        if not self.config:
            raise Exception("ElyGui: No config loaded.")

        self._forms = {}
        self._model_classes = {}

        self.context = {}
        self.styles = {}
        self.styles_list = []

        module_path = os.path.join(DIRECTORY, 'modules')
        for m in self.config.Modules.get_childs('Module'):
            self._load_module(module_path, m)

        for model in Model._ext_list:
            if model is not None:
                cls = Model.get(model)
                if cls:
                    obj = cls(self.context)
                    if obj:
                        self._model_classes[model] = obj

    def get_model_class(self, model):
        if model in self._model_classes:
            return self._model_classes[model]

    def get_form(self, form_id):
        if form_id in self._forms:
            return self._forms[form_id]

    def _load_module(self, module_path, m):
        print("Loading module {0}".format(m.Name.value))
        xml = os.path.join(module_path, m.Name.value, 'elygui.xml')
        cfg = Xml2ClassObject(xml)
        if cfg.Module.Name.value != m.Name.value:
            raise Exception(
                "Module '{0}' did not match with '{1}'". format(
                    m.Name.value, cfg.Module.Name.value))

        loaded_module = import_module('elygui.modules.' + m.Name.value)

        if cfg.has_section(cfg, 'Styles') and \
                cfg.has_section(cfg.Styles, 'Style'):
            self._get_styles(cfg.Styles)

        if cfg.has_section(cfg, 'Forms') and \
                cfg.has_section(cfg.Forms, 'Form'):
            for f in cfg.Forms.get_childs('Form'):
                if not hasattr(f, 'id'):
                    raise ValueError("'id' attribute must be set for 'Form'")
                if not hasattr(f, 'model'):
                    raise ValueError("'model' attribute must be set for 'Form'")
                id_ = f.model + '.' + f.id
                if cfg.has_section(f, 'Extends'):
                    if id_ not in self._forms:
                        raise Exception(
                            "Form '{0}' can not be extended. Not found.".format(
                                id_))
                    form = self._forms[id_]
                    for ext in f.Extends.get_childs('Extend'):
                        form.extend(ext)
                else:
                    if id_ in self._forms:
                        raise Exception("Form '{0}' already exists.".format(
                            f.id))
                    form = Form(f)
                    self._forms[id_] = form

    def _get_styles(self, styles):
        for st in styles.get_childs('Style'):        
            if st.Name.value in self.styles:
                style = self.styles[st.Name.value]
                style.set_values(st)
            else:
                style = Style(st)
                self.styles[st.Name.value] = style
                self.styles_list.append(style)


class Container(object):
    _ids = {}

    def __init__(self, model_name, con_def):
        if not hasattr(con_def, 'id'):
            raise ValueError("id attribute must be set.")

        if model_name is not None:
            self.id = "{0}.{1}".format(model_name, con_def.id)
            if self.id in self._ids:
                raise Exception(
                    "Form or Control with id '{0}' is already present.".format(
                        self.id))
            self._ids[self.id] = self.id
        else:
            self.id = con_def.id
        self.parent = None
        self.controls = []
        self.childs = {}

    def add_childs(self, childs):
        if not childs:
            return
        for ch in childs:
            self._add_child(ch)

    def _add_child(self, child, place=-1):
        ctl_class = getattr(
            sys.modules[__name__],
            child._section_name)
        
        model_name = None
        if Xml2ClassObject.has_section(child, 'model'):
            model_name = child.model
        ctl = ctl_class(model_name, child)
        ctl.parent = self
        if place == -1:
            self.controls.append(ctl)
        else:
            self.controls.insert(place, ctl)
        self.childs[ctl.id] = ctl

        if Xml2ClassObject.has_section(child, 'Childs'):
            ctl.add_childs(child.Childs.get_childs())

    def _remove_child(self, index):
        child = self.controls[index]
        self.childs.pop(child.id)
        self.controls.remove(child)

    def modify(self, ctl_def):
        self.id = self._get_field_value(ctl_def, 'id', self.id)
        self.model_name = self._get_field_value(
            ctl_def, 'model', self.model_name)
        self.label = self._get_field_value(
            ctl_def, 'Label', self.label)

    @staticmethod
    def _get_field_value(ctl_def, name, default=None):
        try:
            if not hasattr(ctl_def, name):
                return default
            val = getattr(ctl_def, name)
            if hasattr(val, 'value'):
                return getattr(val, 'value')
            else:
                return val
        except:
            return default


class Form(Container):
    def __init__(self, form_def):
        if not hasattr(form_def, 'model'):
            raise ValueError("model must be set for Form '{0}'".format(
                form_def.id))
        super(Form, self).__init__(form_def.model, form_def)
        self.title = self._get_field_value(form_def, 'Title', 'NO TITLE')
        self.add_childs(form_def.Childs.get_childs())

    def extend(self, ext_def):
        action = ext_def.Action.value
        ctl = self._resolve_path(ext_def.Path.value)
        place_index = ctl.get_index()

        if action == 'remove':
            ctl.parent._remove_child(place_index)
        elif action == 'place':
            ctl._add_child(ext_def.Controls.get_childs()[0])
        elif action in ['place_after', 'place_before']:
            if action == 'place_after':
                place_index += 1
            ctl.parent._add_child(
                ext_def.Controls.get_childs()[0],
                place=place_index)
        elif action == 'replace':
            ctl.parent._add_child(
                ext_def.Controls.get_childs()[0],
                place=place_index + 1)
            ctl.parent._remove_child(place_index)
        elif action == 'modify':
            ctl.modify(ext_def.Controls.get_childs()[0])
        else:
            raise Exception(
                "'{0}' is not a valid Action.".format(action))

    def _resolve_path(self, path):
        els = path.split('/')
        ctl = self
        i = 1
        while i < len(els):
            ctl = self._get_els(els[i], path, ctl)
            i += 1
        return ctl

    def _get_els(self, el, path, parent):
        err = "Invalid '{0}' in path '{1}'.".format(el, path)
        if not hasattr(parent, 'childs'):
            raise Exception(
                err + " Parent has no attribute 'childs'.")
        if el not in parent.childs:
            raise Exception(
                err + " Not found in parent childs.")
        return parent.childs[el]


class Style(object):
    def __init__(self, style_def):
        self.set_values(style_def)

    def set_values(self, style_def):
        self._get_style(style_def, 'Name', 'name')
        self._get_style(style_def, 'Color', 'font_color')
        self._get_style(style_def, 'FontSize', 'font_size')

    def _get_style(self, style, name, att_name):
        val = None
        if Xml2ClassObject.has_section(style, name):
            val = getattr(style, name).value
        if val is not None:
            setattr(self, att_name, val)
        if not hasattr(self, att_name):
            setattr(self, att_name, None)


class Control(Container):
    def __init__(self, type_, model_name, control_def):
        super(Control, self).__init__(model_name, control_def)
        self.type_ = type_
        self.model_name = model_name
        self.style = self._get_field_value(control_def, 'Style') 
        self.height = self._get_field_value(control_def, 'Height') 
        self.width = self._get_field_value(control_def, 'Width') 

    def get_index(self):
        i = 0
        for ctl in self.parent.controls:
            if ctl.id == self.id:
                return i
            i += 1
    

class HBox(Control):
    def __init__(self, model, control_def):
        super(HBox, self).__init__('HBox', model, control_def)


class VBox(Control):
    def __init__(self, model, control_def):
        super(VBox, self).__init__('VBox', model, control_def)


class Button(Control):
    def __init__(self, model, control_def):
        super(Button, self).__init__('Button', model, control_def)
        self.label = self._get_field_value(control_def, 'Label')


class Entry(Control):
    def __init__(self, model, control_def):
        super(Entry, self).__init__('Entry', model, control_def)
        self.label = self._get_field_value(control_def, 'Label')
