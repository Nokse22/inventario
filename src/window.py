# window.py
#
# Copyright 2023 Nokse
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
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Adw
from gi.repository import Gtk, Gio

#@Gtk.Template(resource_path='/io/github/nokse22/inventario/window.ui')
class InventarioWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'InventarioWindow'

    sidebar_options = ["Dashboard", "Items"]

    components = [
    ["resistor", "ABC12", 34],
    ["capacitor", "DEF34", 67],
    ["inductor", "GHI56", 12],
    ["diode", "JKL78", 45],
    ["transistor", "MNO90", 23],
    ["IC", "PQR12", 78],
    ["LED", "STU34", 56],
    ["crystal oscillator", "VWX56", 90],
    ["relay", "YZA78", 32],
    ["potentiometer", "BCD90", 18],
    ["transformer", "EFG12", 65],
    ["fuse", "HIJ34", 43],
    ["switch", "KLM56", 76],
    ["sensor", "NOP78", 21],
    ["connector", "QRS90", 54],
    ["battery", "TUV12", 37],
    ["microcontroller", "WXY34", 29],
    ["LCD display", "ZAB56", 83],
    ["motor", "CDE78", 50],
    ["speaker", "FGH90", 62]
    ]


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.set_default_size(1000, 700)

        self.split_view = Adw.NavigationSplitView()
        self.set_content(self.split_view)

        # Sidebar
        sidebar_page = Adw.NavigationPage()
        sidebar_page.set_title("Navigation")
        sidebar_page.set_tag("sidebar")

        sidebar_box = Gtk.Box(orientation=1)
        sidebar_page.set_child(sidebar_box)

        sidebar_headerbar = Adw.HeaderBar(css_classes=["flat"])
        sidebar_box.append(sidebar_headerbar)

        # Content
        content_page = Adw.NavigationPage()
        content_page.set_title("Inventario")
        content_page.set_tag("content")

        content_box = Gtk.Box(orientation=1)
        content_page.set_child(content_box)

        content_headerbar = Adw.HeaderBar(css_classes=["flat"])
        content_box.append(content_headerbar)

        toggle_sidebar_button = Gtk.Button(icon_name="go-previous-symbolic")
        toggle_sidebar_button.connect("clicked", self.toggle_sidebar)
        content_headerbar.pack_start(toggle_sidebar_button)


        menu_button = Gtk.MenuButton()
        menu_button.set_icon_name("open-menu-symbolic")
        menu = Gio.Menu()
        menu.append(_("Preferences"), "app.preferences")
        menu.append(_("Keyboard shorcuts"), "app.show-help-overlay")
        menu.append(_("About"), "app.about")
        menu_button.set_menu_model(menu)

        content_headerbar.pack_end(menu_button)

        self.content_srolled_window = Gtk.ScrolledWindow(vexpand=True, overlay_scrolling=False)
        self.content_srolled_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        content_box.append(self.content_srolled_window)

        self.split_view.set_sidebar(sidebar_page)
        self.split_view.set_content(content_page)

        #Navigation
        sidebar_srolled_window = Gtk.ScrolledWindow(vexpand=True)
        self.sidebar_navigation_listBox = Gtk.ListBox(css_classes=["navigation-sidebar"])
        self.sidebar_navigation_listBox.connect("row-activated", self.on_navigation_row_activated)
        sidebar_box.append(sidebar_srolled_window)
        sidebar_srolled_window.set_child(self.sidebar_navigation_listBox)

        #split_view.set_collapsed(True)

        for i in range(len(self.sidebar_options)):
            self.sidebar_navigation_listBox.append(Gtk.Label(label = self.sidebar_options[i], xalign=0))

        self.show_dashboard()


    def show_items(self):
        self.content_srolled_window_list_box = Gtk.ListBox(show_separators=True, selection_mode=0)
        self.content_srolled_window.set_child(self.content_srolled_window_list_box)
        for i in range(20):
            self.add_item(self.components[i][1])


    def add_item(self, ID):
        component_id = 0
        for i in range(len(self.components)):
            if self.components[i][1] == ID:
                component_id = i
                break
        box = Gtk.Box(css_classes=[], margin_start=10, hexpand=True)

        box.append(Gtk.Label(label=self.components[component_id][0], width_request = 200, ellipsize=3,
                halign=Gtk.Align.START, xalign=0, margin_start=12, hexpand=True))

        box.append(Gtk.Label(label=self.components[component_id][2], hexpand=True))

        edit_button = Gtk.Button(icon_name="document-edit-symbolic",
                margin_start=6, margin_end=2, margin_top=2, margin_bottom=2, name=self.components[component_id][1])

        box.append(edit_button)
        self.content_srolled_window_list_box.append(box)
        edit_button.connect("clicked", self.edit_item)

    def edit_item(self, btn):
        print(btn.get_name())

    def toggle_sidebar(self, btn):
        self.split_view.set_collapsed(self.split_view.get_collapsed)

    def on_navigation_row_activated(self, list_box, exc):
        selected_row = list_box.get_selected_row()
        self.split_view.set_collapsed(False)
        if selected_row.get_child().get_label() == "Dashboard":
            self.show_dashboard()
        elif selected_row.get_child().get_label() == "Items":
            self.show_items()

    def show_dashboard(self):
        self.dashboard_box = Gtk.Grid(row_homogeneous=True, column_homogeneous=True,
                row_spacing=10, column_spacing=10, margin_start=10, margin_top=10, margin_bottom=10, margin_end=10)
        self.content_srolled_window.set_child(self.dashboard_box)

        for i in range(4):
            for j in range(10):
                self.dashboard_box.attach(Gtk.Label(label=str(i) + str(j)), i, j, 1, 1)

        self.dashboard_box.attach(self.dashboard_simple_widget("Items", len(self.components)), 0,0,1,1)
        self.dashboard_box.attach(self.dashboard_simple_widget("Sold", len(self.components)), 0,1,1,1)
        self.dashboard_box.attach(self.dashboard_simple_widget("Items to sell", len(self.components)), 0,2,1,1)

    def dashboard_simple_widget(self, info_name, info):
        box = Gtk.Box(css_classes=["card"], margin_start=6, margin_end=6,
                margin_top=6, margin_bottom=6, hexpand=True, spacing = 6)
        box.append(Gtk.Label(label=info_name, hexpand=True, xalign=0, margin_start=10, margin_top=10, margin_bottom=10))
        box.append(Gtk.Label(label=info, hexpand=True, xalign=1, margin_end=10))
        return box
        
