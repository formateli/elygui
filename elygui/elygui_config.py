# This file is part of ElyGui project.
# The COPYRIGHT file at the top level of this repository
# contains the full copyright notices and license terms.

from xml2classobject import Xml2ClassObject


class ElyGuiConfig(Xml2ClassObject):
    def __init__(self, xml_config):
        super(ElyGuiConfig, self).__init__(xml_config)

    @staticmethod
    def get_section(section, name):
        if hasattr(section, name):
            return getattr(section, name)

    @staticmethod
    def get_value(section, name, default=None):
        if not section:
            return default
        if hasattr(section, name):
            return getattr(section, name).value
        return default

    @staticmethod
    def convert_to_bool(value):
        if value is None:
            return False
        if isinstance(value, bool):
            return value
        if str(value).lower() in \
                ('yes', 'y', 'true',  't', '1', '-1'):
            return True
        if str(value).lower() in \
                ('no',  'n', 'false', 'f',
                '0', '0.0', '', 'none', '[]', '{}'):
            return False
        return False
