# This file is part of ElyGui project.
# The COPYRIGHT file at the top level of this repository
# contains the full copyright notices and license terms.

from elygui.model import Model, String, One2Many


class User(Model):
    __model__ = 'user.user'

    name = String()
    groups = One2Many('user.group')


class Group(Model):
    __model__ = 'user.group'

    name = String()
