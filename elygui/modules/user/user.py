# This file is part of ElyGui project.
# The COPYRIGHT file at the top level of this repository
# contains the full copyright notices and license terms.

from elygui.model import Model

__all__ = ['User']


class User(Model):
    __model__ = 'user'

    def initialize(self, context):
        super(User, self).initialize(context)

        self.field('user_id')
        self.field('user_name')
        self.field('password')
        self.field('credentials', {})
        self.field('verified', False)
        self.field('paranoic', True)

        context['model']['user'] = self

    def verify_access(self, obj):
        if self.user_id is None or not self.verified:
            return False
        if obj not in self.credentials:
            if self.paranoic:
                return False
            else:
                return True
        return self.credentials[obj]

    def get_credentials(self, passwd):
        # This function must be totally overriden.
        # Following lines are for test purposes
        # and for expose an example.
        res = False
        print("PAssword: " + passwd)
        if passwd == '1111':
            self.user_id = 0
            self.user_name = 'Admin'
            self.credentials['clock.in_out'] = True
            res = True
        elif passwd == '9999':
            self.user_id = 1
            self.user_name = 'User'
            self.credentials['clock.in_out'] = False
            res = True
        return res

    def button_btn_credential_ok_clicked(self, ctx, frm, ctl):
        entry = frm.get_control('user.entry_credential')

        self.verified = self.get_credentials(entry.get_text())
        if not self.verified:
            self._clear_credentials(frm, ctx)
        else:
            calling = ctx['required_by'][0]
            if not self.verify_access(calling):
                self._clear_credentials(frm, ctx)
            else:
                self._clear_credentials(frm, ctx)
                ctx['next'].append(['OPEN_FORM', calling])
        return ctx

    def button_btn_credential_close_clicked(self, ctx, frm, ctl):
        self._clear_credentials(frm, ctx)
        return ctx

    def button_btn_clear_all_clicked(self, ctx, frm, ctl):
        entry = frm.get_control('user.entry_credential')
        entry.set_text('')

    def button_btn_clear_clicked(self, ctx, frm, ctl):
        entry = frm.get_control('user.entry_credential')
        txt = entry.get_text()
        entry.set_text(txt[:len(txt) - 1])

    def button_btn_0_clicked(self, ctx, frm, ctl):
        return self._pad_number_clicked(0, frm, ctl, ctx)

    def button_btn_1_clicked(self, ctx, frm, ctl):
        return self._pad_number_clicked(1, frm, ctl, ctx)

    def button_btn_2_clicked(self, ctx, frm, ctl):
        return self._pad_number_clicked(2, frm, ctl, ctx)

    def button_btn_3_clicked(self, ctx, frm, ctl):
        return self._pad_number_clicked(3, frm, ctl, ctx)

    def button_btn_4_clicked(self, ctx, frm, ctl):
        return self._pad_number_clicked(4, frm, ctl, ctx)

    def button_btn_5_clicked(self, ctx, frm, ctl):
        return self._pad_number_clicked(5, frm, ctl, ctx)

    def button_btn_6_clicked(self, ctx, frm, ctl):
        return self._pad_number_clicked(6, frm, ctl, ctx)
        
    def button_btn_7_clicked(self, ctx, frm, ctl):
        return self._pad_number_clicked(7, frm, ctl, ctx)

    def button_btn_8_clicked(self, ctx, frm, ctl):
        return self._pad_number_clicked(8, frm, ctl, ctx)

    def button_btn_9_clicked(self, ctx, frm, ctl):
        return self._pad_number_clicked(9, frm, ctl, ctx)

    def _pad_number_clicked(self, number, frm, ctl, ctx):
        entry = frm.get_control('user.entry_credential')
        txt = entry.get_text()
        txt += str(number)
        entry.set_text(txt)

    def _clear_credentials(self, frm, ctx):
        self.button_btn_clear_all_clicked(ctx, frm, None)
        ctx['model']['user'].reset_fields()
        ctx['next'] = [['HIDE_FORM']]
