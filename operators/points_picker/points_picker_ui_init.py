# Copyright (C) 2018 Christopher Gearhart
# chris@bblanimation.com
# http://bblanimation.com/
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# System imports
# NONE!

# Blender imports
# NONE!

# Module imports
from ...subtrees.addon_common.common import ui


class PointsPicker_UI_Init():

    ###################################################
    # draw init

    def ui_setup(self):
        # UI Box functionality
        # NONE!

        # instructions
        self.instructions = {
            "add": "Press left-click to add or select a point",
            "grab": "Hold left-click on a point and drag to move it along the surface of the mesh",
            "remove": "Press 'ALT' and left-click to remove a point",
        }

        # Help Window
        self.info_panel = ui.framed_dialog(label="Points Picker Tools", id="info_panel")
        ui.span(innerText="test", parent=self.info_panel)

        # self.info_panel = self.wm.create_window('Points Picker Help', {'pos':9, 'movable':True})#, 'bgcolor':(0.30, 0.60, 0.30, 0.90)})
        # self.info_panel.add(ui.UI_Label('Instructions', align=0, margin=4))
        # self.inst_paragraphs = [self.info_panel.add(ui.UI_Markdown('', min_size=(200,10))) for i in range(3)]
        # #for i in self.inst_paragraphs: i.visible = False
        # self.set_ui_text()

        # Tools Window
        self.tools_panel = ui.framed_dialog(label="Points Picker Tools", id="tools_panel")
        ui.div(id="tools", parent=self.tools_panel)
        ui.button(label="Commit", parent=self.tools_panel, on_mouseclick=self.done)
        ui.button(label="Cancel", parent=self.tools_panel, on_mouseclick=self.done)

    def set_ui_text(self):
        """ sets the viewport text """
        self.reset_ui_text()
        for i,val in enumerate(['add', 'grab', 'remove']):
            self.inst_paragraphs[i].set_markdown(chr(65 + i) + ") " + self.instructions[val])

    def reset_ui_text(self):
        """ clears the viewport text """
        for inst_p in self.inst_paragraphs:
            inst_p.set_markdown('')

    ###################################################
