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

    def button_btn_credential_ok_clicked(self, form, context):
        self.verified = self.get_credentials('1111')
        if not self.verified:
            self._clear_credentials(context)
        else:
            calling = context['required_by'][0]
            if not self.verify_access(calling):
                self._clear_credentials(context)
            else:
                self._clear_credentials(context)
                context['next'].append(['OPEN_FORM', calling])
        return context

    def button_btn_credential_close_clicked(self, form, context):
        self._clear_credentials(context)
        return context

    def button_btn_0_clicked(self, form, context):
        return self._pad_number_clicked(0, context)

    def button_btn_1_clicked(self, form, context):
        return self._pad_number_clicked(1, context)

    def button_btn_2_clicked(self, form, context):
        return self._pad_number_clicked(2, context)

    def button_btn_3_clicked(self, form, context):
        return self._pad_number_clicked(3, context)

    def button_btn_4_clicked(self, form, context):
        return self._pad_number_clicked(4, context)

    def button_btn_5_clicked(self, form, context):
        return self._pad_number_clicked(5, context)

    def button_btn_6_clicked(self, form, context):
        return self._pad_number_clicked(6, context)
        
    def button_btn_7_clicked(self, form, context):
        return self._pad_number_clicked(7, context)

    def button_btn_8_clicked(self, form, context):
        return self._pad_number_clicked(8, context)

    def button_btn_9_clicked(self, form, context):
        return self._pad_number_clicked(9, context)

    def _pad_number_clicked(self, number, context):
        context['next'] = [[
                'CONTROL', 
                'user.entry_credential', 
                'append_text',
                str(number)
            ]]
        return context

    def _clear_credentials(self, context):
        context['model']['user'].reset_fields()
        context['next'] = [
            [
                'CONTROL', 
                'user.entry_credential', 
                'clear_text',
            ],
            ['HIDE_FORM'],
        ]
