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

    def button_btn_clock_clicked(self, form, context):
        user = context['model']['user']
        if user.verified:
            context['next'] = [['OPEN_FORM', 'clock.in_out']]
        else:
            context['next'] = [['OPEN_FORM', 'user.credential']]
            context['required_by'] = ['clock.in_out']
        return context

    def button_btn_in_clicked(self, form, context):
        user = context['model']['user']
        res = self._verify('in', user)

        self._close_with_reset(context)
        return context

    def button_btn_out_clicked(self, form, context):
        user = context['model']['user']
        res = self._verify('out', user)

        self._close_with_reset(context)
        return context

    def _verify(self, type_, user):
        if type_ == 'in' and user.user_id == 0:
            return 1
        return 0

    def _close_with_reset(self, context):
        context['model']['user'].reset_fields()
        context['next'] = [['CLOSE_FORM']]
