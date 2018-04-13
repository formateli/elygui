# This file is part of ElyGui project.
# The COPYRIGHT file at the top level of this repository
# contains the full copyright notices and license terms.

from elygui.model import Model

__all__ = ['Clock']


class Clock(Model):
    __model__ = 'clock'

    def initialize(self, context):
        super(Clock, self).initialize(context)
        context['model']['clock'] = self

    def button_btn_clock_clicked(self, context):
        ok = context['model']['user'].verified
        if ok:
            context['next'] = [['OPEN_FORM', 'user.in_out']]
        else:
            context['next'] = [['OPEN_FORM', 'user.credential']]
            context['required_by'] = ['user.in_out']
        return context

    def button_btn_in_clicked(self, context):
        context['model']['user'].verified = False
        context['next'] = [['CLOSE_FORM']]
        return context

    def button_btn_out_clicked(self, context):
        print("OUT")
        context['model']['user'].credential = False
        context['model']['user'].credential_X = False
        print(context['model']['user'].credential_X)
        print(context['model']['user'].credential)
        context['next'] = [['CLOSE_FORM']]
        return context

