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
              <Form id="main_form">
                <Title>Main Form</Title>
                <Childs>
                  <VBox id="main_box">
                    <Childs>
                      <HBox id="box_shutdown">
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
              <Form id="main.main_form">
                <Extends>
                  <Extend>
                      <Path>/main_box/box_shutdown</Path>
                      <Action>place</Action>
                      <Controls>
                        <Button id="btn_clock" model="clock">
                          <Label>CLOCK</Label>
                        </Button>
                      </Controls>
                  </Extend>
                </Extends>
              </Form>
              <Form id="main.main_form">
                <Extends>
                  <Extend>
                      <Path>/main_box/box_shutdown/main.btn_shutdown</Path>
                      <Action>place_before</Action>
                      <Controls>
                        <Button id="btn_clock_2" model="clock2">
                          <Label>CLOCK 2</Label>
                        </Button>
                      </Controls>
                  </Extend>
                </Extends>
              </Form>
              <Form id="main.main_form">
                <Extends>
                  <Extend>
                      <Path>/main_box/box_shutdown/main.btn_shutdown</Path>
                      <Action>place_after</Action>
                      <Controls>
                        <Button id="btn_clock_3" model="clock3">
                          <Label>CLOCK 3</Label>
                        </Button>
                      </Controls>
                  </Extend>
                </Extends>
              </Form>
              <Form id="main.main_form">
                <Extends>
                  <Extend>
                      <Path>/main_box/box_shutdown/main.btn_shutdown</Path>
                      <Action>remove</Action>
                  </Extend>
                </Extends>
              </Form>
            </Forms>"""

        forms = Xml2ClassObject(string_xml)

        form_def = forms.get_childs('Form')[0]
        frm = Form('dummy', form_def)

        self.assertEqual(frm.title, 'Main Form')
        self.assertEqual(frm.id, 'dummy.main_form')
        self.assertEqual(frm.controls[0].id, 'main_box')
        self.assertEqual(frm.childs['main_box'].id, 'main_box')
        self.assertEqual(frm.controls[0].controls[0].id, 'box_shutdown')
        self.assertEqual(
            frm.childs['main_box'].childs['box_shutdown'].id, 'box_shutdown')
        self.assertEqual(
            frm.controls[0].controls[0].controls[0].id, 'main.btn_shutdown')
        self.assertEqual(
            frm.childs['main_box'].childs['box_shutdown'].childs['main.btn_shutdown'].id,
                'main.btn_shutdown')

        ctl = frm.childs['main_box'].childs['box_shutdown'].childs['main.btn_shutdown']
        self.assertEqual(ctl.get_full_name(), 'dummy.main.btn_shutdown')

        # Extends
        # place
        form_def = forms.get_childs('Form')[1]
        frm.extend(form_def.Extends.get_childs('Extend')[0])
        ctl = frm.childs['main_box'].childs['box_shutdown'].childs['clock.btn_clock']
        self.assertEqual(ctl.get_full_name(), 'dummy.clock.btn_clock')
        self.assertEqual(ctl, frm.childs['main_box'].childs['box_shutdown'].controls[1])

        # place_before
        form_def = forms.get_childs('Form')[2]
        frm.extend(form_def.Extends.get_childs('Extend')[0])
        ctl = frm.childs['main_box'].childs['box_shutdown'].childs['clock2.btn_clock_2']
        self.assertEqual(ctl.get_full_name(), 'dummy.clock2.btn_clock_2')
        self.assertEqual(ctl, frm.childs['main_box'].childs['box_shutdown'].controls[0])

        # place_after
        form_def = forms.get_childs('Form')[3]
        frm.extend(form_def.Extends.get_childs('Extend')[0])
        ctl = frm.childs['main_box'].childs['box_shutdown'].childs['clock3.btn_clock_3']
        self.assertEqual(ctl.get_full_name(), 'dummy.clock3.btn_clock_3')
        self.assertEqual(ctl, frm.childs['main_box'].childs['box_shutdown'].controls[2])

        # remove
        form_def = forms.get_childs('Form')[4]
        frm.extend(form_def.Extends.get_childs('Extend')[0])
        parent = frm.childs['main_box'].childs['box_shutdown']
        self.assertEqual(len(parent.controls), 3)
        self.assertEqual('main.btn_shutdown' not in parent.childs, True)

        # TODO modify
