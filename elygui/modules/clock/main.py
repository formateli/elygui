# This file is part of ElyGui project.
# The COPYRIGHT file at the top level of this repository
# contains the full copyright notices and license terms.

from elygui.model import Model

__all__ = ['Main']


class Main(Model):
    __model__ = 'main'

    def initialize(self, context):
        super(Main, self).initialize(context)
        print("Initializing 'Main'")

    def button_btn_shutdown_clicked(self, context):
        return "SHUTDOWN"

