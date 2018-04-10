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
        ok = context['model']['user'].credential
        if ok:
            context['next'] = ['OPEN_FORM', 'user.in_out']
        else:
            context['next'] = ['OPEN_FORM', 'user.credential']
        return context

    def button_btn_in_clicked(self, context):
        context['model']['user'].credential = False
        context['next'] = ['CLOSE_FORM']
        return context

    def button_btn_out_clicked(self, context):
        context['model']['user'].credential = False
        context['next'] = ['CLOSE_FORM']
        return context

