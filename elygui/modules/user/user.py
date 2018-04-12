# This file is part of ElyGui project.
# The COPYRIGHT file at the top level of this repository
# contains the full copyright notices and license terms.

from elygui.model import Model

__all__ = ['User']


class User(Model):
    __model__ = 'user'

    def initialize(self, context):
        super(User, self).initialize(context)

        self.credential = False

        context['model']['user'] = self

    def button_btn_credential_ok_clicked(self, context):
        self.credential = True
        calling = context['required_by'][0]
        context['next'] = [
                self._clear_entry_credential(),
                ['HIDE_FORM'],
                ['OPEN_FORM', calling],
            ]
        return context

    def button_btn_credential_close_clicked(self, context):
        self.credential = False
        context['next'] = [
                self._clear_entry_credential(),
                ['HIDE_FORM']
            ]
        return context

    def button_btn_0_clicked(self, context):
        return self._pad_number_clicked(0, context)

    def button_btn_1_clicked(self, context):
        return self._pad_number_clicked(1, context)

    def button_btn_2_clicked(self, context):
        return self._pad_number_clicked(2, context)

    def button_btn_3_clicked(self, context):
        return self._pad_number_clicked(3, context)

    def button_btn_4_clicked(self, context):
        return self._pad_number_clicked(4, context)

    def button_btn_5_clicked(self, context):
        return self._pad_number_clicked(5, context)

    def button_btn_6_clicked(self, context):
        return self._pad_number_clicked(6, context)
        
    def button_btn_7_clicked(self, context):
        return self._pad_number_clicked(7, context)

    def button_btn_8_clicked(self, context):
        return self._pad_number_clicked(8, context)

    def button_btn_9_clicked(self, context):
        return self._pad_number_clicked(9, context)

    def _pad_number_clicked(self, number, context):
        context['next'] = [[
                'CONTROL', 
                'user.entry_credential', 
                'append_text',
                str(number)
            ]]
        return context

    def _clear_entry_credential(self):
        return [
            'CONTROL', 
            'user.entry_credential', 
            'clear_text',
        ]
