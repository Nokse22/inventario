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

import datetime
import random
import csv
import gettext
import locale
import threading
from os import path
from os.path import abspath, dirname, join, realpath
import os
import inspect
import time

class Item(GObject.Object):
    __gtype_name__ = "Item"

    def __init__(self, lenght):
        super().__init__()

        self._item_id = None
        self._item_category = None
        self._item_name = None
        self._item_quantity = None
        self._item_package = None
        self._item_cost = None
        self._item_value = None
        self._item_manufacturer = None
        self._item_description = None
        self._item_creation = None
        self._item_modification = None
        self._item_selling_price = None
        self._item_stock_reserved = None
        self._item_stock_allocated = None
        self._item_stock_planned = None
        self._item_stock_on_order = None
        self._item_stock_for_sale = None
        self._item_storage = None
        self._unit_of_measure = None
        self._item_part_number = None
        self._item_seller = None
        self._item_custom_values_list = []

    @GObject.Property(type=str)
    def item_unit_of_measure(self):
        return self._unit_of_measure

    @GObject.Property(type=str)
    def item_id(self):
        return self._item_id

    @GObject.Property(type=str)
    def item_category(self):
        return self._item_category

    @GObject.Property(type=str)
    def item_name(self):
        return self._item_name

    @GObject.Property(type=int)
    def item_quantity(self):
        return self._item_quantity

    @GObject.Property(type=str)
    def item_package(self):
        return self._item_package

    @GObject.Property(type=str)
    def item_cost(self):
        return self._item_cost

    @GObject.Property(type=str)
    def item_value(self):
        if self._item_value in ["0", "0.0", "0.0 ", "0.0  ", "0.0   "]:
            return None
        return self._item_value

    @GObject.Property(type=str)
    def item_manufacturer(self):
        return self._item_manufacturer

    @GObject.Property(type=str)
    def item_description(self):
        return self._item_description

    @GObject.Property(type=str)
    def item_creation(self):
        return self._item_creation

    @GObject.Property(type=str)
    def item_modification(self):
        return self._item_modification

    @GObject.Property(type=str)
    def item_selling_price(self):
        return self._item_selling_price

    @GObject.Property(type=int)
    def item_stock_reserved(self):
        return self._item_stock_reserved

    @GObject.Property(type=int)
    def item_stock_allocated(self):
        return self._item_stock_allocated

    @GObject.Property(type=int)
    def item_stock_planned(self):
        return self._item_stock_planned

    @GObject.Property(type=int)
    def item_stock_on_order(self):
        return self._item_stock_on_order

    @GObject.Property(type=int)
    def item_stock_for_sale(self):
        return self._item_stock_for_sale

    @GObject.Property(type=str)
    def item_storage(self):
        return self._item_storage

    @GObject.Property(type=str)
    def item_part_number(self):
        return self._item_part_number

    @GObject.Property(type=str)
    def item_seller(self):
        return self._item_seller



    def custom_values_list(self):
        return self._item_custom_values_list

    def set_custom_values_at_index(self, index, value):
        self._item_custom_values_list[index] = value

    def append_custom_value(self, name, value):
        self._item_custom_values_list.append([name, value])

    def get_detail(self, name):
        return getattr(self, name, None)

    # def assign_value(self, name, value):
    #     getattr(self, name, None) = value
        #self._details[index] = value

    def set_detail(self, detail_name, value):
        attributes = inspect.getmembers(self, lambda a: not inspect.isroutine(a))

        for attr_name, _ in attributes:
            if attr_name == f"_{detail_name}":
                setattr(self, f"_{detail_name}", value)
                return

        raise ValueError(f"Invalid detail name: {detail_name}")

    def __repr__(self):
        text = "Item: "
        return text + self.item_id

class InventarioWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'InventarioWindow'

    sidebar_options = ["Dashboard", "Items", "Invoice", "Products"]

    # TO ADD A NEW CATEGORY:
    # add a new entry in the following array like: ["Column name", "Item function to retrieve the value", "type"]
    # the types are:
    # - STR immutable string
    # - str mutable string
    # - int mutable integer
    # - cost price/cost, can be displayed as a currency, stored as a float
    # - value has a unit of measure, stored as a float
    # - date mutable string containing a date, only used for the last modification
    # - DATE immutable date used for the creation date

    # then add a new function in the Item class:
    #
    # @GObject.Property(type=str)
    # def item_storage(self):
    #     return self._details[17])
    #
    # do not change the order of the item details in the Item class,
    # to change the order of the visualized column you can just change it in the following array

    details_names = [
                    ["ID", "item_id", "STR"],
                    ["Category","item_category", "cat"],
                    ["Name","item_name", "str"],
                    ["Stock", "item_quantity", "int"],
                    ["Package", "item_package", "str"],
                    ["Part Number","item_part_number", "str"],
                    ["Price", "item_cost", "cost"],
                    ["Value", "item_value", "value"],
                    ["Manufacturer", "item_manufacturer", "str"],
                    ["Seller", "item_seller", "str"],
                    ["Storage location", "item_storage", "str"],
                    ["Description", "item_description", "str"],
                    ["Selling Price", "item_selling_price", "cost"],
                    ["Stock Reserved", "item_stock_reserved", "int"],
                    ["Stock Allocated", "item_stock_allocated", "int"],
                    ["Stock Planned", "item_stock_planned", "int"],
                    ["Stock on Order", "item_stock_on_order", "int"],
                    ["Stock for Sale", "item_stock_for_sale", "int"],
                    ["Created on", "item_creation", "DATE"],
                    ["Modified on", "item_modification", "date"],
                    ]
    units_of_measure = ["  ",
                   "F", "nF", "uF", "pF",
                   "MΩ", "kΩ", "Ω", "mΩ", "μΩ", "nΩ",
                   "H", "mH", "μH", "nH",
                   "V", "mV", "μV",
                   "A", "mA", "μA",
                   "W", "mW",
                   "Hz", "kHz", "MHz", "GHz",
                   "kg", "g",
                   "m", "mm", "cm", "km",
                   "MV", "kV", "V", "mV", "μV", "nV"]

    categories = ["ELECTRONICS", "MECHANICAL", "CONSUMABLE"]

    details_lenght = len(details_names)

    id_lenght = 5

    dashboard_width = 4
    dashboard_height = 10

    selected_item = 0
    last_page = 1

    dashboard_widgets=["Simple value", "Progress bar"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.settings = Gio.Settings.new('io.github.nokse22.inventario')
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
        open_file_button = Gtk.MenuButton()
        adw_open_button_content = Adw.ButtonContent(icon_name="document-open-symbolic", label="Open/save")
        open_file_button.set_child(adw_open_button_content)

        open_menu = Gio.Menu()

        open_menu_section = Gio.Menu()
        open_menu_section.append("New inventory", "app.new-inventory")
        open_menu.append_section(None, open_menu_section)

        open_menu_section = Gio.Menu()
        open_menu_section.append("Save", "app.save")
        open_menu_section.append("Save As", "app.save-as")
        open_menu.append_section(None, open_menu_section)

        open_menu_section = Gio.Menu()
        open_menu_section.append("Open File", "app.open-inventory")
        open_menu_section.append("Import", "app.import")
        open_menu.append_section(None, open_menu_section)

        open_file_button.set_menu_model(open_menu)

        sidebar_headerbar.pack_start(open_file_button)
        sidebar_box.append(sidebar_headerbar)

        # Content
        content_page = Adw.NavigationPage()
        content_page.set_title("Inventario")
        content_page.set_tag("content")

        self.content_box = Gtk.Box(orientation=1)
        content_page.set_child(self.content_box)

        title_box = Gtk.Box(orientation=1, valign=Gtk.Align.CENTER)

        self.title_label = Gtk.Label(label="Inventario", css_classes=["title-4"], ellipsize=3)
        title_box.append(self.title_label)

        self.subtitle_label = Gtk.Label(visible=False,label="~/", css_classes=["caption"], opacity=0.6, ellipsize=1)
        title_box.append(self.subtitle_label)

        content_headerbar = Gtk.HeaderBar(css_classes=["flat"], title_widget=title_box)
        self.content_box.append(content_headerbar)

        self.search_button_toggle = Gtk.ToggleButton()
        self.search_button_toggle.set_icon_name("pan-down-symbolic")
        self.search_button_toggle.connect("clicked", self.toggle_search_bar)

        self.search_revealer = Gtk.Revealer(transition_type=4)

        self.search_entry = Gtk.Entry(placeholder_text=_("Search"), hexpand=True,
                primary_icon_name="dialog-information-symbolic",
                primary_icon_tooltip_text="Use ! then > or < to filter values",
                primary_icon_sensitive=False,
                secondary_icon_name="edit-clear-symbolic")
        #self.search_entry.set_property(primary_icon_name, "info-symbolic")

        self.search_entry.connect("activate", self.filter_rows)
        self.search_entry.connect("changed", self.entry_text_inserted)

        self.search_entry.connect("icon-press", self.delete_search_text)

        search_button = Gtk.Button(icon_name="system-search-symbolic")
        delete_search_button = Gtk.Button(icon_name="edit-delete-symbolic")

        self.search_selector = Gtk.ComboBoxText(hexpand=True)

        search_box = Gtk.FlowBox(margin_start=4, margin_end=4, margin_bottom=4,
                selection_mode=Gtk.SelectionMode.NONE)

        search_button.connect("clicked", self.filter_rows)
        delete_search_button.connect("clicked", self.delete_filter_rows)

        search_box.append(self.search_entry)

        options_box = Gtk.Box(spacing=6)
        search_box.append(options_box)
        options_box.append(self.search_selector)
        options_box.append(search_button)
        options_box.append(delete_search_button)

        for detail in self.details_names:
            self.search_selector.append_text(detail[0])
        self.search_selector.set_active(2)

        self.search_revealer.set_child(search_box)

        self.content_box.append(self.search_revealer)

        toggle_sidebar_button = Gtk.Button(icon_name="go-previous-symbolic", visible=False)
        toggle_sidebar_button.connect("clicked", self.toggle_sidebar)
        content_headerbar.pack_start(toggle_sidebar_button)

        menu_button = Gtk.MenuButton()
        menu_button.set_icon_name("open-menu-symbolic")
        menu = Gio.Menu()
        menu.append(_("Preferences"), "app.preferences")
        menu.append(_("Keyboard shorcuts"), "win.show-help-overlay")
        menu.append(_("About"), "app.about")
        menu_button.set_menu_model(menu)

        add_button = Gtk.Button()
        add_button.set_icon_name("list-add-symbolic")
        add_button.connect("clicked", self.add_new_item_dialog)

        delete_item_button = Gtk.Button(css_classes=["error"])
        delete_item_button.set_icon_name("user-trash-symbolic")
        delete_item_button.connect("clicked", self.on_delete_item_button_clicked)

        content_headerbar.pack_end(menu_button)
        #content_headerbar.pack_start(self.search_revealer)
        content_headerbar.pack_start(self.search_button_toggle)

        self.content_scrolled_window = Gtk.ScrolledWindow(vexpand=True, overlay_scrolling=True)
        self.content_scrolled_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.toast_overlay = Adw.ToastOverlay()
        self.toast_overlay.set_child(self.content_scrolled_window)
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
        sidebar_scrolled_window = Gtk.ScrolledWindow(vexpand=True)
        self.sidebar_navigation_listBox = Gtk.ListBox(css_classes=["navigation-sidebar"])
        self.sidebar_navigation_listBox.connect("row-activated", self.on_navigation_row_activated)
        sidebar_box.append(sidebar_scrolled_window)
        sidebar_scrolled_window.set_child(self.sidebar_navigation_listBox)

        self.item_info_revealer = Gtk.Revealer(transition_type=1, height_request=300)
        sidebar_box.append(self.item_info_revealer)

        self.model = Gio.ListStore(item_type=Item)

        for i in range(len(self.sidebar_options)):
            self.sidebar_navigation_listBox.append(Gtk.Label(label = self.sidebar_options[i], xalign=0))

        self.show_dashboard()

        self.cv = Gtk.ColumnView(single_click_activate=False, reorderable=True, css_classes=["flat"])

        # ListStore -> FilterListModel -> TreeListModel -> SortListModel -> SingleSelection

        self.row_filter = Gtk.CustomFilter()
        self.row_filter.set_filter_func(self.filter)
        self.tree_model_filter = Gtk.FilterListModel(model=self.model)
        self.tree_model_filter.set_filter(self.row_filter)

        self.cv.set_show_column_separators(self.settings.get_boolean("enable-columns-separators"))
        self.cv.set_show_row_separators(self.settings.get_boolean("enable-rows-separators"))

        self.tree_model = Gtk.TreeListModel.new(self.tree_model_filter, False, True, self.model_func)
        self.tree_sorter = Gtk.TreeListRowSorter.new(self.cv.get_sorter())
        self.sorter_model = Gtk.SortListModel(model=self.tree_model, sorter=self.tree_sorter)

        self.selection_model = Gtk.SingleSelection.new(model=self.sorter_model) # sorter_model
        self.selection_model.connect("selection-changed", self.on_selection_changed)

        self.cv.set_model(self.selection_model)
        self.cv.connect("activate", self.on_column_view_activated)

        for detail in self.details_names:
            self.add_column(detail[0], detail[1], detail[2])

        self.split_view.set_sidebar(sidebar_page)
        self.split_view.set_content(content_page)

        self.navigation_select_page(self.last_page)

        column_visibility_popover_box = Gtk.Box(orientation=1)
        self.column_visibility_check_buttons = []
        for i, column in enumerate(self.cv.get_columns()):
            title = column.get_title()
            box = Gtk.Box(orientation=0)
            box.append(Gtk.Label(label=title, hexpand=True, xalign=0, margin_end=10))
            check_button = Gtk.CheckButton(active = column.get_visible())
            self.column_visibility_check_buttons.append(check_button)
            check_button.connect("toggled", self.on_check_button_toggled, column)
            box.append(check_button)
            column_visibility_popover_box.append(box)
        column_visibility_popover.set_child(column_visibility_popover_box)

        # if self.settings.get_boolean("open-last-on-start"):
        #     path = self.settings.get_string("last-inventory-path")
        #     self.read_inventory_file(path)
            #threading.Thread(target=self.read_inventory_file, args=[path]).start()

        #self.update_sidebar_item_info()

        #self.connect("activate", self.on_window_activate)

    def delete_search_text(self, entry, text):
        self.search_entry.set_text("")

    def entry_text_inserted(self, entry):
        text = entry.get_text()
        if "!" in text:
            entry.add_css_class("success")
        if not "!" in text:
            entry.remove_css_class("success")

    def filter_rows(self, btn):
        if self.search_entry.get_text() != "":
            self.row_filter.changed(Gtk.FilterChange.DIFFERENT)

    def delete_filter_rows(self, btn):
        self.search_entry.set_text("")
        self.row_filter.changed(Gtk.FilterChange.LESS_STRICT)

    def filter(self, item):
        text = self.search_entry.get_text()
        text = text.lower()
        detail_name = self.search_selector.get_active_text()
        detail_call = ""

        for index, detail in enumerate(self.details_names):
            if detail[0] == detail_name:
                detail_call = detail[1]

        item_detail = item.get_detail(detail_call)

        if text == "":
            return 1
        if item_detail == None:
            return 0

        if text in str(item_detail).lower():
            return 1

        try:
            float(text[2:])
        except:
            return 0

        if text[0] == "!":
            value = float(text[2:])
            if text[1] == ">":
                if float(item_detail) > value:
                    return 1
            if text[1] == "<":
                if float(item_detail) < value:
                    return 1
        return 0


    def on_window_activate(self, window):
        # Function to be executed when the window is activated
        print("Window activated!")
        # Call the function you want to execute here
        self.my_custom_function()

    def send_toast(self, message):
        toast = Adw.Toast()
        toast.set_title(message)
        toast.set_timeout(1)
        self.toast_overlay.add_toast(toast)

    def new_factory(self, detail):
        factory = Gtk.SignalListItemFactory()
        factory.connect("setup", self._on_factory_setup)
        factory.connect("bind", self._on_factory_bind, detail)
        factory.connect("unbind", self._on_factory_unbind, detail)
        factory.connect("teardown", self._on_factory_teardown)
        return factory

    def open_file_on_startup(self):
        if self.settings.get_boolean("open-last-on-start"):
            path = self.settings.get_string("last-inventory-path")
            self.read_inventory_file(path)


    def on_selection_changed(self, selection_model, pos, row):
        self.selected_item = selection_model.get_selection().get_maximum()
        self.update_sidebar_item_info()

    def read_inventory_file(self, file_path):
        file_extension = os.path.splitext(file_path)[1]
        self.model.remove_all()
        if file_path == "":
            return
        if file_extension != ".inve":
            return
        try:
            open(file_path, 'r').read()
        except Exception as e:
            self.send_toast("Error reading file:" + str(e))
            return 0

        with open(file_path, 'r') as file:
            file_content = file.read()
            directory, file_name = os.path.split(file_path)
            reader = csv.reader(file_content.splitlines())
            is_custom_value_row = False

            custom_info_start_index = 0

            item_detail_call_list = []

            for i, row in enumerate(reader):
                if i == 0:
                    for i, value in enumerate(row):
                        if value == "False":
                            try:
                                self.cv.get_columns()[i]
                            except:
                                pass
                            else:
                                self.cv.get_columns()[i].set_visible(False)
                                self.column_visibility_check_buttons[i].set_active(False)
                elif i == 1:
                    for i, value in enumerate(row):
                        item_detail_call_list.append(value)
                else:
                    new_item = Item(0)
                    for index, value in enumerate(row):
                        if index > len(item_detail_call_list) - 1:
                            custom_info_start_index = index
                            break
                        if value:
                            try:
                                type_info = self.details_names[index][2]
                                detail_call = item_detail_call_list[index] # self.details_names[index][1]
                                if type_info == "int":
                                    new_value = int(round(float(value)))
                                elif type_info == "cost":
                                    new_value = float(value)
                                # elif type_info == "value":
                                #     new_value = float(value)
                                #if type_info == "str" or type_info == "STR" or type_info == "date" or type_info == "DATE":
                                else:
                                    new_value = str(value)
                                new_item.set_detail(detail_call, new_value)
                                is_custom_value_row = True
                            except:
                                pass
                    if custom_info_start_index > 0:
                        for index in range(int((len(row) - custom_info_start_index)/2)):
                            new_item.append_custom_value(row[custom_info_start_index + index],row[custom_info_start_index + index + 1])

                    self.model.append(new_item)

            self.settings.set_string("last-inventory-path", file_path)
            self.title_label.set_label(file_name)
            self.subtitle_label.set_visible(True)
            self.subtitle_label.set_label("~" + directory)
            self.send_toast("File successfully opened")

    def save_inventory_file(self, file_path):
        print(file_path)
        if file_path == "":
            self.save_inventory_file_as()
            return
        try:
            open(file_path, 'w', newline='\n')
        except Exception as e:
            self.send_toast(str(e))
            return
        with open(file_path, 'w', newline='\n') as csvfile:
            writer = csv.writer(csvfile)

            column_view_row = [self.cv.get_columns()[index].get_visible() for index in range(len(self.details_names))]
            writer.writerow(column_view_row)

            column_view_row = [detail_name[1] for detail_name in self.details_names]
            writer.writerow(column_view_row)

            for item in self.model:
                item_row = [item.get_detail(self.details_names[index][1]) for index in range(len(self.details_names))]
                for custom_value in item.custom_values_list():
                    item_row.append(custom_value[0])
                    item_row.append(custom_value[1])
                writer.writerow(item_row)

        directory, file_name = os.path.split(file_path)
        self.subtitle_label.set_visible(True)
        self.subtitle_label.set_label("~" + directory)
        self.title_label.set_label(file_name)

        self.send_toast("File saved")

        print("file saved")
        self.settings.set_string("last-inventory-path", file_path)

    def on_save_file_path_selected(self, dialog, responce, dialog_parent):
        path = self.save_inventory_file(dialog_parent.get_file().get_path())
        print("the path is "+str(path))
        if responce == Gtk.ResponseType.CANCEL:
            #dialog.destroy()
            pass
        if responce == Gtk.ResponseType.ACCEPT:
            if path == None:
                self.send_toast("Invalid path")
                return
            if os.path.exists(path):
                dialog = Adw.MessageDialog(
                    heading="Replace File?",
                    body="There is already a file named this way",
                    close_response="cancel",
                    parent=self,
                    transient_for=self,
                    modal=True
                )
                dialog.set_title("Delete?")

                dialog.add_response("cancel", "Cancel")
                dialog.add_response("replace", "Replace")
                dialog.set_response_appearance("replace", Adw.ResponseAppearance.DESTRUCTIVE)

                dialog.connect("response", self.replace_file_dialog_responce, dialog_parent)
                dialog.present()
            else:
                self.save_inventory_file(path)

    def replace_file_dialog_responce(self, dialog, responce, dialog_parent):
        if responce == "cancel":
            dialog.destroy()
        if responce == "replace":
            self.save_inventory_file(dialog_parent.get_file().get_path())
            dialog.destroy()


    def save_inventory_file_as(self):
        dialog = Gtk.FileChooserNative(
            title="Save File As",
            transient_for=None,
            action=Gtk.FileChooserAction.SAVE
        )

        dialog.set_accept_label("Save")
        dialog.set_cancel_label("Cancel")

        response = dialog.show()

        dialog.connect("response", self.on_save_file_path_selected, dialog)

    def on_delete_item_button_clicked(self, btn):
        item_to_delete = self.selection_model.get_item(self.selected_item).get_item()
        for i, item in enumerate(self.model):
            if item == item_to_delete:
                item_index_to_delete = i
                break

        if self.selected_item == None:
            self.send_toast("No item is selected")
            return
        dialog = Adw.MessageDialog(
            heading="Delete Item?",
            body="This is a destructive action. The item {} with a stock of {} will be destroyed and can not be recovered.".format(item_to_delete.item_name, item_to_delete.item_quantity),
            close_response="cancel",
            transient_for=self,
            modal=True
        )
        dialog.set_title("Delete?")

        dialog.add_response("cancel", "Cancel")
        dialog.add_response("delete", "Delete")
        dialog.set_response_appearance("delete", Adw.ResponseAppearance.DESTRUCTIVE)

        dialog.connect("response", self.on_delete_item_responce, item_index_to_delete)
        dialog.present()
        #item_index = get_row_model_index_from_id(item_to_delete.item_id)

    def on_delete_item_responce(self, dialog, responce, item_index):
        if responce == "cancel":
            dialog.destroy()

        if responce == "delete":
            self.model.remove(item_index)
            self.selected_item -= 1
            if self.selected_item < 0:
                self.selected_item = 0
                if self.selected_item <= len(self.model):
                    self.selected_item = None
            dialog.destroy()

            self.update_sidebar_item_info()

            self.send_toast("The item has been deleted")

    def on_check_button_toggled(self, check, column):
        column.set_visible(check.get_active())

    def on_file_selected(self, dialog, response):
        if response == Gtk.ResponseType.ACCEPT:
            selected_file = dialog.get_file()
            if selected_file:
                file_path = selected_file.get_path()
                try:
                    open(file_path, 'r').read()
                except Exception as e:
                    self.send_toast("Error reading file:" + str(e))
                else:
                    with open(file_path, 'r') as file:
                        file_contents = file.read()
                        file_extension = os.path.splitext(file_path)[1]
                        dialog.destroy()
                        if file_extension == ".inve":
                            self.read_inventory_file(file_path)
                        else:
                            self.send_toast("File extension not supported, use import")
        else:
            dialog.destroy()

    def open_file_chooser(self, btn=None):
        dialog = Gtk.FileChooserNative(
            title="Open File",
            transient_for=None,
            action=Gtk.FileChooserAction.OPEN,
        )

        dialog.set_accept_label("Open")
        dialog.set_cancel_label("Cancel")

        response = dialog.show()

        dialog.connect("response", self.on_file_selected)

    def read_json(self):
        pass

    def read_csv(self, file_content):
        reader = csv.reader(file_content.splitlines())
        for i, row in enumerate(reader):
            if i == 0:
                for i, value in enumerate(row):
                    if value == "False":
                        self.cv.get_columns()[i].set_visible(False)
            else:
                new_item = Item(self.details_lenght)
                for index, value in enumerate(row):
                    if value:
                        try:
                            type_info = self.details_names[index][2]
                            detail_name = self.details_names[index][1]
                            if type_info == "str" or type_info == "STR":
                                new_value = str(value)
                            elif type_info == "int":
                                new_value = int(value)
                            elif type_info == "cost":
                                new_value = float(value)
                            else:
                                continue
                            new_item.assign_value(detail_name, new_value)
                        except (ValueError, TypeError):
                            pass
                self.model.append(new_item)

    def on_screen_changed(self, window):
        settings.set_int("window-width", window.get_allocated_width())
        settings.set_int("window-height", window.get_allocated_height())

    def toggle_search_bar(self, btn):
        revealed = self.search_revealer.get_reveal_child()
        self.search_revealer.set_reveal_child(not revealed)
        if self.search_revealer.get_reveal_child():
            self.search_button_toggle.set_icon_name("pan-up-symbolic")
        else:
            self.search_button_toggle.set_icon_name("pan-down-symbolic")

    def on_add_stock_to_item_button_clicked(self, btn):
        print("on_add_stock_to_item_button_clicked")
        item_index = self.selected_item
        if item_index < len(self.model):
            item = self.model[item_index]
        else:
            return

        #item = self.get_item_by_id(btn.get_name())
        #self.on_column_view_activated(self.cv, self.selected_item)

        add_item_window = Adw.Window(resizable=True)
        item_name = item.item_name
        if item_name != None:
            add_item_window.set_title("Add stock to " + item_name + " " + item.item_id)
        else:
            add_item_window.set_title("Add stock to " + item.item_id)

        add_item_window.set_default_size(600, 700)
        add_item_window.set_modal(True)
        add_item_window.set_transient_for(self)
        box = Gtk.Box(orientation=1, vexpand=True)
        box.append(Adw.HeaderBar(css_classes=["flat"]))
        list_box_add = Gtk.ListBox(selection_mode = 0, vexpand=True, margin_end=6)
        scrolled_window = Gtk.ScrolledWindow(margin_start=6, margin_top=6, margin_bottom=6, hexpand=True)
        scrolled_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled_window.set_child(list_box_add)
        box4 = Gtk.Box(spacing=6, margin_start=6, margin_end=6, css_classes=["card"])
        box4.append(scrolled_window)
        box.append(box4)

        box3 = Gtk.Box(spacing=6, margin_start=6, margin_end=6, homogeneous=True)
        cancel_button = Gtk.Button(label=_("Cancel"), hexpand=True, margin_top=6, margin_bottom=6)
        cancel_button.connect("clicked", self.quit_window, add_item_window)
        add_button = Gtk.Button(label=_("Edit"), hexpand=True, margin_top=6, margin_bottom=6, css_classes=["suggested-action"])
        add_button.connect("clicked", self.edit_existing_item, list_box_add, item, add_item_window)

        box3.append(cancel_button)
        box3.append(add_button)
        box.append(box3)

        for i in range(len(self.details_names)):
            value = item.get_detail(self.details_names[i][1])
            add_row = True
            box2 = Gtk.Box(homogeneous=True)
            box2.append(Gtk.Label(label=self.details_names[i][0], margin_start=6, xalign=0,
                        hexpand=True))
            if self.details_names[i][2] == "str":
                add_row = False
            if self.details_names[i][2] == "STR":
                box2.append(Gtk.Label(label=value, hexpand=True, margin_end=4, margin_top=4,
                        margin_bottom=4, xalign=0))
            if self.details_names[i][2] == "int":
                spin_button = Gtk.SpinButton(climb_rate=1, hexpand=True, margin_end=4, margin_top=4, margin_bottom=4)
                spin_button.set_adjustment(Gtk.Adjustment(step_increment=1, lower=0, value=0, upper=100000000))
                box2.append(spin_button)
                if value != None:
                    spin_button.set_value(float(value))
            if self.details_names[i][2] == "cost":
                add_row = False
            if self.details_names[i][2] == "DATE":
                add_row = False
            if self.details_names[i][2] == "date":
                box2.append(Gtk.Label(label=self.get_formatted_date(), hexpand=True, margin_end=4, margin_top=4,
                        margin_bottom=4, xalign=0))
            if self.details_names[i][2] == "value":
                add_row = False
            if add_row:
                list_box_add.append(box2)

        add_item_window.set_content(box)
        add_item_window.present()


    def update_sidebar_item_info(self):
        item_index = self.selected_item
        if item_index == None:
            self.item_info_revealer.set_reveal_child(False)
            return
        #self.on_column_view_activated(self.cv, item)

        if len(self.model) == 0:
            return
        if item_index > len(self.model):
            item_index = 0
        self.selected_item = item_index
        self.sidebar_item_info_list_box = Gtk.ListBox(show_separators=True, selection_mode=0,
                margin_start=6, margin_end=6, vexpand=True, width_request=300)
        box1 = Gtk.Box(orientation=1, css_classes=["card"],
                margin_start=6, margin_end=6, margin_top=6, margin_bottom=6)


        sidebar_scrolled_window_item_info = Gtk.ScrolledWindow(vexpand=True)
        sidebar_scrolled_window_item_info.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        sidebar_scrolled_window_item_info.set_child(self.sidebar_item_info_list_box)
        box5 = Gtk.Box(orientation=1)

        infoCarousel = Adw.Carousel(allow_scroll_wheel=False)
        infoCarousel.append(box5)
        carouselIndicator = Adw.CarouselIndicatorLines(carousel=infoCarousel, margin_top=4)
        box1.append(carouselIndicator)

        #box5.append(carouselIndicator)
        box5.append(Gtk.Label(label="General Info", margin_top=2, margin_bottom=6, css_classes=["title-4"]))
        box5.append(Gtk.Separator())
        box5.append(sidebar_scrolled_window_item_info)


        self.sidebar_item_custom_values_list_box = Gtk.ListBox(show_separators=True, selection_mode=0,
                margin_start=6, margin_end=6, vexpand=True, width_request=300)
        sidebar_scrolled_window_item_custom = Gtk.ScrolledWindow(vexpand=True)
        sidebar_scrolled_window_item_custom.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        sidebar_scrolled_window_item_custom.set_child(self.sidebar_item_custom_values_list_box)
        box5 = Gtk.Box(orientation=1)
        box5.append(Gtk.Label(label="Custom Info", margin_top=2, margin_bottom=6, css_classes=["title-4"]))
        box5.append(Gtk.Separator())
        box5.append(sidebar_scrolled_window_item_custom)

        infoCarousel.append(box5)

        box1.append(infoCarousel)


        item_id=self.model[item_index].item_id

        add_this_button = Gtk.Button(hexpand=True, label="Add", css_classes=["success"])
        remove_this_button = Gtk.Button(hexpand=True, label="-1", css_classes=["error"])
        edit_button = Gtk.Button(icon_name="document-edit-symbolic", hexpand=True)

        box2 = Gtk.Box(homogeneous=True, margin_start=6, margin_end=6, margin_top=6, margin_bottom=6, hexpand=True, spacing=6)
        box2.append(edit_button)
        box2.append(add_this_button)
        box2.append(remove_this_button)

        edit_button.connect("clicked", self.show_edit_item_dialog)
        add_this_button.connect("clicked", self.on_add_stock_to_item_button_clicked)
        remove_this_button.connect("clicked", self.on_remove_one_item_button_clicked)

        box1.append(box2)

        self.item_info_revealer.set_child(box1)

        self.item_info_revealer.set_reveal_child(True)

        item = self.selection_model.get_item(item_index).get_item()

        for info in item.custom_values_list():
            box6 = Gtk.Box()
            box6.append(Gtk.Label(label=info[0], xalign=0, hexpand=True, margin_end=6, margin_start=6, margin_top=3, margin_bottom=3))
            box6.append(Gtk.Label(label=info[1], xalign=1, hexpand=True, halign=Gtk.Align.FILL, margin_end=6))
            self.sidebar_item_custom_values_list_box.append(box6)

        for i in range(len(self.details_names)):
            box = Gtk.FlowBox(margin_start=6, margin_end=6, max_children_per_line=2,
                    selection_mode=Gtk.SelectionMode.NONE)
            name = self.details_names[i][0] + ":"
            box.append(Gtk.Label(ellipsize=2, label=name, xalign=0, hexpand=True, margin_end=6))

            item.get_detail(self.details_names[i][1])

            detail_type = self.details_names[i][2]
            value = item.get_detail(self.details_names[i][1])
            if detail_type == "cost":
                if value != None:
                    text = round(float(value), 2)
            else:
                text = value
            if text == "" or text == None:
                text = "..."
            box.append(Gtk.Label(label=text, xalign=1, hexpand=True, halign=Gtk.Align.FILL))
            self.sidebar_item_info_list_box.append(box)

    def on_column_view_activated(self, cv, row_index):
        print("activated")
        print(row_index)
        self.show_edit_item_dialog()
        self.selected_item = row_index
        self.update_sidebar_item_info()

    def show_edit_item_dialog(self, btn=None):
        print("show_edit_item_dialog")
        item_index = self.selected_item
        if item_index < len(self.model):
            item = item = self.selection_model.get_item(self.selected_item).get_item()
        else:
            return

        add_item_window = Adw.Window(resizable=True)
        item_name = item.item_name
        if item_name != None:
            add_item_window.set_title("Edit " + item_name + " " + item.item_id)
        else:
            add_item_window.set_title("Edit " + item.item_id)
        add_item_window.set_default_size(600, 700)
        add_item_window.set_modal(True)
        add_item_window.set_transient_for(self)
        box = Gtk.Box(orientation=1, vexpand=True)
        box.append(Adw.HeaderBar(css_classes=["flat"]))
        list_box_add = Gtk.ListBox(selection_mode = 0, vexpand=True, margin_end=6)
        scrolled_window = Gtk.ScrolledWindow(margin_start=6, margin_top=6, margin_bottom=6, hexpand=True)
        scrolled_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled_window.set_child(list_box_add)
        box4 = Gtk.Box(spacing=6, margin_start=6, margin_end=6, css_classes=["card"])
        box4.append(scrolled_window)
        box.append(box4)

        box3 = Gtk.Box(spacing=6, margin_start=6, margin_end=6, homogeneous=True)
        cancel_button = Gtk.Button(label=_("Cancel"), hexpand=True, margin_top=6, margin_bottom=6)
        cancel_button.connect("clicked", self.quit_window, add_item_window)
        add_button = Gtk.Button(label=_("Edit"), hexpand=True, margin_top=6, margin_bottom=6, css_classes=["suggested-action"])
        add_button.connect("clicked", self.edit_existing_item, list_box_add, item, add_item_window)
        box3.append(cancel_button)
        box3.append(add_button)
        box.append(box3)

        for i in range(len(self.details_names)):
            box2 = Gtk.Box(homogeneous=True)
            list_box_add.append(box2)
            box2.append(Gtk.Label(label=self.details_names[i][0], xalign=0, hexpand=True))
            value = item.get_detail(self.details_names[i][1])
            if self.details_names[i][2] == "STR":
                box2.append(Gtk.Label(label=value, hexpand=True, margin_top=4,
                        margin_bottom=4, xalign=0))
            elif self.details_names[i][2] == "int":
                spin_button = Gtk.SpinButton(climb_rate=1, hexpand=True, margin_top=4, margin_bottom=4)
                spin_button.set_adjustment(Gtk.Adjustment(step_increment=1, lower=0, value=0, upper=100000000))
                box2.append(spin_button)
                if value != None:
                    spin_button.set_value(float(value))
            elif self.details_names[i][2] == "cost":
                spin_button = Gtk.SpinButton(climb_rate=1, digits=2, hexpand=True, margin_top=4, margin_bottom=4)
                spin_button.set_adjustment(Gtk.Adjustment(step_increment=0.01, lower=0, value=0, upper=100000000))
                box2.append(spin_button)
                if value != None:
                    spin_button.set_value(float(value))
            elif self.details_names[i][2] == "DATE":
                box2.append(Gtk.Label(label=value, hexpand=True, margin_top=4, margin_bottom=4, xalign=0))
            elif self.details_names[i][2] == "date":
                box2.append(Gtk.Label(label=self.get_formatted_date(), hexpand=True, margin_top=4, margin_bottom=4, xalign=0))
            elif self.details_names[i][2] == "cat":
                category_drop_down = Gtk.ComboBoxText(margin_top=4, margin_bottom=4,margin_end=4)
                for category in self.categories:
                    category_drop_down.append_text(category)
                box2.append(category_drop_down)
                category_drop_down.set_active(self.find_index(self.categories, value))

            elif self.details_names[i][2] == "value":
                spin_button = Gtk.SpinButton(climb_rate=1, digits=2, hexpand=True, margin_top=4, margin_bottom=4)
                spin_button.set_width_chars(6)
                spin_button.set_adjustment(Gtk.Adjustment(step_increment=0.1, lower=0, value=0, upper=100000000))
                number, unit = self.split_string_with_unit(value)
                if number != None:
                    try:
                        float(number)
                    except:
                        spin_button.set_value(0)
                    else:
                        spin_button.set_value(float(number))
                drop_down = Gtk.DropDown.new_from_strings(self.units_of_measure)
                drop_down.set_size_request(100, 0)
                drop_down.set_enable_search(True)
                drop_down.set_margin_start(6)
                drop_down.set_margin_end(4)
                drop_down.set_margin_top(4)
                drop_down.set_selected(self.find_index(self.units_of_measure, unit))
                box4 = Gtk.Box()
                box4.append(spin_button)
                box4.append(drop_down)
                box2.append(box4)
            else:
                entry = Gtk.Entry(placeholder_text=_("Write here"),hexpand=True, margin_top=4, margin_bottom=4)
                box2.append(entry)
                if value != None:
                    entry.set_text(str(value))
        add_item_window.set_content(box)
        add_item_window.present()

    def find_index(self, arr, value):
        try:
            index = arr.index(value)
            return index
        except ValueError:
            return 0

    def split_string_with_unit(self, input_string):
        if input_string == None:
            return input_string, "  "
        index_of_space = str(input_string).find(" ")
        if index_of_space != -1:
            first_part = input_string[:index_of_space]
            second_part = input_string[index_of_space + 1:]
            print(second_part)
            return float(first_part), second_part
        return float(input_string), "  "

    def edit_existing_item(self, btn, list_box, item, window):
        print("edit_existing_item")
        for i in range(len(self.details_names)):
            detail_name = self.details_names[i][1]
            value_widget = list_box.get_row_at_index(i).get_child().get_first_child().get_next_sibling()

            if self.details_names[i][2] == "STR":
                value = value_widget.get_label()
            elif self.details_names[i][2] == "int":
                value = int(value_widget.get_value())
            elif self.details_names[i][2] == "cost":
                value = float(value_widget.get_value())
            elif self.details_names[i][2] == "value":
                value = str(round(float(value_widget.get_first_child().get_value()), 2))
                unit_index = value_widget.get_first_child().get_next_sibling().get_selected()
                value += " " + str(self.units_of_measure[unit_index])
            elif self.details_names[i][2] == "cat":
                value = value_widget.get_active_text()
            else:
                value = value_widget.get_text()

            if value == 0 or value == "0" or value == "0.0":
                value = None

            item.set_detail(detail_name, value)
            self.update_sidebar_item_info()
        self.send_toast(_("Item successfully edited"))

        window.destroy()

    def on_remove_one_item_button_clicked(self, btn):
        #item = self.get_item_by_id(btn.get_name())
        #item.set_value_at_index() -= 1
        #item.details_all[10] = self.get_formatted_date()
        #self.on_column_view_activated(self.cv, self.selected_item)
        pass

    def get_item_by_id(self, item_id):
        for item in self.model:
            if item.item_id == item_id:
                return item

    def get_row_model_index_from_id(self, item_id):
        for item, i in enumerate(self.model):
            if item.item_id == item_id:
                return i

    def on_item_row_activated(self, list_box, exc):
        item_row_name = list_box.get_selected_row().get_child().get_name()
        index = self.get_index_from_id(item_row_name)

    def model_func(self, args):
        #print(args)
        pass

    def add_column(self, column_name, detail_call, detail_type):
        factory = Gtk.SignalListItemFactory()
        factory.connect("setup", self._on_factory_setup)
        factory.connect("bind", self._on_factory_bind, detail_call)
        factory.connect("unbind", self._on_factory_unbind, detail_call)
        factory.connect("teardown", self._on_factory_teardown)

        col = Gtk.ColumnViewColumn(title=column_name, factory=factory, resizable=True)
        sorter = Gtk.CustomSorter.new(self.sort_func, user_data=[detail_call, detail_type])
        sorter.connect("changed", self.scroll_to_the_top)
        col.set_sorter(sorter)
        col.props.expand = True
        self.cv.append_column(col)

    def scroll_to_the_top(self, change, data):
        self.content_scrolled_window.get_vadjustment().set_value(0)
        print(0)

    def sort_func(self, obj_1, obj_2, detail_call_and_type):
        detail_call = detail_call_and_type[0]
        detail_type = detail_call_and_type[1]
        obj_1_detail = obj_1.get_detail(detail_call)
        obj_2_detail = obj_2.get_detail(detail_call)

        if detail_type in ["int", "cost", "value"]:
            if detail_type == "value":
                obj_1_detail, unit = self.split_string_with_unit(obj_1_detail)
                obj_2_detail, unit = self.split_string_with_unit(obj_2_detail)
            if obj_1_detail == None:
                obj_1_detail = 0
            if obj_2_detail == None:
                obj_2_detail = 0
            if float(obj_1_detail) < float(obj_2_detail):
                return -1
            elif float(obj_1_detail) == float(obj_2_detail):
                return 0
            return 1

        else:
            if str(obj_1_detail) < str(obj_2_detail):
                return -1
            elif str(obj_1_detail) == str(obj_2_detail):
                return 0
            return 1

    def show_items(self):
        self.search_button_toggle.set_visible(True)
        self.search_revealer.set_reveal_child(self.search_button_toggle.get_active())

        self.content_scrolled_window.set_child(self.cv)
        if self.settings.get_boolean("enable-horizontal-scrolling"):
            self.content_scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.action_bar_revealer.set_reveal_child(True)
        #if self.model != None:
        self.selected_item = 0
        self.update_sidebar_item_info()
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

    def add_new_item_dialog(self, args):
        add_item_window = Adw.Window(resizable=True)
        add_item_window.set_title("Add item")

        add_item_window.set_default_size(600, 700)
        add_item_window.set_modal(True)
        add_item_window.set_transient_for(self)
        box = Gtk.Box(orientation=1, vexpand=True)
        box.append(Adw.HeaderBar(css_classes=["flat"]))
        list_box_add = Gtk.ListBox(selection_mode = 0, vexpand=True, margin_end=6)
        scrolled_window = Gtk.ScrolledWindow(margin_start=6, margin_top=6, margin_bottom=6, hexpand=True)
        scrolled_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        box6 = Gtk.Box(orientation=1)
        box6.append(list_box_add)
        scrolled_window.set_child(box6)
        box4 = Gtk.Box(spacing=6, margin_start=6, margin_end=6, css_classes=["card"])
        box4.append(scrolled_window)
        box.append(box4)

        box3 = Gtk.Box(spacing=6, margin_start=6, margin_end=6, homogeneous=True)
        cancel_button = Gtk.Button(label=_("Cancel"), hexpand=True, margin_top=6, margin_bottom=6)
        cancel_button.connect("clicked", self.quit_window, add_item_window)
        add_button = Gtk.Button(label=_("Add"), hexpand=True, margin_top=6, margin_bottom=6, css_classes=["suggested-action"])

        box3.append(cancel_button)
        box3.append(add_button)
        box.append(box3)

        for i in range(len(self.details_names)):
            box2 = Gtk.Box(homogeneous=True)
            list_box_add.append(box2)
            box2.append(Gtk.Label(label=self.details_names[i][0], margin_start=6, xalign=0,
                    hexpand=True))
            if self.details_names[i][2] == "str":
                box2.append(Gtk.Entry(placeholder_text=_("Write here"),hexpand=True, margin_end=4, margin_top=4,
                        margin_bottom=4))
            if self.details_names[i][2] == "STR":
                box2.append(Gtk.Label(label=self.generate_new_id(), hexpand=True, margin_end=4, margin_top=4,
                        margin_bottom=4, xalign=0))
            if self.details_names[i][2] == "int":
                spin_button = Gtk.SpinButton(climb_rate=1, hexpand=True, margin_end=4, margin_top=4, margin_bottom=4)
                spin_button.set_adjustment(Gtk.Adjustment(step_increment=1, lower=0, value=0, upper=100000000))
                box2.append(spin_button)
            if self.details_names[i][2] == "cost":
                spin_button = Gtk.SpinButton(climb_rate=1, digits=2, hexpand=True, margin_end=4, margin_top=4, margin_bottom=4)
                spin_button.set_adjustment(Gtk.Adjustment(step_increment=0.01, lower=0, value=0, upper=100000000))
                box2.append(spin_button)
            if self.details_names[i][2] == "DATE":
                box2.append(Gtk.Label(label=self.get_formatted_date(), hexpand=True, margin_end=4, margin_top=4,
                        margin_bottom=4, xalign=0))
            if self.details_names[i][2] == "date":
                box2.append(Gtk.Label(label=self.get_formatted_date(), hexpand=True, margin_end=4, margin_top=4,
                        margin_bottom=4, xalign=0))
            if self.details_names[i][2] == "value":
                spin_button = Gtk.SpinButton(climb_rate=1, digits=2, hexpand=True, margin_end=4, margin_top=4, margin_bottom=4)
                spin_button.set_adjustment(Gtk.Adjustment(step_increment=0.01, lower=0, value=0, upper=100000000))

                drop_down = Gtk.DropDown.new_from_strings(self.units_of_measure)
                drop_down.set_size_request(100, 0)
                drop_down.set_enable_search(True)
                drop_down.set_margin_start(6)
                drop_down.set_margin_bottom(4)
                drop_down.set_margin_end(4)
                drop_down.set_margin_top(4)
                drop_down.set_selected(0)

                box4 = Gtk.Box()
                box4.append(spin_button)
                box4.append(drop_down)
                box2.append(box4)
            if self.details_names[i][2] == "cat":
                category_drop_down = Gtk.ComboBoxText(margin_top=4, margin_bottom=4,margin_end=4)
                for category in self.categories:
                    category_drop_down.append_text(category)
                box2.append(category_drop_down)

        box6.append(Gtk.Separator())
        custom_info_box = Gtk.Box(orientation=1)
        box6.append(custom_info_box)

        box7 = Gtk.Box(hexpand=True)
        label = Gtk.Label(label="Add Custom Info", hexpand=True, margin_top=6, margin_bottom=6, css_classes=["title-3"])
        add_custom_info_button = Gtk.Button(icon_name="list-add-symbolic", margin_start=6, margin_top=6, margin_bottom=6,margin_end=12)

        box7.append(label)
        box7.append(add_custom_info_button)

        custom_info_box.append(box7)
        #custom_info_box.append()
        custom_info_list_box = Gtk.ListBox(selection_mode = 0, vexpand=True, margin_end=6)
        add_custom_info_button.connect("clicked", self.add_custom_info_to_listbox, custom_info_list_box)

        custom_info_box.append(custom_info_list_box)

        add_button.connect("clicked", self.add_item_to_list, list_box_add, add_item_window, custom_info_list_box)

        add_item_window.set_content(box)
        add_item_window.present()

    def add_custom_info_to_listbox(self, btn, list_box):
        row_index = 0

        box2 = Gtk.Box(margin_end=4, margin_start=6, margin_top=4, margin_bottom=4, spacing=6)
        list_box.append(box2)
        name = "Custom info"
        box2.append(Gtk.Entry(placeholder_text=_("Name"),hexpand=True))
        box2.append(Gtk.Entry(placeholder_text=_("Value"),hexpand=True))
        delete_button = Gtk.Button(icon_name="user-trash-symbolic")
        delete_button.connect("clicked", self.delete_custom_item_row, list_box)
        box2.append(delete_button)

    def delete_custom_item_row(self, btn, list_box):
        list_box.remove(btn.get_parent().get_parent())

    def get_formatted_date(self):
        today = datetime.date.today()
        formatted_date = today.strftime("%Y.%m.%d")
        return formatted_date

    def add_item_to_list(self, btn, list_box_add, window, custom_info_list_box):
        new_item = Item(self.details_lenght)
        for i in range(len(self.details_names)):
            value_widget = list_box_add.get_row_at_index(i).get_child().get_first_child().get_next_sibling()
            detail_type = self.details_names[i][2]
            detail_name = self.details_names[i][1]
            value = None
            if detail_type == "str" or detail_type == "DATE" or detail_type == "date":
                value = value_widget.get_text()
            if detail_type == "STR":
                value = value_widget.get_label()
            if detail_type == "int" or detail_type == "cost":
                value = value_widget.get_value()
            if detail_type == "cat":
                value = value_widget.get_active_text()
            if detail_type == "value":
                value = str(round(float(value_widget.get_first_child().get_value()), 2))
                unit_index = value_widget.get_first_child().get_next_sibling().get_selected()
                value += " " + str(self.units_of_measure[unit_index])
            new_item.set_detail(detail_name, value)

        custom_infos = 0
        while custom_info_list_box.get_row_at_index(custom_infos) != None:
            name = custom_info_list_box.get_row_at_index(custom_infos).get_child().get_first_child().get_text()
            value = custom_info_list_box.get_row_at_index(custom_infos).get_child().get_first_child().get_next_sibling().get_text()
            if name != "" and value != "":
                new_item.append_custom_value(name, value)
            custom_infos += 1

        # value = list_box.get_row_at_index(index).get_child().get_first_child().get_next_sibling().get_text()
        # name = list_box.get_row_at_index(index).get_child().get_first_child().get_text()

        self.model.append(new_item)
        self.selected_item = len(self.model) - 1
        self.update_sidebar_item_info()
        window.destroy()

    def generate_new_id(self):
        chars = ["0","1","3","3","4","5","6","7","8","9","A","B","C","D","E","F","G","H","I","L","M","N","O","P","Q","R","S","T","U","V","Z","J","K"]
        new_id = ""
        for i in range(self.id_lenght):
            new_id = new_id + random.choice(chars)
        for i in range(len(self.model)):
            if new_id == self.model[i].item_id:
                new_id == self.generate_new_id()
        return new_id

    def toggle_sidebar(self, btn):
        self.split_view.set_collapsed(self.split_view.get_collapsed)

    def on_navigation_row_activated(self, list_box, exc):
        selected_row = list_box.get_selected_row()

        self.split_view.set_collapsed(False)
        self.navigation_select_page(selected_row.get_index())



    def show_products(self):
        print("show products")
        self.item_info_revealer.set_reveal_child(False)
        self.action_bar_revealer.set_reveal_child(False)
        self.products_box = Gtk.Box(margin_start=10, margin_top=10, margin_bottom=10, margin_end=10)
        self.content_scrolled_window.set_child(self.products_box)

        products_status_page = Adw.StatusPage(title="Work in progress",
                icon_name="package-x-generic-symbolic", hexpand=True, vexpand=True,
                description="Products are still not supported")
        self.products_box.append(products_status_page)

    def show_invoice(self):
        print("show invoices")
        self.item_info_revealer.set_reveal_child(False)
        self.action_bar_revealer.set_reveal_child(False)
        self.invoices_box = Gtk.Box(margin_start=10, margin_top=10, margin_bottom=10, margin_end=10)
        self.content_scrolled_window.set_child(self.invoices_box)

        invoice_status_page = Adw.StatusPage(title="Work in progress",
                icon_name="accessories-text-editor-symbolic", hexpand=True, vexpand=True,
                description="Invoices are still not supported")
        self.invoices_box.append(invoice_status_page)

    def navigation_select_page(self, index):
        selected_row = self.sidebar_navigation_listBox.get_row_at_index(index)
        self.sidebar_navigation_listBox.select_row(selected_row)

        self.last_page = index

        if selected_row.get_child().get_label() == "Dashboard":
            self.show_dashboard()
        elif selected_row.get_child().get_label() == "Items":
            self.show_items()
        elif selected_row.get_child().get_label() == "Products":
            self.show_products()
        elif selected_row.get_child().get_label() == "Invoice":
            self.show_invoice()

    def show_dashboard(self):
        self.search_button_toggle.set_visible(False)
        self.search_revealer.set_reveal_child(False)
        self.content_scrolled_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.NEVER)
        self.content_scrolled_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.item_info_revealer.set_reveal_child(False)
        self.action_bar_revealer.set_reveal_child(False)
        self.dashboard_box = Gtk.Grid(row_homogeneous=True, column_homogeneous=True,
                row_spacing=10, column_spacing=10, margin_start=10, margin_top=10, margin_bottom=10, margin_end=10)
        self.content_scrolled_window.set_child(self.dashboard_box)

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
            cost = self.model[i].item_cost
            stock = self.model[i].item_quantity
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
            
