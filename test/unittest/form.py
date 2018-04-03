# This file is part of elygui project.
# The COPYRIGHT file at the top level of this repository
# contains the full copyright notices and license terms.

from xml2classobject import Xml2ClassObject
from elygui.elygui import Form
import unittest


class ElyGuiFormTest(unittest.TestCase):

    def test_ely_gui_form(self):

        string_xml = """
            <Forms>
              <Form id="main">
                <Title>Main Form</Title>
                <Childs>
                  <VBox id="main_box" model="main">
                    <Childs>
                      <HBox id="box_shutdown" model="main">
                        <Height>150</Height>
                        <Childs>
                          <Button id="btn_shutdown" model="main">
                            <Label>SHUTDOWN</Label>
                          </Button>
                        </Childs>
                      </HBox>
                    </Childs>
                  </VBox>
                </Childs>
              </Form>
            </Forms>"""

        forms = Xml2ClassObject(string_xml)

        form_def = forms.get_childs('Form')[0]
        frm = Form('dummy', form_def)

        self.assertEqual(frm.Title, 'Main Form')
