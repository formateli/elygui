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
        self._context = {}
        self._model_classes = {}

        module_path = os.path.join(DIRECTORY, 'modules')
        for m in self.config.Modules.get_childs('Module'):
            self._load_module(module_path, m)

        for model, _ in Model._ext.items():
            if model is not None:
                cls = Model.get(model)
                if cls:
                    obj = cls(self._context)
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

        if cfg.has_section(cfg, 'Forms') and \
                cfg.has_section(cfg.Forms, 'Form'):
            for f in cfg.Forms.get_childs('Form'):
                if cfg.has_section(f, 'Extends'):
                    if f.id not in self._forms:
                        raise Exception(
                            "Form '{0}' can not be extended. Not found.".format(
                                f.id))
                    form = self._forms[f.id]
                    for ext in f.Extends.get_childs('Extend'):
                        form.extend(ext)
                else:
                    form_name = m.Name.value + '.' + f.id
                    if form_name in self._forms:
                        raise Exception("Form '{0}' already exists.".format(
                            form_name))
                    form = Form(m.Name.value, f)
                    self._forms[m.Name.value + '.' + f.id] = form


class Container(object):
    def __init__(self, module_name, con_def):
        self.module_name = module_name
        self.id = con_def.id
        self.parent = None
        self.controls = []
        self.childs = {}

    def add_childs(self, module_name, childs):
        if not childs:
            return
        for ch in childs:
            self._add_child(module_name, ch)

    def _add_child(self, module_name, child, place=-1):
        ctl_class = getattr(
            sys.modules[__name__],
            child._section_name)
        
        model_name = None
        if Xml2ClassObject.has_section(child, 'model'):
            model_name = child.model
        ctl = ctl_class(module_name, model_name, child)
        ctl.parent = self
        if place == -1:
            self.controls.append(ctl)
        else:
            self.controls.insert(place, ctl)
        self.childs[ctl.id] = ctl

        if Xml2ClassObject.has_section(child, 'Childs'):
            ctl.add_childs(
                module_name, child.Childs.get_childs())

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
    def __init__(self, module_name, form_def):
        super(Form, self).__init__(module_name, form_def)
        self.id = module_name + '.' + self.id
        self.title = self._get_field_value(form_def, 'Title', 'NO TITLE')
        self.add_childs(
            module_name, form_def.Childs.get_childs())

    def extend(self, ext_def):
        action = ext_def.Action.value
        ctl = self._resolve_path(ext_def.Path.value)
        place_index = ctl.get_index()

        if action == 'remove':
            ctl.parent._remove_child(place_index)
        elif action == 'place':
            ctl._add_child(
                self.module_name, ext_def.Controls.get_childs()[0])
        elif action in ['place_after', 'place_before']:
            if action == 'place_after':
                place_index += 1
            ctl.parent._add_child(
                self.module_name, ext_def.Controls.get_childs()[0],
                place=place_index)
        elif action == 'replace':
            ctl.parent._add_child(
                self.module_name, ext_def.Controls.get_childs()[0],
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


class Control(Container):
    def __init__(self, type_, module_name, model_name, control_def):
        super(Control, self).__init__(module_name, control_def)
        if model_name is not None:
            self.id = model_name + '.' + self.id
        self.type_ = type_
        self.model_name = model_name
        self.height = self._get_field_value(control_def, 'Height') 
        self.width = self._get_field_value(control_def, 'Width') 

    def get_full_name(self):
        return self.module_name + '.' + self.id

    def get_index(self):
        i = 0
        for ctl in self.parent.controls:
            if ctl.id == self.id:
                return i
            i += 1


class HBox(Control):
    def __init__(self, module_name, model, control_def):
        super(HBox, self).__init__('HBox', module_name, model, control_def)


class VBox(Control):
    def __init__(self, module_name, model, control_def):
        super(VBox, self).__init__('VBox', module_name, model, control_def)


class Button(Control):
    def __init__(self, module_name, model, control_def):
        super(Button, self).__init__('Button', module_name, model, control_def)
        self.label = self._get_field_value(control_def, 'Label')


class Entry(Control):
    def __init__(self, module_name, model, control_def):
        super(Entry, self).__init__('Entry', module_name, model, control_def)
        self.label = self._get_field_value(control_def, 'Label')
