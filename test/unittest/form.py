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
              <!-- No id -->
              <Form model="no_id"></Form>

              <!-- No model -->
              <Form id="no_model"></Form>

              <Form id="main_form" model="test">
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
              <Form id="main_form" model="test">
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
              <Form id="main_form" model="test">
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
              <Form id="main_form" model="test">
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
              <Form id="main_form" model="test">
                <Extends>
                  <Extend>
                      <Path>/main_box/box_shutdown/main.btn_shutdown</Path>
                      <Action>remove</Action>
                  </Extend>
                </Extends>
              </Form>
              <Form id="main_form" model="test">
                <Extends>
                  <Extend>
                      <Path>/main_box/box_shutdown/clock3.btn_clock_3</Path>
                      <Action>replace</Action>
                      <Controls>
                        <Button id="btn_clock_3r" model="clock3r">
                          <Label>CLOCK 3 REPLACED</Label>
                        </Button>
                      </Controls>
                  </Extend>
                </Extends>
              </Form>
              <Form id="main_form" model="test">
                <Extends>
                  <Extend>
                      <Path>/main_box/box_shutdown/clock3r.btn_clock_3r</Path>
                      <Action>modify</Action>
                      <Controls>
                        <Button id="btn_clock_3r" model="clock3r">
                          <Label>CLOCK 3 REPLACED MODIFIED</Label>
                        </Button>
                      </Controls>
                  </Extend>
                </Extends>
              </Form>
            </Forms>"""

        forms = Xml2ClassObject(string_xml)

        # Missing id
        with self.assertRaises(ValueError):
            form_def = forms.get_childs('Form')[0]
            frm = Form(form_def)

        # Missing model
        with self.assertRaises(ValueError):
            form_def = forms.get_childs('Form')[1]
            frm = Form(form_def)

        form_def = forms.get_childs('Form')[2]
        frm = Form(form_def)

        self.assertEqual(frm.title, 'Main Form')
        self.assertEqual(frm.id, 'test.main_form')
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
        self.assertEqual(ctl.id, 'main.btn_shutdown')

        # Extends
        # place
        form_def = forms.get_childs('Form')[3]
        frm.extend(form_def.Extends.get_childs('Extend')[0])
        ctl = frm.childs['main_box'].childs['box_shutdown'].childs['clock.btn_clock']
        self.assertEqual(ctl.id, 'clock.btn_clock')
        self.assertEqual(ctl, frm.childs['main_box'].childs['box_shutdown'].controls[1])

        # place_before
        form_def = forms.get_childs('Form')[4]
        frm.extend(form_def.Extends.get_childs('Extend')[0])
        ctl = frm.childs['main_box'].childs['box_shutdown'].childs['clock2.btn_clock_2']
        self.assertEqual(ctl.id, 'clock2.btn_clock_2')
        self.assertEqual(ctl, frm.childs['main_box'].childs['box_shutdown'].controls[0])

        # place_after
        form_def = forms.get_childs('Form')[5]
        frm.extend(form_def.Extends.get_childs('Extend')[0])
        ctl = frm.childs['main_box'].childs['box_shutdown'].childs['clock3.btn_clock_3']
        self.assertEqual(ctl.id, 'clock3.btn_clock_3')
        self.assertEqual(ctl, frm.childs['main_box'].childs['box_shutdown'].controls[2])

        # remove
        form_def = forms.get_childs('Form')[6]
        frm.extend(form_def.Extends.get_childs('Extend')[0])
        parent = frm.childs['main_box'].childs['box_shutdown']
        self.assertEqual(len(parent.controls), 3)
        self.assertEqual('main.btn_shutdown' not in parent.childs, True)

        # replace
        form_def = forms.get_childs('Form')[7]
        frm.extend(form_def.Extends.get_childs('Extend')[0])
        parent = frm.childs['main_box'].childs['box_shutdown']
        self.assertEqual(len(parent.controls), 3)
        self.assertEqual('clock3.btn_clock_3' not in parent.childs, True)
        ctl = frm.childs['main_box'].childs['box_shutdown'].childs['clock3r.btn_clock_3r']
        self.assertEqual(ctl.id, 'clock3r.btn_clock_3r')        

        # modify
        form_def = forms.get_childs('Form')[8]
        frm.extend(form_def.Extends.get_childs('Extend')[0])
        ctl = frm.childs['main_box'].childs['box_shutdown'].childs['clock3r.btn_clock_3r']
        self.assertEqual(ctl.label, 'CLOCK 3 REPLACED MODIFIED')
