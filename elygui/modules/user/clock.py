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

    def button_btn_clock_clicked(self, frm, ctl, ctx):
        user = ctx['model']['user']
        if user.verified:
            ctx['next'] = [['OPEN_FORM', 'clock.in_out']]
        else:
            ctx['next'] = [['OPEN_FORM', 'user.credential']]
            ctx['required_by'] = ['clock.in_out']
        return ctx

    def button_btn_in_clicked(self, frm, ctl, ctx):
        user = ctx['model']['user']
        res = self._verify('in', user)

        self._close_with_reset(ctx)
        return ctx

    def button_btn_out_clicked(self, frm, ctl, ctx):
        user = ctx['model']['user']
        res = self._verify('out', user)

        self._close_with_reset(ctx)
        return ctx

    def _verify(self, type_, user):
        if type_ == 'in' and user.user_id == 0:
            return 1
        return 0

    def _close_with_reset(self, context):
        context['model']['user'].reset_fields()
        context['next'] = [['CLOSE_FORM']]
