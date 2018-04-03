# This file is part of ElyGui project.
# The COPYRIGHT file at the top level of this repository
# contains the full copyright notices and license terms.

from six import add_metaclass


class _Model(type):
    _ext = {}

    def __new__(meta, name, bases, class_dict):
        print ("Registering model class: {0}".format(name))
        #print("\n\n==================")
        #print ("Meta: {0}".format(meta))
        #print ("Name: {0}".format(name))
        #print ("Bases: {0}".format(bases))
        #print ("ClassDict: {0}".format(class_dict))

        if not "__model__" in class_dict:
            raise Exception(
                "'__model__' attribute must be set for Model derived classes. Class '{0}'".format(
                name))
        if class_dict['__model__'] in _Model._ext:
            bases = (_Model._ext[class_dict['__model__']],) + bases

        #print ("New Bases: {0}".format(bases))
        #print("==================\n")
    
        new_cls = type.__new__(meta, name, bases, class_dict)
        setattr(new_cls, '__model__', class_dict['__model__'])

        _Model._ext[class_dict['__model__']] = new_cls

        return new_cls


    @classmethod
    def get(cls, model_name):
        #print (" Getting " + model_name)
        if not model_name in cls._ext:
            cls._ext[model_name] = Model
            return cls._ext[model_name]
        return cls._ext[model_name]


@add_metaclass(_Model)
class Model(object):
    __model__ = None

    def __init__(self, context):
        self.initialize(context)

    def initialize(self, context):
        pass
