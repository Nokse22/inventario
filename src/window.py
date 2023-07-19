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
import csv
import gettext
import locale
from os import path
from os.path import abspath, dirname, join, realpath
import os

class Item(GObject.Object):
    __gtype_name__ = "Item"

    def __init__(self):
        super().__init__()

        self._details = []

        for i in range(11):
            self._details.append(None)

    @GObject.Property(type=str)
    def item_id(self):
        return self._details[0]

    @GObject.Property(type=str)
    def item_category(self):
        return self._details[1]

    @GObject.Property(type=str)
    def item_name(self):
        return self._details[2]

    @GObject.Property(type=int)
    def item_quantity(self):
        return self._details[3]

    @GObject.Property(type=str)
    def item_package(self):
        return self._details[4]

    @GObject.Property(type=float)
    def item_cost(self):
        return self._details[5]

    @GObject.Property(type=float)
    def item_value(self):
        return self._details[6]

    @GObject.Property(type=str)
    def item_manufacturer(self):
        return self._details[7]

    @GObject.Property(type=str)
    def item_description(self):
        return self._details[8]

    @GObject.Property(type=str)
    def item_creation(self):
        return self._details[9]

    @GObject.Property(type=str)
    def item_mofification(self):
        return self._details[10]

    @GObject.Property(type=int)
    def details_all(self):
        return self._details

    def assign_value_at_index(self, index, value):
        self._details[index] = value



    def __repr__(self):
        text = "Item: "
        for i in range(len(self._details)):
            text = text + str(self.details_names[i][0]) + ": " +  str(self._details[i + 1]) + ", "
        return text

class InventarioWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'InventarioWindow'

    sidebar_options = ["Dashboard", "Items"]

    details_names = [
                    ["ID", "item_id", "STR"],
                    ["Category","item_category", "str"],
                    ["Name","item_name", "str"],
                    ["Quantity", "item_quantity", "int"],
                    ["Package", "item_package", "str"],
                    ["Cost", "item_cost", "cost"],
                    ["Value", "item_value", "cost"],
                    ["Manufacturer", "item_manufacturer", "str"],
                    ["Description", "item_description", "str"],
                    ["Created on", "item_creation", "str"],
                    ["Modified on", "item_mofification", "str"]
                    ]

    id_lenght = 5

    dashboard_width = 3
    dashboard_height = 10

    selected_item = None
    last_page = 1

    dashboard_widgets=["Simple value", "Progress bar"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.settings = Gio.Settings.new('io.github.nokse22.inventario')
        self.selected_item = self.settings.get_int("item-selected")
        self.last_page = self.settings.get_int("last-page")

        if self.settings.get_boolean("window-save"):
            self.settings.bind(
                "window-width", self, "default-width", Gio.SettingsBindFlags.DEFAULT
            )
            self.settings.bind(
                "window-height", self, "default-height", Gio.SettingsBindFlags.DEFAULT
            )
        else:
            self.set_default_size(1000, 700)

        self.split_view = Adw.NavigationSplitView()
        self.set_content(self.split_view)

        # Sidebar
        sidebar_page = Adw.NavigationPage()
        sidebar_page.set_title("")
        sidebar_page.set_tag("sidebar")

        sidebar_box = Gtk.Box(orientation=1)
        sidebar_page.set_child(sidebar_box)

        sidebar_headerbar = Adw.HeaderBar(css_classes=["flat"])
        #self.open_file_button = Gtk.MenuButton(icon_name="document-open-symbolic")
        #self.open_file_button.connect("clicked", self.show_file_chooser_dialog)
        # open_file_button_popover = Gtk.Popover(halign=Gtk.Align.START,
        #        has_arrow=True, width_request=200)
        open_file_button = Gtk.MenuButton()
        adw_open_button_content = Adw.ButtonContent(icon_name="document-open-symbolic", label="Open")
        open_file_button.set_child(adw_open_button_content)

        # open_menu = Gio.Menu()
        # open_menu.append_section()
        # open_menu.append(_("New inventory"), )
        # open_menu.append(_("Import items from file"), )
        # open_menu.append(_("Save"), )

        # Create the open_menu
        open_menu = Gio.Menu()

        # Create menu sections
        open_menu_section = Gio.Menu()
        open_menu_section.append("New inventory", "app.new-inventory")
        open_menu.append_section(None, open_menu_section)

        open_menu_section = Gio.Menu()
        open_menu_section.append("Save", "app.save")
        open_menu_section.append("Save As", "app.save-as")
        open_menu.append_section(None, open_menu_section)

        open_menu_section = Gio.Menu()
        open_menu_section.append("Open", "app.open-inventory")
        open_menu_section.append("Import", "app.import")
        open_menu.append_section(None, open_menu_section)


        open_file_button.set_menu_model(open_menu)

        # open_file_button_popover_box = Gtk.Box(hexpand=True)
        # open_file_button_popover.set_child(open_file_button_popover_box)

        # new_inventory_button = Gtk.Button()
        # new_inventory_button.set_child(Gtk.Label(label=_("New inventory"),hexpand=True, xalign=0))
        # open_file_button_popover_box.append(new_inventory_button)

        sidebar_headerbar.pack_start(open_file_button)
        sidebar_box.append(sidebar_headerbar)

        # Content
        content_page = Adw.NavigationPage()
        content_page.set_title("Inventario")
        content_page.set_tag("content")

        self.content_box = Gtk.Box(orientation=1)
        content_page.set_child(self.content_box)

        content_headerbar = Adw.HeaderBar(css_classes=["flat"])
        self.content_box.append(content_headerbar)

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

        delete_item_button = Gtk.Button(css_classes=["error"])
        delete_item_button.set_icon_name("user-trash-symbolic")
        delete_item_button.connect("clicked", self.on_delete_item_button_clicked)

        search_button = Gtk.Button()
        search_button.set_icon_name("system-search-symbolic")
        search_button.connect("clicked", self.search_item)

        self.search_revealer = Gtk.Revealer(transition_type=2)
        search_entry = Gtk.Entry(placeholder_text=_("Search"))
        self.search_revealer.set_child(search_entry)
        #search_entry.connect("focus-out", self.search_item)

        # add_menu = Gio.Menu()
        # add_menu.append(_("Item"), None)
        # add_menu.append(_("Description"), None)
        # add_button.set_menu_model(add_menu)

        content_headerbar.pack_end(menu_button)
        content_headerbar.pack_start(self.search_revealer)
        content_headerbar.pack_start(search_button)

        self.content_srolled_window = Gtk.ScrolledWindow(vexpand=True, overlay_scrolling=True)
        self.content_srolled_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.toast_overlay = Adw.ToastOverlay()
        self.toast_overlay.set_child(self.content_srolled_window)
        self.content_box.append(self.toast_overlay)

        self.action_bar = Gtk.ActionBar()
        self.action_bar_revealer = Gtk.Revealer(transition_type=1)
        self.action_bar_revealer.set_child(self.action_bar)

        column_visibility_popover = Gtk.Popover(halign=Gtk.Align.END, has_arrow=False)
        column_visibility_popover.set_position(Gtk.PositionType.TOP)
        column_visibility_popover.set_offset(0,-6)
        column_visibility_button = Gtk.MenuButton(icon_name="open-menu-symbolic", popover = column_visibility_popover)

        self.action_bar.pack_end(column_visibility_button)
        self.action_bar.pack_start(add_button)
        self.action_bar.pack_start(delete_item_button)

        self.content_box.append(self.action_bar_revealer)

        #Navigation
        sidebar_srolled_window = Gtk.ScrolledWindow(vexpand=True)
        self.sidebar_navigation_listBox = Gtk.ListBox(css_classes=["navigation-sidebar"])
        self.sidebar_navigation_listBox.connect("row-activated", self.on_navigation_row_activated)
        sidebar_box.append(sidebar_srolled_window)
        sidebar_srolled_window.set_child(self.sidebar_navigation_listBox)


        self.sidebar_srolled_window_item_info = Gtk.ScrolledWindow(vexpand=True)
        self.sidebar_srolled_window_item_info.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.item_info_revealer = Gtk.Revealer(transition_type=1)

        self.item_info_revealer.set_child(self.sidebar_srolled_window_item_info)
        sidebar_box.append(self.item_info_revealer)

        self.model = Gio.ListStore(item_type=Item)

        # for n in self.nodes.keys():
        #     new_item = Item()
        #     for i, detail in enumerate(self.details_names):
        #         if i == 0:
        #             new_item.assign_value_at_index(i, n)
        #         else:
        #             try:
        #                 self.nodes[n][i - 1]
        #             except:
        #                 pass
        #             else:
        #                 new_item.assign_value_at_index(i, self.nodes[n][i - 1])
        #     self.model.append(new_item)

        for i in range(len(self.sidebar_options)):
            self.sidebar_navigation_listBox.append(Gtk.Label(label = self.sidebar_options[i], xalign=0))

        self.show_dashboard()

        self.cv = Gtk.ColumnView(single_click_activate=False, reorderable=True, enable_rubberband=True,
                show_row_separators=True, css_classes=["flat"])
        tree_model = Gtk.TreeListModel.new(self.model, False, True, self.model_func)
        tree_sorter = Gtk.TreeListRowSorter.new(self.cv.get_sorter())
        sorter_model = Gtk.SortListModel(model=tree_model, sorter=tree_sorter)
        selection = Gtk.SingleSelection.new(model=sorter_model)
        self.cv.set_model(selection)
        self.cv.connect("activate", self.on_column_view_activated)

        for i in range(len(self.details_names)):
            self.add_column(self.details_names[i][0], self.details_names[i][1])

        column_visibility_popover_box = Gtk.Box(orientation=1)
        for i, column in enumerate(self.cv.get_columns()):
            title = column.get_title()
            box = Gtk.Box(orientation=0)
            box.append(Gtk.Label(label=title, hexpand=True, xalign=0, margin_end=10))
            check_button = Gtk.CheckButton(active = column.get_visible())
            check_button.connect("toggled", self.on_check_button_toggled, column)
            box.append(check_button)
            column_visibility_popover_box.append(box)
        column_visibility_popover.set_child(column_visibility_popover_box)

        self.split_view.set_sidebar(sidebar_page)
        self.split_view.set_content(content_page)

        self.navigation_select_page(self.last_page)

    def on_delete_item_button_clicked(self, btn):
        pass

    def on_check_button_toggled(self, check, column):
        column.set_visible(not column.get_visible())

    def on_file_selected(self, dialog, response):
        if response == -3:
            selected_file = dialog.get_file()
            if selected_file:
                file_path = selected_file.get_path()
                try:
                    open(file_path, 'r').read()
                except Exception as e:
                    dialog.destroy()
                    toast = Adw.Toast()
                    toast.set_title("Error reading file:" + str(e))
                    toast.set_timeout(2)
                    self.toast_overlay.add_toast(toast)
                else:
                    with open(file_path, 'r') as file:
                        file_contents = file.read()
                        file_extension = os.path.splitext(file_path)[1]
                        dialog.destroy()
                        toast = Adw.Toast()
                        toast.set_title("File successfully opened")
                        toast.set_timeout(1)
                        self.toast_overlay.add_toast(toast)

                        if file_extension == ".csv":
                            self.read_csv(file_contents)
                        if file_extension == ".json":
                            self.read_json(file_contents)
        else:
            dialog.destroy()

    def show_file_chooser_dialog(self, btn):

        dialog = Gtk.FileChooserNative(
            title="Open File",
            transient_for=None,
            action=Gtk.FileChooserAction.OPEN,
        )

        dialog.set_accept_label("Open")
        dialog.set_cancel_label("Cancel")

        # Show the dialog and get the response
        response = dialog.show()

        dialog.connect("response", self.on_file_selected)

    def read_json(self):
        pass

    def read_csv(self, file_content):
        reader = csv.reader(file_content.splitlines())
        for row in reader:
            new_item = Item()
            for index, value in enumerate(row):
                if value:
                    try:
                        type_info = self.details_names[index][2]
                        #print(str(type_info) + " is "+str(value))
                        if type_info == "str" or type_info == "STR":
                            new_value = str(value)
                        elif type_info == "int":
                            new_value = int(value)
                        elif type_info == "cost":
                            new_value = float(value)
                        else:
                            continue

                        new_item.assign_value_at_index(index, new_value)
                    except (ValueError, TypeError):
                        # Handle any conversion errors
                        pass

            self.model.append(new_item)

    def on_screen_changed(self, window):
        settings.set_int("window-width", window.get_allocated_width())
        settings.set_int("window-height", window.get_allocated_height())

    def search_item(self, btn):
        self.search_revealer.set_reveal_child(not self.search_revealer.get_reveal_child())

    def on_column_view_activated(self, cv, row):
        if len(self.model) == 0:
            return
        if row > len(self.model):
            row = 0
        self.selected_item = row
        self.sidebar_item_info_list_box = Gtk.ListBox(show_separators=False, selection_mode=0,
                margin_start=6, margin_end=6, margin_top=6, margin_bottom=6, vexpand=True)
        #self.sidebar_item_info_list_box.append(Gtk.Image(icon_name="document-edit-symbolic", icon_size=10))
        box1 = Gtk.Box(orientation=1, css_classes=["card"],
                margin_start=6, margin_end=6, margin_top=6, margin_bottom=6)
        box1.append(self.sidebar_item_info_list_box)

        item_id=self.model[row].details_all[0]

        add_this_button = Gtk.Button(hexpand=True, label="Add", css_classes=["success"], name=item_id)
        remove_this_button = Gtk.Button(hexpand=True, label="-1", css_classes=["error"], name=item_id)
        box2 = Gtk.Box(homogeneous=True, margin_start=6, margin_end=6, margin_top=6, margin_bottom=6, hexpand=True, spacing=6)
        box2.append(add_this_button)
        box2.append(remove_this_button)

        add_this_button.connect("clicked", self.on_add_one_item_button_clicked)
        remove_this_button.connect("clicked", self.on_remove_one_item_button_clicked)

        box1.append(box2)
        self.sidebar_srolled_window_item_info.set_child(box1)
        self.item_info_revealer.set_reveal_child(True)

        for i in range(len(self.details_names)):
            box = Gtk.Box(margin_start=6, margin_end=6)
            name = self.details_names[i][0] + ":"
            box.append(Gtk.Label(ellipsize=2, label=name, xalign=0, hexpand=True, margin_end=6))
            try:
                self.model[row].details_all[i]
            except IndexError:
                text = "..."
            else:
                text = self.model[row].details_all[i]
            box.append(Gtk.Label(label=text, xalign=1, hexpand=True))
            self.sidebar_item_info_list_box.append(box)

    def on_add_one_item_button_clicked(self, btn):
        item = self.get_item_by_id(btn.get_name())
        item.details_all[2] += 1
        self.on_column_view_activated(self.cv, self.selected_item)

        add_item_window = Adw.Window(resizable=False)
        add_item_window.set_title("Add item")
        add_item_window.set_default_size(400, 500)
        add_item_window.set_modal(True)
        add_item_window.set_transient_for(self)
        box = Gtk.Box(orientation=1, vexpand=True)
        box.append(Adw.HeaderBar(css_classes=["flat"]))
        list_box_add = Gtk.ListBox(selection_mode = 0, margin_start=6, margin_end=6,
                css_classes=["card"], vexpand=True)
        box.append(list_box_add)

        box3 = Gtk.Box(spacing=6, margin_start=6, margin_end=6, homogeneous=True)
        cancel_button = Gtk.Button(label=_("Cancel"), hexpand=True, margin_top=6, margin_bottom=6)
        cancel_button.connect("clicked", self.quit_window, add_item_window)
        add_button = Gtk.Button(label=_("Add"), hexpand=True, margin_top=6, margin_bottom=6)
        add_button.connect("clicked", self.add_existing_item, list_box_add)
        box3.append(cancel_button)
        box3.append(add_button)
        box.append(box3)

        add_item_window.set_content(box)
        add_item_window.present()

    def add_existing_item(self, btn, list_box):
        pass

    def on_remove_one_item_button_clicked(self, btn):
        item = self.get_item_by_id(btn.get_name())
        item.details_all[2] -= 1
        self.on_column_view_activated(self.cv, self.selected_item)

    def get_item_by_id(self, item_id):
        for item in self.model:
            if item.details_all[0] == item_id:
                return item
    def on_item_row_activated(self, list_box, exc):
        item_row_name = list_box.get_selected_row().get_child().get_name()
        index = self.get_index_from_id(item_row_name)

    def model_func(self, args):
        #print(args)
        pass

    def add_column(self, column_name, detail):
        factory = Gtk.SignalListItemFactory()
        factory.connect("setup", self._on_factory_setup)
        factory.connect("bind", self._on_factory_bind, detail)
        factory.connect("unbind", self._on_factory_unbind, detail)
        factory.connect("teardown", self._on_factory_teardown)

        col1 = Gtk.ColumnViewColumn(title=column_name, factory=factory, resizable=True)#, sorter = Gtk.StringSorter()
        col1.props.expand = True
        self.cv.append_column(col1)

    def show_items(self):
        self.content_srolled_window.set_child(self.cv)
        self.action_bar_revealer.set_reveal_child(True)
        if self.selected_item != None:
            self.on_column_view_activated(self.cv, self.selected_item)
            self.cv.get_model().select_item(self.selected_item, True)

    def _on_factory_setup(self, factory, list_item):
        cell = Gtk.Inscription()
        cell._binding = None
        list_item.set_child(cell)

    def _on_factory_bind(self, factory, list_item, what):
        cell = list_item.get_child()
        item = list_item.get_item().get_item()
        try:
            item.bind_property(what, cell, "text", GObject.BindingFlags.SYNC_CREATE)
        except:
            pass
        else:
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

    def quit_window(self, btn, window):
        window.destroy()

    def add_item(self, args):
        add_item_window = Adw.Window(resizable=False)
        add_item_window.set_title("Add a new item")
        add_item_window.set_default_size(400, 500)
        add_item_window.set_modal(True)
        add_item_window.set_transient_for(self)
        box = Gtk.Box(orientation=1, vexpand=True)
        box.append(Adw.HeaderBar(css_classes=["flat"]))
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

        for i in range(len(self.details_names)):
            box2 = Gtk.Box()
            list_box_add.append(box2)
            box2.append(Gtk.Label(label=self.details_names[i][0], margin_start=6, xalign=0,
                    hexpand=True, width_request=200))
            if self.details_names[i][2] == "str":
                box2.append(Gtk.Entry(placeholder_text=_("Write here"),hexpand=True, margin_end=4, margin_top=4,
                        margin_bottom=4, width_request=200))
            if self.details_names[i][2] == "STR":
                box2.append(Gtk.Label(label=self.generate_new_id(), hexpand=True, margin_end=4, margin_top=4,
                        margin_bottom=4, width_request=200, xalign=0))
            if self.details_names[i][2] == "int":
                spin_button = Gtk.SpinButton(climb_rate=1, hexpand=True, margin_end=4, margin_top=4, margin_bottom=4, width_request=200)
                spin_button.set_adjustment(Gtk.Adjustment(step_increment=1, lower=0, value=0, upper=100000000))
                box2.append(spin_button)
            if self.details_names[i][2] == "cost":
                spin_button = Gtk.SpinButton(climb_rate=1, digits=2, hexpand=True, margin_end=4, margin_top=4, margin_bottom=4, width_request=200)
                spin_button.set_adjustment(Gtk.Adjustment(step_increment=0.01, lower=0, value=0, upper=100000000))
                box2.append(spin_button)

        add_item_window.set_content(box)
        add_item_window.present()

    def add_item_to_list(self, btn, list_box_add, window):
        new_item = Item()
        for i in range(len(self.details_names)):
            value_widget = list_box_add.get_row_at_index(i).get_child().get_first_child().get_next_sibling()
            if self.details_names[i][2] == "str":
                value = value_widget.get_text()
            if self.details_names[i][2] == "STR":
                value = value_widget.get_label()
            if self.details_names[i][2] == "int" or self.details_names[i][2] == "cost":
                value = value_widget.get_value()
            new_item.assign_value_at_index(i, value)
        self.model.append(new_item)
        window.destroy()

    def generate_new_id(self):
        chars = ["0","1","3","3","4","5","6","7","8","9","A","B","C","D","E","F","G","H","I","L","M","N","O","P","Q","R","S","T","U","V","Z","J","K"]
        new_id = ""
        for i in range(self.id_lenght):
            new_id = new_id + random.choice(chars)
        for i in range(len(self.model)):
            if new_id == self.model[i].details_all[0]:
                new_id == self.generate_new_id()
        return new_id

    def toggle_sidebar(self, btn):
        self.split_view.set_collapsed(self.split_view.get_collapsed)

    def on_navigation_row_activated(self, list_box, exc):
        selected_row = list_box.get_selected_row()

        self.split_view.set_collapsed(False)
        if selected_row.get_child().get_label() == "Dashboard":
            self.show_dashboard()
            self.last_page = 0
        elif selected_row.get_child().get_label() == "Items":
            self.show_items()
            self.last_page = 1

    def navigation_select_page(self, index):
        selected_row = self.sidebar_navigation_listBox.get_row_at_index(index)
        self.sidebar_navigation_listBox.select_row(selected_row)
        if selected_row.get_child().get_label() == "Dashboard":
            self.show_dashboard()
        elif selected_row.get_child().get_label() == "Items":
            self.show_items()

    def show_dashboard(self):
        self.item_info_revealer.set_reveal_child(False)
        self.action_bar_revealer.set_reveal_child(False)
        self.dashboard_box = Gtk.Grid(row_homogeneous=True, column_homogeneous=True,
                row_spacing=10, column_spacing=10, margin_start=10, margin_top=10, margin_bottom=10, margin_end=10)
        self.content_srolled_window.set_child(self.dashboard_box)

        for i in range(self.dashboard_width):
            for j in range(self.dashboard_height):
                btn = Gtk.Button(css_classes=["flat"], icon_name="list-add-symbolic", name=str(i) + "," + str(j))
                btn.connect("clicked", self.add_dashboard_widget)
                self.dashboard_box.attach(btn, i, j, 1, 1)

        self.dashboard_box.attach(self.dashboard_simple_widget("Items", len(self.model)), 0,0,1,1)
        self.dashboard_box.attach(self.dashboard_simple_widget("Sold", len(self.model)), 0,1,1,1)
        self.dashboard_box.attach(self.dashboard_simple_widget("Value", str(self.get_inventory_value()) + " €"), 0,2,1,1)
        self.dashboard_box.attach(self.dashboard_progress_widget("Items to 100", len(self.model), 100), 1,0,2,1)

    def get_inventory_value(self):
        total = 0
        for i in range(len(self.model)):
            cost = self.model[i].details_all[5]
            stock = self.model[i].details_all[3]
            if cost != None and stock != None:
                total += cost * stock
        return total


    def add_dashboard_widget(self, name, x, y, width, height):
        pass

    def dashboard_big_text_widget(self, info_name, info):
        box = Gtk.Box(css_classes=["card"], margin_start=6, margin_end=6,
                margin_top=6, margin_bottom=6, hexpand=True, spacing = 6)
        box.append(Gtk.Label(label=info_name, hexpand=True, xalign=0, margin_start=10, margin_top=10, margin_bottom=10))
        box.append(Gtk.Label(label=info, hexpand=True, xalign=1, margin_end=10))
        return box

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
        add_item_window.set_default_size(800, 700)
        add_item_window.set_modal(True)
        add_item_window.set_title(_("Add a widget"))
        add_item_window.set_transient_for(self)
        box = Gtk.Box(orientation=1, vexpand=True)
        box.append(Adw.HeaderBar(css_classes=["flat"]))
        list_box_add = Gtk.ListBox(selection_mode = 0, margin_start=6, margin_end=6,
                css_classes=["card"])
        box.append(list_box_add)

        box3 = Gtk.Box(spacing=6, margin_start=6, margin_end=6, homogeneous=True)
        cancel_button = Gtk.Button(label=_("Cancel"), hexpand=True, margin_top=6, margin_bottom=6)
        cancel_button.connect("clicked", self.quit_window, add_item_window)
        add_button = Gtk.Button(label=_("Add"), hexpand=True, margin_top=6, margin_bottom=6)
        add_button.connect("clicked", self.add_dashboard_widget, 1, 1, 1, 1)

        #self.dashboard_simple_widget("Items", len(self.model)))
        grid = Gtk.Grid(row_homogeneous=True, column_homogeneous=True, vexpand=True,
                row_spacing=10, column_spacing=10, margin_start=10, margin_top=10, margin_bottom=10, margin_end=10)
        box.append(grid)
        for i in range(3):
            for j in range(2):
                grid.attach(Gtk.Label(label="o"), i, j, 1, 1)

        box3.append(cancel_button)
        box3.append(add_button)

        box.append(box3)
        add_item_window.set_content(box)
        add_item_window.present()

        options = ["Widget", "Start position X", "Start position Y", "Width", "Height"]

        combo_box = Gtk.ComboBoxText(width_request=200, hexpand=True, margin_end=4, margin_top=4, margin_bottom=4)
        widget_box = Gtk.Box()
        widget_box.append(Gtk.Label(label="Widget", margin_start=6, xalign=0, hexpand=True, width_request=200))
        widget_box.append(combo_box)
        list_box_add.append(widget_box)

        for string in self.dashboard_widgets:
            combo_box.append_text(string)

        start_x_box = Gtk.Box()
        start_x_box.append(Gtk.Label(label="Start position X", margin_start=6, xalign=0, hexpand=True, width_request=200))
        start_x_box.append(combo_box)
        spin_button_start_x = Gtk.SpinButton(climb_rate=1, hexpand=True, margin_end=4, margin_top=4, margin_bottom=4, width_request=200)
        spin_button_start_x.set_adjustment(Gtk.Adjustment(step_increment=1, lower=0, value=1, upper=10))
        start_x_box.append(spin_button_start_x)
        list_box_add.append(start_x_box)

        start_y_box = Gtk.Box()
        start_y_box.append(Gtk.Label(label="Start position Y", margin_start=6, xalign=0, hexpand=True, width_request=200))
        start_y_box.append(combo_box)
        spin_button_start_y = Gtk.SpinButton(climb_rate=1, hexpand=True, margin_end=4, margin_top=4, margin_bottom=4, width_request=200)
        spin_button_start_y.set_adjustment(Gtk.Adjustment(step_increment=1, lower=0, value=1, upper=10))
        start_y_box.append(spin_button_start_y)
        list_box_add.append(start_y_box)

        width_box = Gtk.Box()
        width_box.append(Gtk.Label(label="Width", margin_start=6, xalign=0, hexpand=True, width_request=200))
        width_box.append(combo_box)
        spin_button_width = Gtk.SpinButton(climb_rate=1, hexpand=True, margin_end=4, margin_top=4, margin_bottom=4, width_request=200)
        spin_button_width.set_adjustment(Gtk.Adjustment(step_increment=1, lower=1, value=1, upper=3))
        width_box.append(spin_button_width)
        list_box_add.append(width_box)

        height_box = Gtk.Box()
        height_box.append(Gtk.Label(label="Height", margin_start=6, xalign=0, hexpand=True, width_request=200))
        height_box.append(combo_box)
        spin_button_height = Gtk.SpinButton(climb_rate=1, hexpand=True, margin_end=4, margin_top=4, margin_bottom=4, width_request=200)
        spin_button_height.set_adjustment(Gtk.Adjustment(step_increment=1, lower=1, value=1, upper=2))
        height_box.append(spin_button_height)
        list_box_add.append(height_box)

        combo_box.connect("changed", self.on_widget_changed, combo_box, grid,
                    spin_button_width,
                    spin_button_height)
        spin_button_height.connect("changed", self.on_widget_changed, combo_box, grid,
                    spin_button_width,
                    spin_button_height)
        spin_button_width.connect("changed", self.on_widget_changed, combo_box, grid,
                    spin_button_width,
                    spin_button_height)
        self.simple_widget = self.dashboard_simple_widget("Name", 20)
        self.progress_widget = self.dashboard_progress_widget("Name", 20, 100)

    def on_widget_changed(self, a, combo, grid, x, y):
        try:
            grid.remove(self.simple_widget)
        except Exception:
            pass

        try:
            grid.remove(self.progress_widget)
        except Exception:
            pass



        self.simple_widget = self.dashboard_simple_widget(combo.get_active_text(), 20)
        self.progress_widget = self.dashboard_progress_widget(combo.get_active_text(), 20, 100)

        if combo.get_active_text() == self.dashboard_widgets[0]:
            grid.attach(self.simple_widget, 0, 0, x.get_value(), y.get_value())
            
