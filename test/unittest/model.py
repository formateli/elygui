# This file is part of elygui project.
# The COPYRIGHT file at the top level of this repository
# contains the full copyright notices and license terms.

from elygui.model import Model
import unittest


class A(Model):
    __model__ = 'test.a'

    def value(self):
        return "Class A"

    def valueA(self):
        return "Value A"


class A1(Model):
    __model__ = 'test.a'

    def value(self):
        v = super(A1, self).value()
        return v + " + Class A1"


class A2(Model):
    __model__ = 'test.a'

    def value(self):
        v = super(A2, self).value()
        return v + " + Class A2"


class ElyGuiModelTest(unittest.TestCase):

    def test_ely_gui_model(self):
        a = Model.get('test.a')(context=None)

        self.assertEqual(a.valueA(), 'Value A')
        self.assertEqual(a.value(), 'Class A + Class A1 + Class A2')
