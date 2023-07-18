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

from gi.repository import GObject
from gi.repository import Adw
from gi.repository import Gtk, Gio, GLib
import random

class Item(GObject.Object):
    __gtype_name__ = "Item"

    def __init__(self, item_id, item_name, item_quantity, item_package, item_cost):
        super().__init__()

        self._details = []
        self.details_names = [["Name","item_name"], ["Quantity", "item_quantity"],
                    ["Package", "item_package"], ["Cost", "item_cost"]]

        self._details.append(item_id)
        self._details.append(item_name)
        self._details.append(item_quantity)
        self._details.append(item_package)
        self._details.append(item_cost)

    @GObject.Property(type=str)
    def item_id(self):
        return self._details[0]

    @GObject.Property(type=str)
    def item_name(self):
        return self._details[1]

    @GObject.Property(type=int)
    def item_quantity(self):
        return self._details[2]

    @GObject.Property(type=str)
    def item_package(self):
        return self._details[3]

    @GObject.Property(type=float)
    def item_cost(self):
        return self._details[4]

    @GObject.Property(type=int)
    def details_n(self):
        return len(self._details)

    @GObject.Property(type=int)
    def details_all(self):
        return self._details

    def __repr__(self):
        text = "Item: "
        for i in range(len(self._details) - 1):
            text = text + str(self.details_names[i][0]) + ": " +  str(self._details[i + 1]) + ", "
        return text

class InventarioWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'InventarioWindow'

    sidebar_options = ["Dashboard", "Items"]

    column_details = [["Name", "str"], ["ID", "STR"], ["Quantity", "int"],
            ["Package", "str"], ["Cost", "cost"], ["Manufacturer", "str"]]

    details_names = [["Name","item_name"], ["Quantity", "item_quantity"],
                    ["Package", "item_package"], ["Cost", "item_cost"]]

    id_lenght = 5

    dashboard_width = 3
    dashboard_height = 10

    dashboard_widgets=["Simple value", "Progress bar"]

    nodes = {
            "ABC12": ("resistor", 34, "To220", 0.01),
            "DEF34": ("capacitor", 67, "SMD0805", 0.05),
            "GHI56": ("inductor", 12, "Axial", 0.2),
            "JKL78": ("diode", 45, "SOD-123", 0.08),
            "MNO90": ("transistor", 23, "SOT-23", 0.12),
            "PQR12": ("IC", 78, "DIP-16", 0.4),
            "STU34": ("LED", 56, "PLCC-4", 0.1),
            "VWX56": ("crystal oscillator", 90, "SMD3225", 0.3),
            "YZA78": ("relay", 32, "DIP-8", 0.15),
            "BCD90": ("potentiometer", 18, "Through Hole", 0.25),
            "EFG12": ("transformer", 65, "EFD20", 0.6),
            "HIJ34": ("fuse", 43, "SMD1206", 0.07),
            "KLM56": ("switch", 76, "Toggle", 0.18),
            "NOP78": ("sensor", 21, "SMD0805", 0.3),
            "QRS90": ("connector", 54, "USB Type-C", 0.5),
            "TUV12": ("battery", 37, "18650", 2.5),
            "WXY34": ("microcontroller", 29, "QFP-32", 1.2),
            "ZAB56": ("LCD display", 83, "TFT", 5.0),
            "CDE78": ("motor", 50, "DC Brushed", 3.8),
            "FGH90": ("speaker", 62, "8 Ohm", 2.2)
        }

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

        toggle_sidebar_button = Gtk.Button(icon_name="go-previous-symbolic", visible=False)
        toggle_sidebar_button.connect("clicked", self.toggle_sidebar)
        content_headerbar.pack_start(toggle_sidebar_button)


        menu_button = Gtk.MenuButton()
        menu_button.set_icon_name("open-menu-symbolic")
        menu = Gio.Menu()
        menu.append(_("Preferences"), "app.preferences")
        menu.append(_("Keyboard shorcuts"), "app.show-help-overlay")
        menu.append(_("About"), "app.about")
        menu_button.set_menu_model(menu)

        add_button = Gtk.Button()
        add_button.set_icon_name("list-add-symbolic")
        add_button.connect("clicked", self.add_item)
        # add_menu = Gio.Menu()
        # add_menu.append(_("Item"), None)
        # add_menu.append(_("Description"), None)
        # add_button.set_menu_model(add_menu)

        content_headerbar.pack_end(menu_button)
        content_headerbar.pack_end(add_button)

        self.content_srolled_window = Gtk.ScrolledWindow(vexpand=True, overlay_scrolling=False)
        self.content_srolled_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        #content_box.append(self.content_srolled_window)

        #Navigation
        sidebar_srolled_window = Gtk.ScrolledWindow(vexpand=True)
        self.sidebar_navigation_listBox = Gtk.ListBox(css_classes=["navigation-sidebar"])
        self.sidebar_navigation_listBox.connect("row-activated", self.on_navigation_row_activated)
        sidebar_box.append(sidebar_srolled_window)
        sidebar_srolled_window.set_child(self.sidebar_navigation_listBox)

        self.sidebar_srolled_window_item_info = Gtk.ScrolledWindow(vexpand=True)
        self.revealer = Gtk.Revealer(transition_type=1)

        self.revealer.set_child(self.sidebar_srolled_window_item_info)
        sidebar_box.append(self.revealer)

        #split_view.set_collapsed(True)

        for i in range(len(self.sidebar_options)):
            self.sidebar_navigation_listBox.append(Gtk.Label(label = self.sidebar_options[i], xalign=0))

        self.show_dashboard()

        self.model = Gio.ListStore(item_type=Item)
        for n in self.nodes.keys():
            self.model.append(Item(item_id=n, item_name=self.nodes[n][0], item_quantity=self.nodes[n][1],
                    item_package=self.nodes[n][2], item_cost=self.nodes[n][3]))

        self.cv = Gtk.ColumnView()
        tree_model = Gtk.TreeListModel.new(self.model, False, True, self.model_func)
        tree_sorter = Gtk.TreeListRowSorter.new(self.cv.get_sorter())
        sorter_model = Gtk.SortListModel(model=tree_model, sorter=tree_sorter)
        selection = Gtk.SingleSelection.new(model=sorter_model)
        self.cv.set_model(selection)

        for i in range(len(self.details_names)):
            self.add_column(self.details_names[i][0], self.details_names[i][1])

        scroll = Gtk.ScrolledWindow(vexpand=True)
        scroll.set_child(self.cv)

        self.set_default_size(1000, 700)

        self.split_view.set_sidebar(sidebar_page)
        self.split_view.set_content(content_page)
        content_box.append(scroll)

    def model_func(self, args):
        #print(args)
        pass

    def add_column(self, column_name, detail):
        factory = Gtk.SignalListItemFactory()
        factory.connect("setup", self._on_factory_setup)
        factory.connect("bind", self._on_factory_bind, detail)
        factory.connect("unbind", self._on_factory_unbind, detail)
        factory.connect("teardown", self._on_factory_teardown)

        col1 = Gtk.ColumnViewColumn(title=column_name, factory=factory)
        col1.props.expand = True
        self.cv.append_column(col1)


    def _on_factory_setup(self, factory, list_item):
        cell = Gtk.Inscription()
        cell._binding = None
        list_item.set_child(cell)

    def _on_factory_bind(self, factory, list_item, what):
        cell = list_item.get_child()
        item = list_item.get_item().get_item()
        cell._binding = item.bind_property(what, cell, "text", GObject.BindingFlags.SYNC_CREATE)

    def _on_factory_unbind(self, factory, list_item, what):
        cell = list_item.get_child()
        if cell._binding:
            cell._binding.unbind()
            cell._binding = None

    def _on_factory_teardown(self, factory, list_item):
        cell = list_item.get_child()
        cell._binding = None

    def _on_selected_item_notify(self, dropdown, _):
        item = dropdown.get_selected_item()
        print(f"Selected item: {item}")

    def show_items(self):
        self.content_srolled_window_list_box = Gtk.ListBox(show_separators=True)
        self.content_srolled_window_list_box.connect("row-activated", self.on_item_row_activated)
        self.content_srolled_window.set_child(self.content_srolled_window_list_box)
        for i in range(len(self.components)):
            self.add_item_row(self.components[i][1])

    def on_item_row_activated(self, list_box, exc):
        item_row_name = list_box.get_selected_row().get_child().get_name()
        index = self.get_index_from_id(item_row_name)
        self.sidebar_item_info_list_box = Gtk.ListBox(show_separators=False, selection_mode=0,
                margin_start=6, margin_end=6, margin_top=6, margin_bottom=6, css_classes=["card"])
        #self.sidebar_item_info_list_box.append(Gtk.Image(icon_name="document-edit-symbolic", icon_size=10))
        self.sidebar_srolled_window_item_info.set_child(self.sidebar_item_info_list_box)
        self.revealer.set_reveal_child(True)
        for i in range(len(self.column_details)):
            box = Gtk.Box(margin_start=6, margin_end=6)
            box.append(Gtk.Label(label=self.column_details[i][0], xalign=0, hexpand=True))
            try:
                self.components[index][i]
            except IndexError:
                text = "..."
            else:
                text = self.components[index][i]
            box.append(Gtk.Label(label=text, xalign=1, hexpand=True))
            self.sidebar_item_info_list_box.append(box)

    def get_index_from_id(self, ID):
        for i in range(len(self.components)):
            if self.components[i][1] == ID:
                return i
    def quit_window(self, btn, window):
        window.destroy()

    def add_item(self, args):
        add_item_window = Adw.Window(resizable=False)
        add_item_window.set_default_size(400, 500)
        add_item_window.set_modal(True)
        add_item_window.set_transient_for(self)
        box = Gtk.Box(orientation=1, vexpand=True)
        box.append(Gtk.Label(label=_("Add an item"), css_classes=["title-1"], margin_top=10, margin_bottom=10))
        list_box_add = Gtk.ListBox(selection_mode = 0, margin_start=6, margin_end=6,
                css_classes=["card"], vexpand=True)
        box.append(list_box_add)

        box3 = Gtk.Box(spacing=6, margin_start=6, margin_end=6, homogeneous=True)
        cancel_button = Gtk.Button(label=_("Cancel"), hexpand=True, margin_top=6, margin_bottom=6)
        cancel_button.connect("clicked", self.quit_window, add_item_window)
        add_button = Gtk.Button(label=_("Add"), hexpand=True, margin_top=6, margin_bottom=6)
        add_button.connect("clicked", self.add_item_to_list, list_box_add, add_item_window)
        box3.append(cancel_button)
        box3.append(add_button)

        box.append(box3)

        for i in range(len(self.column_details)):
            box2 = Gtk.Box()
            list_box_add.append(box2)
            box2.append(Gtk.Label(label=self.column_details[i][0], margin_start=6, xalign=0,
                    hexpand=True, width_request=200))
            if self.column_details[i][1] == "str":
                box2.append(Gtk.Entry(placeholder_text=_("Write here"),hexpand=True, margin_end=4, margin_top=4,
                        margin_bottom=4, width_request=200))
            if self.column_details[i][1] == "STR":
                box2.append(Gtk.Label(label=self.generate_new_id(), hexpand=True, margin_end=4, margin_top=4,
                        margin_bottom=4, width_request=200, xalign=0))
            if self.column_details[i][1] == "int":
                spin_button = Gtk.SpinButton(climb_rate=1,wrap=True, hexpand=True, margin_end=4, margin_top=4, margin_bottom=4, width_request=200)
                spin_button.set_adjustment(Gtk.Adjustment(step_increment=1, lower=0, value=0))
                box2.append(spin_button)
            if self.column_details[i][1] == "cost":
                spin_button = Gtk.SpinButton(climb_rate=1,wrap=True, hexpand=True, margin_end=4, margin_top=4, margin_bottom=4, width_request=200)
                spin_button.set_adjustment(Gtk.Adjustment(step_increment=1, lower=0, value=0))
                box2.append(spin_button)

        add_item_window.set_content(box)
        add_item_window.present()

    def add_item_to_list(self, btn, list_box_add, window):
        new_item =[]
        for i in range(len(self.column_details)):
            value_widget = list_box_add.get_row_at_index(i).get_child().get_first_child().get_next_sibling()
            if self.column_details[i][1] == "str":
                new_item.append(value_widget.get_text())
            if self.column_details[i][1] == "STR":
                new_item.append(value_widget.get_label())
            if self.column_details[i][1] == "int" or self.column_details[i][1] == "cost":
                new_item.append(int(value_widget.get_adjustment().get_value()))
        self.components.append(new_item)
        window.destroy()
        self.show_items()

    def generate_new_id(self):
        chars = ["0","1","3","3","4","5","6","7","8","9","A","B","C","D","E","F","G","H","I","L","M","N","O","P","Q","R","S","T","U","V","Z","J","K"]
        new_id = ""
        for i in range(self.id_lenght):
            new_id = new_id + random.choice(chars)
        for i in range(len(self.components[i][1])):
            if new_id == self.components[i][1]:
                new_id == self.generate_new_id()
        return new_id

    def add_item_row(self, ID):
        component_id = self.get_index_from_id(ID)
        box = Gtk.Box(css_classes=[], margin_start=10, hexpand=True, name=ID, homogeneous=True)

        for i in range(len(self.column_details)):
            try:
                self.components[component_id][i]
            except IndexError:
                text = ""
            else:
                text = self.components[component_id][i]
                if self.column_details[i][1] == "cost":
                    text = text + " €"
            box.append(Gtk.Label(label=text, ellipsize=3,
                halign=Gtk.Align.START, xalign=0, margin_start=12, hexpand=True))

        edit_button = Gtk.Button(icon_name="document-edit-symbolic", halign=Gtk.Align.CENTER,
                margin_start=6, margin_top=6, margin_bottom=6, name=self.components[component_id][1])

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
        self.revealer.set_reveal_child(False)
        self.dashboard_box = Gtk.Grid(row_homogeneous=True, column_homogeneous=True,
                row_spacing=10, column_spacing=10, margin_start=10, margin_top=10, margin_bottom=10, margin_end=10)
        self.content_srolled_window.set_child(self.dashboard_box)

        for i in range(self.dashboard_width):
            for j in range(self.dashboard_height):
                btn = Gtk.Button(css_classes=["flat"], icon_name="list-add-symbolic", name=str(i) + "," + str(j))
                btn.connect("clicked", self.add_dashboard_widget)
                self.dashboard_box.attach(btn, i, j, 1, 1)

        self.dashboard_box.attach(self.dashboard_simple_widget("Items", len(self.components)), 0,0,1,1)
        self.dashboard_box.attach(self.dashboard_simple_widget("Sold", len(self.components)), 0,1,1,1)
        self.dashboard_box.attach(self.dashboard_simple_widget("Items to sell", len(self.components)), 0,2,1,1)
        self.dashboard_box.attach(self.dashboard_progress_widget("Items to 100", len(self.components), 100), 1,0,2,1)

    def add_dashboard_widget(self, name, x, y, width, height):
        pass

    def dashboard_simple_widget(self, info_name, info):
        box = Gtk.Box(css_classes=["card"], margin_start=6, margin_end=6,
                margin_top=6, margin_bottom=6, hexpand=True, spacing = 6)
        box.append(Gtk.Label(label=info_name, hexpand=True, xalign=0, margin_start=10, margin_top=10, margin_bottom=10))
        box.append(Gtk.Label(label=info, hexpand=True, xalign=1, margin_end=10))
        return box
        
    def dashboard_progress_widget(self, info_name, info, total):
        box = Gtk.Box(css_classes=["card"], margin_start=6, margin_end=6,
                margin_top=6, margin_bottom=6, hexpand=True, spacing = 6, orientation=1)
        box.append(Gtk.Label(label=info_name, hexpand=True, xalign=0, margin_start=10, margin_top=10, margin_bottom=10))
        box.append(Gtk.ProgressBar(fraction=info/total, hexpand=True, margin_end=10, margin_start=10, margin_bottom=10))
        return box

    def add_dashboard_widget(self, btn):
        add_item_window = Adw.Window(resizable=False)
        add_item_window.set_default_size(400, 500)
        add_item_window.set_modal(True)
        add_item_window.set_transient_for(self)
        box = Gtk.Box(orientation=1, vexpand=True)
        box.append(Gtk.Label(label=_("Add a widget"), css_classes=["title-1"], margin_top=10, margin_bottom=10))
        list_box_add = Gtk.ListBox(selection_mode = 2, margin_start=6, margin_end=6,
                css_classes=["card"], vexpand=True)
        box.append(list_box_add)

        box3 = Gtk.Box(spacing=6, margin_start=6, margin_end=6, homogeneous=True)
        cancel_button = Gtk.Button(label=_("Cancel"), hexpand=True, margin_top=6, margin_bottom=6)
        cancel_button.connect("clicked", self.quit_window, add_item_window)
        add_button = Gtk.Button(label=_("Add"), hexpand=True, margin_top=6, margin_bottom=6)
        add_button.connect("clicked", self.add_dashboard_widget, 1, 1, 1, 1)
        box3.append(cancel_button)
        box3.append(add_button)

        box.append(box3)
        add_item_window.set_content(box)
        add_item_window.present()

        for i in range(len(self.dashboard_widgets)):
            box2 = Gtk.Box()
            box2.append(Gtk.Label(label=self.dashboard_widgets[i], margin_start=6, xalign=0,
                    hexpand=True, width_request=200))
            spin_button1 = Gtk.SpinButton(climb_rate=1,wrap=True, hexpand=True, margin_end=4, margin_top=4, margin_bottom=4, width_request=200)
            spin_button1.set_adjustment(Gtk.Adjustment(step_increment=1, lower=0, value=1))
            box2.append(spin_button1)
            spin_button2 = Gtk.SpinButton(climb_rate=1,wrap=True, hexpand=True, margin_end=4, margin_top=4, margin_bottom=4, width_request=200)
            spin_button2.set_adjustment(Gtk.Adjustment(step_increment=1, lower=0, value=1))
            box2.append(spin_button2)

            list_box_add.append(box2)
            
