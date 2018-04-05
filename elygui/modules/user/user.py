# This file is part of ElyGui project.
# The COPYRIGHT file at the top level of this repository
# contains the full copyright notices and license terms.

from elygui.model import Model

__all__ = ['User']


class User(Model):
    __model__ = 'user'

    def initialize(self, context):
        super(User, self).initialize(context)
        context['model'] = {'user': {'credential': False}}

    def button_btn_credential_close_clicked(self, context):
        context['model']['user']['credential'] = False
        context['next'] = ['CLOSE_FORM']
        return context

    def button_btn_credential_ok_clicked(self, context):
        context['model']['user']['credential'] = True
        context['next'] = ['CLOSE_FORM']
        return context
