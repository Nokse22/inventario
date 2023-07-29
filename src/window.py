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
import string
import webbrowser

class Part(GObject.Object):
    __gtype_name__ = "Part"

    def __init__(self):
        super().__init__()

        self._part_id = None
        self._part_category = None
        self._part_name = None
        self._part_stock = None
        self._part_package = None
        self._part_cost = None
        self._part_value = None
        self._part_manufacturer = None
        self._part_description = None
        self._part_seller = None
        self._part_stock_reserved = None
        self._part_stock_allocated = None
        self._part_stock_planned = None
        self._part_stock_on_order = None
        self._part_stock_for_sale = None
        self._part_storage = None
        self._part_part_number = None
        self._used_quantity = None
        self._part_datasheet = None

    @GObject.Property(type=str)
    def part_datasheet(self):
        return self._part_datasheet

    @GObject.Property(type=str)
    def used_quantity(self):
        return self._used_quantity

    @GObject.Property(type=str)
    def part_stock_on_order(self):
        return self._part_stock_on_order

    @GObject.Property(type=str)
    def part_id(self):
        return self._part_id

    @GObject.Property(type=str)
    def part_manufacturer(self):
        return self._part_manufacturer

    @GObject.Property(type=str)
    def part_seller(self):
        return self._part_seller

    @GObject.Property(type=str)
    def part_category(self):
        return self._part_category

    @GObject.Property(type=str)
    def part_name(self):
        return self._part_name

    @GObject.Property(type=int)
    def part_stock(self):
        #return self._part_quantity + self._part_stock_reserved + self._part_stock_allocated + self._part_stock_planned + self._part_stock_on_order + self._part_stock_for_sale
        return self._part_stock

    @GObject.Property(type=str)
    def part_package(self):
        return self._part_package

    @GObject.Property(type=str)
    def part_cost(self):
        return self._part_cost

    @GObject.Property(type=str)
    def part_description(self):
        return self._part_description

    @GObject.Property(type=int)
    def part_stock_reserved(self):
        return self._part_stock_reserved

    @GObject.Property(type=int)
    def part_stock_allocated(self):
        return self._part_stock_allocated

    @GObject.Property(type=int)
    def part_stock_planned(self):
        return self._part_stock_planned

    @GObject.Property(type=int)
    def part_stock_in_partion(self):
        return self._part_stock_on_order

    @GObject.Property(type=int)
    def part_stock_for_sale(self):
        return self._part_stock_for_sale

    @GObject.Property(type=str)
    def part_storage(self):
        return self._part_storage

    @GObject.Property(type=str)
    def part_part_number(self):
        return self._part_part_number

    def set_parts_index(self, index, value):
        self._part_parts_list[index] = value

    def append_part(self, part_id, quantity):
        self._part_parts_list.append([part_id, quantity])

    def get_detail(self, name):
        return getattr(self, name, None)

    def set_detail(self, detail_name, value):
        attributes = inspect.getmembers(self, lambda a: not inspect.isroutine(a))
        for attr_name, _ in attributes:
            if attr_name == f"_{detail_name}":
                setattr(self, f"_{detail_name}", value)
                return

        raise ValueError(f"Invalid detail name: {detail_name}")

    def __repr__(self):
        text = "Part: "
        return text + (self.part_id or "") + " " + (self.part_name or "no name") + " " + (self.part_description or "")

class Product(GObject.Object):
    __gtype_name__ = "Product"

    def __init__(self):
        super().__init__()

        self._product_id = None
        self._product_category = None
        self._product_name = None
        self._product_stock = None
        self._product_package = None
        self._product_cost = None
        self._product_value = None
        self._product_manufacturer = None
        self._product_description = None
        self._product_creation = None
        self._product_modification = None
        self._product_seller = None
        self._product_selling_price = None
        self._product_stock_reserved = None
        self._product_stock_allocated = None
        self._product_stock_planned = None
        self._product_stock_on_order = None
        self._product_stock_for_sale = None
        self._product_storage = None
        self._product_part_number = None
        self._product_revision = None

        self._product_parts_list = Gio.ListStore(item_type=Part)

    @GObject.Property(type=str)
    def product_revision(self):
        return self._product_revision

    @GObject.Property(type=str)
    def product_stock_on_order(self):
        return self._product_stock_on_order

    @GObject.Property(type=str)
    def product_parts_list(self):
        return self._product_parts_list

    @GObject.Property(type=str)
    def product_id(self):
        return self._product_id

    @GObject.Property(type=str)
    def product_manufacturer(self):
        return self._product_manufacturer

    @GObject.Property(type=str)
    def product_seller(self):
        return self._product_seller

    @GObject.Property(type=str)
    def product_category(self):
        return self._product_category

    @GObject.Property(type=str)
    def product_name(self):
        return self._product_name

    @GObject.Property(type=int)
    def product_stock(self):
        #return self._product_quantity + self._product_stock_reserved + self._product_stock_allocated + self._product_stock_planned + self._product_stock_on_order + self._product_stock_for_sale
        return self._product_stock

    @GObject.Property(type=str)
    def product_package(self):
        return self._product_package

    @GObject.Property(type=str)
    def product_cost(self):
        return self._product_cost

    @GObject.Property(type=str)
    def product_description(self):
        return self._product_description

    @GObject.Property(type=str)
    def product_creation(self):
        return self._product_creation

    @GObject.Property(type=str)
    def product_modification(self):
        return self._product_modification

    @GObject.Property(type=str)
    def product_selling_price(self):
        return self._product_selling_price

    @GObject.Property(type=int)
    def product_stock_reserved(self):
        return self._product_stock_reserved

    @GObject.Property(type=int)
    def product_stock_allocated(self):
        return self._product_stock_allocated

    @GObject.Property(type=int)
    def product_stock_planned(self):
        return self._product_stock_planned

    @GObject.Property(type=int)
    def product_stock_in_production(self):
        return self._product_stock_on_order

    @GObject.Property(type=int)
    def product_stock_for_sale(self):
        return self._product_stock_for_sale

    @GObject.Property(type=str)
    def product_storage(self):
        return self._product_storage

    @GObject.Property(type=str)
    def product_part_number(self):
        return self._product_part_number


    def parts_list(self):
        return self._product_parts_list

    def append_part(self, part):
        self._product_parts_list.append(part)

    def get_detail(self, name):
        return getattr(self, name, None)

    def set_detail(self, detail_name, value):
        attributes = inspect.getmembers(self, lambda a: not inspect.isroutine(a))

        for attr_name, _ in attributes:
            if attr_name == f"_{detail_name}":
                setattr(self, f"_{detail_name}", value)
                return

        raise ValueError(f"Invalid detail name: {detail_name}")

    def __repr__(self):
        text = "Product: "
        return text + self.product_id


class Item(GObject.Object):
    __gtype_name__ = "Item"

    def __init__(self, length):
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
        self._item_low_stock = None
        self._item_buy_link = None
        self._item_datasheet = None
        self._item_custom_values_list = []

    @GObject.Property(type=str)
    def item_datasheet(self):
        return self._item_datasheet

    @GObject.Property(type=str)
    def item_buy_link(self):
        return self._item_buy_link

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

    @GObject.Property(type=str)
    def item_low_stock(self):
        return self._item_low_stock

    def custom_values_list(self):
        return self._item_custom_values_list

    def set_custom_values_at_index(self, index, value):
        self._item_custom_values_list[index] = value

    def append_custom_value(self, name, value):
        self._item_custom_values_list.append([name, value])

    def get_detail(self, name):
        return getattr(self, name, None)

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

    sidebar_options = ["Dashboard", "Items", "Products", "Low Stock", "Out Of Stock", "Production", "Invoice", ]

    dashboard_index = 0
    items_index = 1
    products_index = 2
    invoices_index = 6
    low_stock_index = 3
    out_of_stock_index = 4
    production_index = 5

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

    part_item_product_translation = [
        ["part_id", "item_id", "product_id", "ID"],
        ["part_category", "item_category", "product_category", "Category"],
        ["part_name", "item_name", "product_name", "Name"],
        ["part_description", "item_description", "product_description", "Description"],
        ["part_package", "item_package", "product_package", "Package"],
        ["part_part_number", "item_part_number", "product_part_number", "Part Number"],
        ["part_cost", "item_cost", "product_cost", "Cost"],
        ["part_manufacturer", "item_manufacturer", "product_manufacturer", "Manufaturer"],
        ["part_seller", "item_seller", "product_seller", "Seller"],
        ["part_storage", "item_storage", "product_storage", "Storage"],
        ["part_stock_reserved", "item_stock_reserved", "product_stock_reserved", "Stock Reserved"],
        ["part_stock_allocated", "item_stock_allocated", "product_stock_allocated", "Stock Allocated"],
        ["part_stock_planned", "item_stock_planned", "product_stock_planned", "Stock Planned"],
        ["part_stock_on_order", "item_stock_on_order", "product_stock_on_order", "Stock on Order"],
        ["part_stock_for_sale", "item_stock_for_sale", "product_stock_for_sale", "Stock for Sale"],
        ["part_datasheet", "item_datasheet", "product_datasheet", "Datasheet"]
    ]

    details_names = [
                    ["ID", "item_id", "STR"],
                    ["Category","item_category", "cat"],
                    ["Name","item_name", "str"],
                    ["Description", "item_description", "str"],
                    ["Stock", "item_quantity", "int"],
                    ["Low Stock", "item_low_stock", "int"],
                    ["Package", "item_package", "str"],
                    ["Part Number","item_part_number", "str"],
                    ["Price", "item_cost", "cost"],
                    ["Value", "item_value", "value"],
                    ["Manufacturer", "item_manufacturer", "str"],
                    ["Seller", "item_seller", "str"],
                    ["Storage location", "item_storage", "str"],
                    ["Selling Price", "item_selling_price", "cost"],
                    ["Stock Reserved", "item_stock_reserved", "int"],
                    ["Stock Allocated", "item_stock_allocated", "int"],
                    ["Stock Planned", "item_stock_planned", "int"],
                    ["Stock on Order", "item_stock_on_order", "int"],
                    ["Stock for Sale", "item_stock_for_sale", "int"],
                    ["Buy Link", "item_buy_link", "str"],
                    ["Data-sheet", "item_datasheet", "str"],
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
                   "MV", "kV", "V", "mV", "μV", "nV",
                   "inches", "feet",
                   "°"]

    items_categories = ["ELECTRONICS", "MECHANICAL", "CONSUMABLE"]
    products_categories = ["ELECTRONICS", "MECHANICAL"]

    product_details_names = [
                    ["ID", "product_id", "STR"],
                    ["Category","product_category", "cat"],
                    ["Name","product_name", "str"],
                    ["Stock", "product_stock", "int"],
                    ["Package", "product_package", "str"],
                    ["Part Number","product_part_number", "str"],
                    ["Revision","product_revision", "str"],
                    ["Price", "product_cost", "cost"],
                    ["Manufacturer", "product_manufacturer", "str"],
                    ["Seller", "product_seller", "str"],
                    ["Storage location", "product_storage", "str"],
                    ["Description", "product_description", "str"],
                    ["Selling Price", "product_selling_price", "cost"],
                    ["Stock Reserved", "product_stock_reserved", "int"],
                    ["Stock Allocated", "product_stock_allocated", "int"],
                    ["Stock Planned", "product_stock_planned", "int"],
                    ["Stock on Order", "product_stock_on_order", "int"],
                    ["Stock for Sale", "product_stock_for_sale", "int"],
                    ["Created on", "product_creation", "DATE"],
                    ["Modified on", "product_modification", "date"],
                    ]

    details_lenght = len(details_names)

    id_lenght = 5

    dashboard_width = 4
    dashboard_height = 10

    filter_parameters = []

    selected_item = 0
    selected_product = 0
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

        #self.split_view = Adw.NavigationSplitView()
        #self.set_content(self.split_view)

        # Create outer AdwNavigationSplitView
        self.split_view = Adw.NavigationSplitView()
        self.split_view.set_min_sidebar_width(470)
        self.split_view.set_max_sidebar_width(1400)
        self.split_view.set_sidebar_width_fraction(0.7)

        self.set_content(self.split_view)

        # Create inner AdwNavigationSplitView
        inner_view = Adw.NavigationSplitView()
        inner_view.set_max_sidebar_width(260)
        inner_view.set_sidebar_width_fraction(0.38)

        sidebar_page = Adw.NavigationPage()
        content_page = Adw.NavigationPage()

        self.sidebar_split_view = Adw.NavigationSplitView()
        self.sidebar_split_view.set_max_sidebar_width(200)
        self.sidebar_split_view.set_sidebar_width_fraction(0.6)
        self.sidebar_split_view.set_sidebar(sidebar_page)
        self.sidebar_split_view.set_content(content_page)

        self.sidebar_page_split_view = Adw.NavigationPage()
        self.sidebar_page_split_view.set_child(self.sidebar_split_view)
        self.split_view.set_sidebar(self.sidebar_page_split_view)
        self.right_pane = Adw.NavigationPage()
        self.split_view.set_content(self.right_pane)


        right_pane_box = Gtk.Box(orientation=1)
        self.right_pane.set_child(right_pane_box)
        right_pane_box.append(Adw.HeaderBar(css_classes=["flat"], hexpand=True))
        self.right_pane_content_box = Gtk.Box(vexpand=True,hexpand=True)
        right_pane_box.append(self.right_pane_content_box)
        #self.right_pane_content_box.append(Gtk.Label(label="item info", css_classes=["title-1"], vexpand=True, hexpand=True))

        # Sidebar
        sidebar_page.set_title("")
        sidebar_page.set_tag("sidebar")

        sidebar_box = Gtk.Box(orientation=1)
        sidebar_page.set_child(sidebar_box)

        sidebar_headerbar = Adw.HeaderBar(css_classes=["flat"], )
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
        open_menu_section.append("Open Inventory Folder", "app.open-inventory")
        open_menu_section.append("Import", "app.import")
        open_menu.append_section(None, open_menu_section)

        open_file_button.set_menu_model(open_menu)

        sidebar_headerbar.pack_start(open_file_button)
        sidebar_box.append(sidebar_headerbar)

        # Content

        content_page.set_title("Inventario")
        content_page.set_tag("content")

        self.content_box = Gtk.Box(orientation=1)
        content_page.set_child(self.content_box)

        title_box = Gtk.Box(orientation=1, valign=Gtk.Align.CENTER)

        self.title_label = Gtk.Label(label="Inventario", css_classes=["title-4"], ellipsize=3)
        title_box.append(self.title_label)

        self.subtitle_label = Gtk.Label(visible=False,label="~/", css_classes=["caption"], opacity=0.6, ellipsize=1)
        title_box.append(self.subtitle_label)

        self.content_headerbar = Gtk.HeaderBar(css_classes=["flat"], title_widget=title_box, show_title_buttons=False)
        self.content_box.append(self.content_headerbar)

        self.search_button_toggle = Gtk.ToggleButton()
        self.search_button_toggle.set_icon_name("pan-down-symbolic")
        self.search_button_toggle.connect("clicked", self.toggle_search_bar)

        self.search_revealer = Gtk.Revealer(transition_type=4)

        self.search_entry = Gtk.Entry(placeholder_text=_("Search"), hexpand=True,
                primary_icon_name="dialog-information-symbolic",
                primary_icon_tooltip_text="Use ! then > or < to filter values",
                primary_icon_sensitive=False,
                secondary_icon_name="edit-clear-symbolic",
                width_request=150)
        #self.search_entry.set_property(primary_icon_name, "info-symbolic")

        self.search_entry.connect("activate", self.filter_rows)
        self.search_entry.connect("changed", self.entry_text_inserted)

        self.search_entry.connect("icon-press", self.delete_search_text)

        search_button = Gtk.Button(icon_name="system-search-symbolic",
                hexpand=True, css_classes=["accent"])
        delete_search_button = Gtk.Button(icon_name="edit-delete-symbolic", hexpand=True)
        add_search_option_button = Gtk.Button(icon_name="list-add-symbolic", hexpand=True)

        detail_just_names = []
        for detail in self.details_names:
            detail_just_names.append(detail[0])
        self.search_selector = Gtk.DropDown.new_from_strings(detail_just_names)
        self.search_selector.set_selected(2)
        self.search_bar_box = Gtk.FlowBox(margin_start=4, margin_end=4, margin_bottom=4,
                selection_mode=Gtk.SelectionMode.NONE)

        search_button.connect("clicked", self.filter_rows)
        delete_search_button.connect("clicked", self.delete_filter_rows)
        add_search_option_button.connect("clicked", self.add_new_search_option)

        options_box = Gtk.Box(spacing=6)
        first_search_box = Gtk.Box(spacing=6)

        options_box.append(search_button)
        options_box.append(add_search_option_button)
        options_box.append(delete_search_button)

        #options_box.append()

        first_search_box.append(self.search_entry)
        first_search_box.append(self.search_selector)
        self.search_bar_box.append(options_box)
        self.search_bar_box.append(first_search_box)

        # for detail in self.details_names:
        #     self.search_selector.append_text(detail[0])
        # self.search_selector.set_active(2)

        self.search_revealer.set_child(self.search_bar_box)

        self.content_box.append(self.search_revealer)

        toggle_sidebar_button = Gtk.Button(icon_name="go-previous-symbolic", visible=False)
        toggle_sidebar_button.connect("clicked", self.toggle_sidebar)
        self.content_headerbar.pack_start(toggle_sidebar_button)

        menu_button = Gtk.MenuButton()
        menu_button.set_icon_name("open-menu-symbolic")
        menu = Gio.Menu()
        menu.append(_("Preferences"), "app.preferences")
        menu.append(_("Keyboard shortcuts"), "win.show-help-overlay")
        menu.append(_("About"), "app.about")
        menu_button.set_menu_model(menu)

        add_button = Gtk.Button()
        add_button.set_icon_name("list-add-symbolic")
        add_button.connect("clicked", self.add_new_item_or_product_dialog)

        delete_item_button = Gtk.Button(css_classes=["error"])
        delete_item_button.set_icon_name("user-trash-symbolic")
        delete_item_button.connect("clicked", self.on_delete_selected_button_clicked)

        self.content_headerbar.pack_end(menu_button)
        #self.content_headerbar.pack_start(self.search_revealer)
        self.content_headerbar.pack_start(self.search_button_toggle)

        self.content_scrolled_window = Gtk.ScrolledWindow(vexpand=True, overlay_scrolling=True)
        self.content_scrolled_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.toast_overlay = Adw.ToastOverlay()
        self.toast_overlay.set_child(self.content_scrolled_window)
        self.content_box.append(self.toast_overlay)

        self.action_bar = Gtk.ActionBar()
        self.action_bar_revealer = Gtk.Revealer(transition_type=4)
        self.action_bar_revealer.set_child(self.action_bar)

        column_visibility_popover = Gtk.Popover(halign=Gtk.Align.END, has_arrow=False)
        column_visibility_popover.set_position(Gtk.PositionType.TOP)
        column_visibility_popover.set_offset(0,-6)
        self.column_visibility_button = Gtk.MenuButton(icon_name="open-menu-symbolic", popover = column_visibility_popover)

        self.action_bar.pack_end(self.column_visibility_button)
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
        self.right_pane_content_box.append(self.item_info_revealer)

        self.info_scrolled_window_product_custom = Gtk.ScrolledWindow(vexpand=True)
        self.info_scrolled_window_product_custom.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)


        self.right_pane_content_box.append(self.info_scrolled_window_product_custom)
        self.model = Gio.ListStore(item_type=Item)

        for i in range(len(self.sidebar_options)):
            self.sidebar_navigation_listBox.append(Gtk.Label(label = self.sidebar_options[i], xalign=0))

        for detail in self.details_names:
            self.filter_parameters.append(["", detail[1]])

        # Items column view

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

        self.selection_model = Gtk.SingleSelection.new(model=self.sorter_model)
        self.selection_model.connect("selection-changed", self.on_selection_changed)

        self.cv.set_model(self.selection_model)
        self.cv.connect("activate", self.on_column_view_activated)

        for detail in self.details_names:
            self.add_column(detail[0], detail[1], detail[2], self.cv)

        column_visibility_popover_box = Gtk.Box(orientation=1)
        self.column_visibility_check_buttons = []

        for column in self.cv.get_columns():
            column_visibility_popover_box.append(self.column_visibility_check_button(column, self.column_visibility_check_buttons))

        column_visibility_popover.set_child(column_visibility_popover_box)

        # products column view

        self.products_model = Gio.ListStore(item_type=Product)

        self.products_cv = Gtk.ColumnView(single_click_activate=False, reorderable=True, css_classes=["flat"])

        # ListStore -> FilterListModel -> TreeListModel -> SortListModel -> SingleSelection

        self.products_row_filter = Gtk.CustomFilter()
        self.products_row_filter.set_filter_func(self.filter)
        self.products_tree_model_filter = Gtk.FilterListModel(model=self.products_model)
        self.products_tree_model_filter.set_filter(self.products_row_filter)

        self.products_cv.set_show_column_separators(self.settings.get_boolean("enable-columns-separators"))
        self.products_cv.set_show_row_separators(self.settings.get_boolean("enable-rows-separators"))

        self.products_tree_model = Gtk.TreeListModel.new(self.products_tree_model_filter, False, True, self.model_func)
        self.products_tree_sorter = Gtk.TreeListRowSorter.new(self.cv.get_sorter())
        self.products_sorter_model = Gtk.SortListModel(model=self.products_tree_model, sorter=self.products_tree_sorter)

        self.products_selection_model = Gtk.SingleSelection.new(model=self.products_sorter_model)
        self.products_selection_model.connect("selection-changed", self.on_selection_changed)

        self.products_cv.set_model(self.products_selection_model)
        self.products_cv.connect("activate", self.on_column_view_activated)

        for detail in self.product_details_names:
            self.add_column(detail[0], detail[1], detail[2], self.products_cv)

        products_column_visibility_popover = Gtk.Popover(halign=Gtk.Align.END, has_arrow=False)
        products_column_visibility_popover.set_position(Gtk.PositionType.TOP)
        products_column_visibility_popover.set_offset(0,-6)
        self.products_column_visibility_button = Gtk.MenuButton(icon_name="open-menu-symbolic", popover = products_column_visibility_popover)

        products_column_visibility_popover_box = Gtk.Box(orientation=1)
        self.products_column_visibility_check_buttons = []

        for column in self.products_cv.get_columns():
            products_column_visibility_popover_box.append(self.column_visibility_check_button(column, self.products_column_visibility_check_buttons))

        products_column_visibility_popover.set_child(products_column_visibility_popover_box)

        self.action_bar.pack_end(self.products_column_visibility_button)

        self.navigation_select_page(self.last_page)

    def column_visibility_check_button(self, column, array):
        title = column.get_title()
        box = Gtk.Box(orientation=0)
        box.append(Gtk.Label(label=title, hexpand=True, xalign=0, margin_end=10))
        check_button = Gtk.CheckButton(active = column.get_visible())
        array.append(check_button)
        check_button.connect("toggled", self.on_check_button_toggled, column)
        box.append(check_button)
        return box

    def add_new_search_option(self, btn):
        new_search_box = Gtk.Box(spacing=6)
        search_entry = Gtk.Entry(placeholder_text=_("New Search Option"), hexpand=True,
                primary_icon_name="dialog-information-symbolic",
                primary_icon_tooltip_text="Use ! then > or < to filter values",
                primary_icon_sensitive=False,
                secondary_icon_name="edit-clear-symbolic",
                width_request=150)
        search_entry.connect("icon-press", self.delete_search_text)
        detail_just_names = []
        search_entry.connect("activate", self.filter_rows)
        search_entry.connect("changed", self.entry_text_inserted)
        for detail in self.details_names:
            detail_just_names.append(detail[0])
        search_selector = Gtk.DropDown.new_from_strings(detail_just_names)
        search_selector.set_selected(0)

        delete_search_button = Gtk.Button(icon_name="edit-delete-symbolic",
                css_classes=["error"])
        delete_search_button.connect("clicked", self.delete_search_option, new_search_box)
        new_search_box.append(search_entry)
        new_search_box.append(search_selector)
        new_search_box.append(delete_search_button)

        self.search_bar_box.append(new_search_box)

    def delete_search_option(self, btn, widget):
        self.search_bar_box.remove(widget)
    def delete_search_text(self, entry, text):
        entry.set_text("")

    def entry_text_inserted(self, entry):
        text = entry.get_text()
        if "!" in text:
            entry.add_css_class("success")
        if not "!" in text:
            entry.remove_css_class("success")

    def filter_rows(self, btn):
        self.filter_parameters = []
        for detail in self.details_names:
            self.filter_parameters.append(["", detail[1]])

        for child_index, child in enumerate(self.search_bar_box):
            if child_index == 0:
                continue
            condition = child.get_child().get_first_child().get_text()
            detail_call = self.details_names[child.get_child().get_first_child().get_next_sibling().get_selected()][1]
            for index, detail in enumerate(self.details_names):
                if detail[1] == detail_call:
                    self.filter_parameters[index][0] = condition
        self.row_filter.changed(Gtk.FilterChange.DIFFERENT)

        self.update_sidebar_item_info()

    def delete_filter_rows(self, btn=None):
        self.filter_parameters = []
        for detail in self.details_names:
            self.filter_parameters.append(["", detail[1]])
        self.row_filter.changed(Gtk.FilterChange.DIFFERENT)

        childs_to_remove = []
        for child_index, child in enumerate(self.search_bar_box):
            if child_index == 0:
                continue
            elif child_index == 1:
                child.get_child().get_first_child().set_text("")
            else:
                childs_to_remove.append(child)
        for child in childs_to_remove:
            self.search_bar_box.remove(child)

    def filter(self, item):
        show = True

        if self.last_page == self.low_stock_index:
            if int(item.get_detail("item_quantity") or 0) < int(item.get_detail("item_low_stock") or 0):
                pass
            else:
                return False

        if self.last_page == self.out_of_stock_index:
            if int(item.get_detail("item_quantity") or 0) == 0:
                pass
            else:
                return False

        for parameter in self.filter_parameters:
            text = parameter[0] # text to search
            #text = text.lower()
            detail_call = parameter[1] # detail where to search
            item_detail = item.get_detail(detail_call) # item detail

            if text == "":
                continue

            if text[0] == "!":
                try:
                    float(text[2:])
                    float(item_detail)
                except:
                    show = False
                    break
                value = float(text[2:])
                if text[1] == ">":
                    if float(item_detail) > value:
                        continue
                elif text[1] == "<":
                    if float(item_detail) < value:
                        continue
                else:
                    show = False
                    break

            if item_detail == None:
                show = False
                break
            if text.lower() in str(item_detail).lower():
                continue
            else:
                show = False
                break
        return show

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
        if self.last_page == self.items_index:
            self.selected_item = selection_model.get_selection().get_maximum()
            self.update_sidebar_item_info()

        elif self.last_page == self.invoices_index:
            self.selected_item = selection_model.get_selection().get_maximum()

        elif self.last_page == self.products_index:
            self.selected_product = selection_model.get_selection().get_maximum()
            self.update_sidebar_product_info()

        elif self.last_page == self.low_stock_index:
            self.selected_item = selection_model.get_selection().get_maximum()
            self.update_sidebar_item_info()

        elif self.last_page == self.out_of_stock_index:
            self.selected_item = selection_model.get_selection().get_maximum()
            self.update_sidebar_item_info()

        print("selection changed")

    def read_inventory_file(self, inventory_path):
        self.model.remove_all()
        if inventory_path == "":
            return

        items_list_path = inventory_path + "/inventory.csv"
        preferences_path = inventory_path + "/preferences.csv"
        products_folder_path = inventory_path + "/products/"

        parent_dir = os.path.dirname(products_folder_path)
        os.makedirs(parent_dir, exist_ok=True)

        products_files = [f for f in os.listdir(products_folder_path) if os.path.isfile(os.path.join(products_folder_path, f))]

        for file in products_files:
            this_product_path = products_folder_path + file

            try:
                open(this_product_path, 'r').read()
            except Exception as e:
                self.send_toast("Error reading inventory file:" + str(e))
                return 0

            with open(this_product_path, 'r') as file:
                file_content = file.read()
                directory, file_name = os.path.split(this_product_path)
                reader = csv.reader(file_content.splitlines())

                product_detail_call_list = []
                part_detail_call_list = []

                for i, row in enumerate(reader):
                    if i == 0:
                        for i, value in enumerate(row):
                            product_detail_call_list.append(value)
                    elif i == 1:
                        new_product = Product()
                        for index, value in enumerate(row):
                            if index > len(product_detail_call_list) - 1:
                                break
                            if value:
                                try:
                                    type_info = self.product_details_names[index][2]
                                    detail_call = product_detail_call_list[index]
                                    if type_info == "int":
                                        new_value = int(round(float(value)))
                                    elif type_info == "cost":
                                        new_value = float(value)
                                    else:
                                        new_value = str(value)
                                    new_product.set_detail(detail_call, new_value)
                                    is_custom_value_row = True
                                except:
                                    pass
                    elif i == 2:
                        for i, value in enumerate(row):
                            part_detail_call_list.append(value)
                    else:
                        new_part = Part()
                        for i, value in enumerate(row):
                            new_part.set_detail(part_detail_call_list[i], value)
                        print(new_part)
                        new_product.append_part(new_part)
            self.products_model.append(new_product)
        try:
            open(preferences_path, 'r').read()
        except Exception as e:
            self.send_toast("Error reading preferences file:" + str(e))
            print(str(e))
            return 0

        with open(preferences_path, 'r') as file:
            file_content = file.read()
            directory, file_name = os.path.split(preferences_path)
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
                if i == 1:
                    for i, value in enumerate(row):
                        if value == "False":
                            try:
                                self.products_cv.get_columns()[i]
                            except:
                                pass
                            else:
                                self.products_cv.get_columns()[i].set_visible(False)
                                self.products_column_visibility_check_buttons[i].set_active(False)

        try:
            open(items_list_path, 'r').read()
        except Exception as e:
            self.send_toast("Error reading inventory file:" + str(e))
            return 0

        with open(items_list_path, 'r') as file:
            file_content = file.read()
            directory, file_name = os.path.split(items_list_path)
            reader = csv.reader(file_content.splitlines())
            is_custom_value_row = False

            custom_info_start_index = 0

            item_detail_call_list = []

            for i, row in enumerate(reader):
                if i == 0:
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

            self.settings.set_string("last-inventory-path", inventory_path)
            self.title_label.set_label(os.path.basename(os.path.normpath(inventory_path)))
            self.subtitle_label.set_visible(True)
            self.subtitle_label.set_label("~" + inventory_path)
            self.send_toast("File successfully opened")

    def save_inventory_file(self, inventory_path):
        items_list_path = inventory_path + "/inventory.csv"
        products_path = inventory_path + "/products/"
        preferences_path = inventory_path + "/preferences.csv"

        parent_dir = os.path.dirname(products_path)
        os.makedirs(parent_dir, exist_ok=True)

        if inventory_path == "":
            self.save_inventory_file_as()
            return
        try:
            open(items_list_path, 'w', newline='\n')
        except Exception as e:
            self.send_toast(str(e))
            print(str(e))
        else:
            with open(items_list_path, 'w', newline='\n') as csvfile:
                writer = csv.writer(csvfile)

                column_view_row = [detail_name[1] for detail_name in self.details_names]
                writer.writerow(column_view_row)

                for item in self.model:
                    item_row = [item.get_detail(self.details_names[index][1]) for index in range(len(self.details_names))]
                    for custom_value in item.custom_values_list():
                        item_row.append(custom_value[0])
                        item_row.append(custom_value[1])
                    writer.writerow(item_row)

        try:
            open(preferences_path, 'w', newline='\n')
        except Exception as e:
            self.send_toast(str(e))
            print(str(e))
        else:
            with open(preferences_path, 'w', newline='\n') as csvfile:
                writer = csv.writer(csvfile)

                column_view_row = [self.cv.get_columns()[index].get_visible() for index in range(len(self.details_names))]
                writer.writerow(column_view_row)

                products_column_view_row = [self.products_cv.get_columns()[index].get_visible() for index in range(len(self.product_details_names))]
                writer.writerow(products_column_view_row)

        for product in self.products_model:
            this_product_path = products_path + str(product.product_id) + ".csv"
            try:
                open(this_product_path, 'w', newline='\n')
            except Exception as e:
                self.send_toast(str(e))
                print(str(e))
            else:
                with open(this_product_path, 'w', newline='\n') as csvfile:
                    writer = csv.writer(csvfile)

                    column_view_row = [product_detail_name[1] for product_detail_name in self.product_details_names]
                    writer.writerow(column_view_row)

                    product_row = [product.get_detail(self.product_details_names[index][1]) for index in range(len(self.product_details_names))]
                    writer.writerow(product_row)

                    parts_column_view_row = [part_detail_name[0] for part_detail_name in self.part_item_product_translation]
                    writer.writerow(parts_column_view_row)

                    for part in product.product_parts_list:
                        part_row = [part.get_detail(self.part_item_product_translation[index][0]) for index in range(len(self.part_item_product_translation))]
                        writer.writerow(part_row)

        directory, file_name = os.path.split(inventory_path)
        self.subtitle_label.set_visible(True)
        self.subtitle_label.set_label("~" + directory)
        self.title_label.set_label(file_name)

        self.send_toast("File saved")

        print("files saved in " + str(inventory_path))
        self.settings.set_string("last-inventory-path", inventory_path)

    def on_save_file_path_selected(self, dialog, response, dialog_parent):
        path = dialog_parent.get_file().get_path()

        print("The path is "+str(path))
        if response == Gtk.ResponseType.CANCEL:
            #dialog.destroy()
            pass
        if response == Gtk.ResponseType.ACCEPT:
            if path == None:
                self.send_toast("Invalid path")
                return
            elif os.path.exists(path):
                dialog = Adw.MessageDialog(
                    heading="Replace Folder?",
                    body="There is already a folder named this way",
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

    def replace_file_dialog_responce(self, dialog, response, dialog_parent):
        if response == "cancel":
            dialog.destroy()
        if response == "replace":
            self.save_inventory_file(dialog_parent.get_file().get_path())
            dialog.destroy()


    def save_inventory_file_as(self):
        dialog = Gtk.FileChooserNative(
            title="Save File As",
            transient_for=self,
            action=Gtk.FileChooserAction.SELECT_FOLDER
        )

        dialog.set_accept_label("Select Folder")
        dialog.set_cancel_label("Cancel")

        response = dialog.show()

        dialog.connect("response", self.on_save_file_path_selected, dialog)

    def delete_selected_item(self):
        item_row = self.selection_model.get_item(self.selected_item)
        if item_row == None:
            self.send_toast("No item is selected")
            return
        item_to_delete = item_row.get_item()

        for i, item in enumerate(self.model):
            if item == item_to_delete:
                item_index_to_delete = i
                break

        dialog = Adw.MessageDialog(
            heading="Delete Item?",
            body="This is a destructive action. The item {} will be destroyed and can not be recovered.".format(item_to_delete.item_name),
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

    def delete_selected_product(self):
        if self.selected_product == None:
            self.send_toast("No product is selected")
            return
        product_row = self.products_selection_model.get_item(self.selected_product)
        if product_row == None:
            self.send_toast("No product is selected")
            return
        product_to_delete = product_row.get_item()

        for i, product in enumerate(self.products_model):
            if product == product_to_delete:
                product_index_to_delete = i
                break

        dialog = Adw.MessageDialog(
            heading="Delete Product?",
            body="This is a destructive action. The product {} will be destroyed and can not be recovered.".format(product_to_delete.product_name),
            close_response="cancel",
            transient_for=self,
            modal=True
        )
        dialog.set_title("Delete?")

        dialog.add_response("cancel", "Cancel")
        dialog.add_response("delete", "Delete")
        dialog.set_response_appearance("delete", Adw.ResponseAppearance.DESTRUCTIVE)

        dialog.connect("response", self.on_delete_product_responce, product_index_to_delete)
        dialog.present()
        #item_index = get_row_model_index_from_id(item_to_delete.item_id)

    def on_delete_product_responce(self, dialog, response, product_index):
        if response == "cancel":
            dialog.destroy()

        if response == "delete":
            self.products_model.remove(product_index)

            if self.selected_product != 0:
                self.selected_product -= 1
            elif self.selected_product == 0:
                if len(self.products_model) == 0:
                    self.selected_product = None
                else:
                    self.selected_product = 0
            print(self.selected_product)
            self.update_sidebar_product_info()
            dialog.destroy()
            print(self.selected_product)

            self.send_toast("The item has been deleted")

    def on_delete_selected_button_clicked(self, btn):
        if self.last_page == self.items_index:
            self.delete_selected_item()
        elif self.last_page == self.low_stock_index:
            self.delete_selected_item()
        elif self.last_page == self.out_of_stock_index:
            self.delete_selected_item()
        elif self.last_page == self.products_index:
            self.delete_selected_product()

    def on_delete_item_responce(self, dialog, response, item_index):
        if response == "cancel":
            dialog.destroy()

        if response == "delete":
            self.model.remove(item_index)

            if self.selected_item != 0:
                self.selected_item -= 1
            elif self.selected_item == 0:
                if len(self.model) == 0:
                    self.selected_item = None
                else:
                    self.selected_item = 0

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
                self.read_inventory_file(file_path)
        else:
            dialog.destroy()

    def open_file_chooser(self, btn=None):
        dialog = Gtk.FileChooserNative(
            title="Open Inventory Folder",
            transient_for=None,
            action=Gtk.FileChooserAction.SELECT_FOLDER,
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
                        hexpand=True, name=self.details_names[i][1]))
            if self.details_names[i][2] == "str":
                add_row = False
            elif self.details_names[i][2] == "STR":
                add_row = False
            elif self.details_names[i][2] == "int":
                spin_button = Gtk.SpinButton(climb_rate=1, hexpand=True, margin_end=4,
                        margin_top=4, margin_bottom=4, name=self.details_names[i][2])
                spin_button.set_adjustment(Gtk.Adjustment(step_increment=1, lower=0, value=0, upper=100000000))
                box2.append(spin_button)
                if value != None:
                    spin_button.set_value(float(value))
            elif self.details_names[i][2] == "cost":
                add_row = False
            elif self.details_names[i][2] == "DATE":
                add_row = False
            elif self.details_names[i][2] == "cat":
                add_row = False
            elif self.details_names[i][2] == "date":
                box2.append(Gtk.Label(label=self.get_formatted_date(), hexpand=True, margin_end=4, margin_top=4,
                        margin_bottom=4, xalign=0, name=self.details_names[i][2]))
            elif self.details_names[i][2] == "value":
                add_row = False

            if add_row:
                list_box_add.append(box2)

        add_item_window.set_content(box)
        add_item_window.present()

    def update_sidebar_product_info(self):
        product_index = self.selected_product

        info_page_status_page = Adw.StatusPage(title="Info Page",
                icon_name="view-list-bullet-symbolic", hexpand=True, vexpand=True,
                description="There are no products to display")

        if len(self.products_model) == 0 or product_index == None:
            self.info_scrolled_window_product_custom.set_child(info_page_status_page)
            return
        if product_index > len(self.products_model):
            product_index = 0

        self.selected_product = product_index
        self.sidebar_product_info_list_box = Gtk.ListBox(show_separators=True, selection_mode=0,
                margin_start=6, margin_end=6, vexpand=True, hexpand=True)#, width_request=300)
        box1 = Gtk.Box(orientation=1, hexpand=True)

        if self.products_selection_model.get_item(product_index) != None:
            product = self.products_selection_model.get_item(product_index).get_item()
        else:
            return

        sidebar_scrolled_window_product_info = Gtk.ScrolledWindow(vexpand=True, hexpand=True)
        sidebar_scrolled_window_product_info.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        sidebar_scrolled_window_product_info.set_child(self.sidebar_product_info_list_box)
        box5 = Gtk.Box(orientation=1, hexpand=True)

        name = product.product_name or "No Name"
        description = product.product_description or "There is no description"

        box5.append(Gtk.Label(label=name, margin_top=2, margin_bottom=6, css_classes=["title-1"], xalign=0, margin_start=6))
        box5.append(Gtk.Label(label=description, margin_top=2, margin_bottom=6, css_classes=["title-4"], xalign=0, margin_start=6))
        box5.append(Gtk.Separator())
        box5.append(sidebar_scrolled_window_product_info)

        box1.append(box5)
        #box1.append(self.sidebar_product_info_list_box)

        product_id=self.products_model[product_index].product_id

        add_this_button = Gtk.Button(hexpand=True, label="Make One", css_classes=["success"])
        remove_this_button = Gtk.Button(hexpand=True, label="-1", css_classes=["error"])
        edit_button = Gtk.Button(icon_name="document-edit-symbolic", hexpand=True)

        bottom_buttons_box = Gtk.Box(homogeneous=True, margin_start=6, margin_end=6, margin_top=6, margin_bottom=6, hexpand=True, spacing=6)
        bottom_buttons_box.append(edit_button)
        bottom_buttons_box.append(add_this_button)
        bottom_buttons_box.append(remove_this_button)

        edit_button.connect("clicked", self.show_edit_product_dialog)
        #add_this_button.connect("clicked", self.on_add_stock_to_product_button_clicked)
        #remove_this_button.connect("clicked", self.on_remove_one_product_button_clicked)

        self.info_scrolled_window_product_custom.set_child(box1)

        self.sidebar_product_parts_list_box = Gtk.ListBox(show_separators=True, selection_mode=0,
                margin_start=6, margin_end=6, vexpand=True, hexpand=True)#, width_request=300)

        parts_column_view = Gtk.ColumnView()
        parts_model = product.parts_list()
        tree_model = Gtk.TreeListModel.new(parts_model, False, True, self.model_func)
        tree_sorter = Gtk.TreeListRowSorter.new(parts_column_view.get_sorter())
        sorter_model = Gtk.SortListModel(model=tree_model, sorter=tree_sorter)
        selection = Gtk.NoSelection.new(model=sorter_model)
        parts_column_view.set_model(selection)

        for detail in self.part_item_product_translation:
            self.add_part_column_view_column(detail[3], detail[0], parts_column_view)

        self.add_part_column_view_column("Used", "used_quantity", parts_column_view)

        scrolled_window_product_parts = Gtk.ScrolledWindow(vexpand=True, hexpand=True)
        scrolled_window_product_parts.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolled_window_product_parts.set_child(parts_column_view)#self.sidebar_product_parts_list_box)

        middle_title_and_buttons_box = Gtk.Box(margin_top=6, margin_bottom=6, margin_start=6, margin_end=6, hexpand=True)
        middle_title_and_buttons_box.append(Gtk.Label(label="Parts used", margin_top=2, margin_bottom=6,
                css_classes=["title-3"], xalign=0, hexpand=True))

        add_part_button = Gtk.Button(hexpand=True, label="+", css_classes=["success"], halign=Gtk.Align.END)
        middle_title_and_buttons_box.append(add_part_button)

        box1.append(Gtk.Separator())
        box1.append(middle_title_and_buttons_box)
        box1.append(Gtk.Separator())
        box1.append(scrolled_window_product_parts)
        box1.append(bottom_buttons_box)

        for i in range(len(product.product_parts_list)):
            part = product.product_parts_list[i]
            box6 = Gtk.Box()
            box6.append(Gtk.Label(label=part.part_name, xalign=0, hexpand=True, margin_end=6, margin_start=6, margin_top=3, margin_bottom=3))
            box6.append(Gtk.Label(label=part.part_description, xalign=1, hexpand=True, halign=Gtk.Align.FILL, margin_end=6))
            self.sidebar_product_parts_list_box.append(box6)

        for i in range(len(self.product_details_names)):
            box = Gtk.FlowBox(margin_start=6, margin_end=6, max_children_per_line=2,
                    selection_mode=Gtk.SelectionMode.NONE)
            name = self.product_details_names[i][0] + ":"
            box.append(Gtk.Label(ellipsize=2, label=name, xalign=0, hexpand=True, margin_end=6))

            product.get_detail(self.product_details_names[i][1])

            detail_type = self.product_details_names[i][2]
            value = product.get_detail(self.product_details_names[i][1])
            if detail_type == "cost":
                if value != None:
                    text = round(float(value), 2)
            else:
                text = value
            if text == "" or text == None:
                text = "..."
            box.append(Gtk.Label(ellipsize=3, label=text, xalign=1, hexpand=True, halign=Gtk.Align.FILL))
            self.sidebar_product_info_list_box.append(box)
        print("updated product info")

    def add_part_column_view_column(self, detail_name, detail_call, column_view):
        factory = Gtk.SignalListItemFactory()
        factory.connect("setup", self._on_factory_setup)
        factory.connect("bind", self._on_factory_bind, detail_call)
        factory.connect("unbind", self._on_factory_unbind, detail_call)
        factory.connect("teardown", self._on_factory_teardown)

        col1 = Gtk.ColumnViewColumn(title=detail_name, factory=factory)
        col1.props.expand = True
        column_view.append_column(col1)

    def show_edit_product_dialog(self):
        print("show_edit_product_dialog")

    def update_sidebar_item_info(self):
        item_index = self.selected_item

        info_page_status_page = Adw.StatusPage(title="Info Page",
                icon_name="view-list-bullet-symbolic", hexpand=True, vexpand=True,
                description="There are no items to display")

        if len(self.model) == 0:
            self.info_scrolled_window_product_custom.set_child(info_page_status_page)
            return

        self.sidebar_item_info_list_box = Gtk.ListBox(show_separators=True, selection_mode=0,
                margin_start=6, margin_end=6, vexpand=True, hexpand=True)#, width_request=300)
        box1 = Gtk.Box(orientation=1, hexpand=True)

        if self.selection_model.get_item(item_index) != None:
            item = self.selection_model.get_item(item_index).get_item()
        else:
            return

        sidebar_scrolled_window_item_info = Gtk.ScrolledWindow(vexpand=True, hexpand=True)
        sidebar_scrolled_window_item_info.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        sidebar_scrolled_window_item_info.set_child(self.sidebar_item_info_list_box)
        box5 = Gtk.Box(orientation=1, hexpand=True)

        name = item.item_name or "No Name"
        description = item.item_description or "There is no description"

        box5.append(Gtk.Label(label=name, margin_top=2, margin_bottom=6, css_classes=["title-1"], xalign=0, margin_start=6))
        box5.append(Gtk.Label(label=description, ellipsize=3, margin_top=2, margin_bottom=6, css_classes=["title-4"], xalign=0, margin_start=6))
        box5.append(Gtk.Separator())

        box1.append(box5)
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

        item_id=self.model[item_index].item_id

        add_this_button = Gtk.Button(hexpand=True, label="Add", css_classes=["success"])
        remove_this_button = Gtk.Button(hexpand=True, label="-1", css_classes=["error"])
        edit_button = Gtk.Button(icon_name="document-edit-symbolic", hexpand=True)

        buy_more_button = Gtk.LinkButton(css_classes=["accent"])
        buy_more_button.set_icon_name("shopping-cart-symbolic")

        if item.item_buy_link != None:
            buy_more_button.set_uri(item.item_buy_link)
        else:
            buy_more_button.set_sensitive(False)

        datasheet_button = Gtk.LinkButton(css_classes=[""])
        datasheet_button.set_icon_name("rich-text-symbolic")

        if item.item_datasheet != None:
            datasheet_button.set_uri(item.item_datasheet)
        else:
            datasheet_button.set_sensitive(False)

        bottom_buttons_box = Gtk.Box(homogeneous=True, margin_start=6, margin_end=6, margin_top=6, margin_bottom=6, hexpand=True, spacing=6)
        bottom_buttons_box.append(edit_button)
        bottom_buttons_box.append(add_this_button)
        bottom_buttons_box.append(remove_this_button)
        bottom_buttons_box.append(buy_more_button)
        bottom_buttons_box.append(datasheet_button)

        edit_button.connect("clicked", self.show_edit_item_dialog)
        add_this_button.connect("clicked", self.on_add_stock_to_item_button_clicked)
        remove_this_button.connect("clicked", self.on_remove_one_item_button_clicked)

        box1.append(bottom_buttons_box)

        self.info_scrolled_window_product_custom.set_child(box1)

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
            box.append(Gtk.Label(ellipsize=3, label=text, xalign=1, hexpand=True, halign=Gtk.Align.FILL))
            self.sidebar_item_info_list_box.append(box)
        print("updated item info")

    def on_column_view_activated(self, cv, row_index):
        if self.last_page == self.items_index:
            self.selected_item = row_index
            self.show_edit_item_dialog()
            self.update_sidebar_item_info()
        elif self.last_page == self.invoices_index:
            item = self.selection_model.get_item(self.selected_item).get_item()
            self.invoice_items_model.append(item)
        elif self.last_page == self.products_index:
            self.selected_product = row_index
            self.show_edit_product_dialog()
            self.update_sidebar_product_info()

    def show_edit_product_dialog(self, btn=None):
        print("show_edit_product_dialog")
        product_index = self.selected_product
        if product_index < len(self.model):
            product = self.products_selection_model.get_item(self.selected_product).get_item()
        else:
            return

        edit_product_window = Adw.Window(resizable=True)
        product_name = product.product_name
        if product_name != None:
            edit_product_window.set_title("Edit " + product_name + " " + product.product_id)
        else:
            edit_product_window.set_title("Edit " + product.product_id)
        edit_product_window.set_default_size(600, 700)
        edit_product_window.set_modal(True)
        edit_product_window.set_transient_for(self)
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
        cancel_button.connect("clicked", self.quit_window, edit_product_window)
        add_button = Gtk.Button(label=_("Edit"), hexpand=True, margin_top=6, margin_bottom=6, css_classes=["suggested-action"])
        add_button.connect("clicked", self.edit_existing_product, list_box_add, product, edit_product_window)
        box3.append(cancel_button)
        box3.append(add_button)
        box.append(box3)

        for i in range(len(self.product_details_names)):
            box2 = Gtk.Box(homogeneous=True, margin_end=4, margin_start=4)
            list_box_add.append(box2)
            box2.append(Gtk.Label(label=self.product_details_names[i][0], xalign=0,
                    hexpand=True, name=self.product_details_names[i][1]))
            value = product.get_detail(self.product_details_names[i][1])
            if self.product_details_names[i][2] == "STR":
                box2.append(Gtk.Label(label=value, hexpand=True, margin_top=4,
                        margin_bottom=4, xalign=0, name=self.product_details_names[i][2]))
            elif self.product_details_names[i][2] == "int":
                spin_button = Gtk.SpinButton(climb_rate=1, hexpand=True, margin_top=4,
                        margin_bottom=4, name=self.product_details_names[i][2])
                spin_button.set_adjustment(Gtk.Adjustment(step_increment=1, lower=0, value=0, upper=100000000))
                box2.append(spin_button)
                if value != None:
                    spin_button.set_value(float(value))
            elif self.product_details_names[i][2] == "cost":
                spin_button = Gtk.SpinButton(climb_rate=1, digits=2, hexpand=True,
                        margin_top=4, margin_bottom=4, name=self.product_details_names[i][2])
                spin_button.set_adjustment(Gtk.Adjustment(step_increment=0.01, lower=0, value=0, upper=100000000))
                box2.append(spin_button)
                if value != None:
                    spin_button.set_value(float(value))
            elif self.product_details_names[i][2] == "DATE":
                box2.append(Gtk.Label(label=value, hexpand=True, margin_top=4, margin_bottom=4,
                        xalign=0, name=self.product_details_names[i][2]))
            elif self.product_details_names[i][2] == "date":
                box2.append(Gtk.Label(label=self.get_formatted_date(), hexpand=True, margin_top=4,
                        margin_bottom=4, xalign=0, name=self.product_details_names[i][2]))
            elif self.product_details_names[i][2] == "cat":
                drop_down = Gtk.DropDown.new_from_strings(self.products_categories)
                drop_down.set_name(name=self.product_details_names[i][2])
                #drop_down.set_size_request(100, 0)
                #drop_down.set_enable_search(True)
                drop_down.set_margin_top(4)
                drop_down.set_margin_bottom(4)
                drop_down.set_selected(self.find_index(self.products_categories, value))

                # category_drop_down = Gtk.ComboBoxText(margin_top=4, margin_bottom=4,margin_end=4,
                #         name=self.product_details_names[i][2])
                # for category in self.products_categories:
                #     category_drop_down.append_text(category)
                box2.append(drop_down)
                #category_drop_down.set_active(self.find_index(self.products_categories, value))

            elif self.product_details_names[i][2] == "value":
                spin_button = Gtk.SpinButton(climb_rate=1, digits=2, hexpand=True, margin_top=4, margin_bottom=4)
                spin_button.set_width_chars(6)
                spin_button.set_adjustment(Gtk.Adjustment(step_increment=0.1, lower=0, value=0, upper=100000000))
                number, unit = self.split_string_with_unit(value)
                spin_button.set_value(float(number))
                drop_down = Gtk.DropDown.new_from_strings(self.units_of_measure)
                drop_down.set_size_request(100, 0)
                drop_down.set_enable_search(True)
                drop_down.set_margin_start(6)
                drop_down.set_margin_top(4)
                drop_down.set_margin_bottom(4)
                drop_down.set_selected(self.find_index(self.units_of_measure, unit))
                box4 = Gtk.Box(name=self.product_details_names[i][2])
                box4.append(spin_button)
                box4.append(drop_down)
                box2.append(box4)
            else:
                entry = Gtk.Entry(placeholder_text=_("Write here"),hexpand=True, margin_top=4,
                        margin_bottom=4, name=self.product_details_names[i][2])
                box2.append(entry)
                if value != None:
                    entry.set_text(str(value))
        edit_product_window.set_content(box)
        edit_product_window.present()

    def edit_existing_product(self, btn, list_box, product, window):
        print("edit_existing_product")
        for i in range(len(self.product_details_names)):
            value_widget_row = list_box.get_row_at_index(i)

            if value_widget_row != None:
                value_widget = value_widget_row.get_child().get_first_child().get_next_sibling()
                detail_call = value_widget_row.get_child().get_first_child().get_name()
                detail_type = value_widget.get_name()

                if detail_call != None and detail_type != None:
                    if detail_type == "STR":
                        value = value_widget.get_label()
                    elif detail_type == "int":
                        value = int(value_widget.get_value())
                    elif detail_type == "cost":
                        value = float(value_widget.get_value())
                    elif detail_type == "value":
                        value = str(round(float(value_widget.get_first_child().get_value()), 2))
                        unit_index = value_widget.get_first_child().get_next_sibling().get_selected()
                        value += " " + str(self.units_of_measure[unit_index])
                    elif detail_type == "cat":
                        value = self.products_categories[value_widget.get_selected()]
                    else:
                        value = value_widget.get_text()

                    if value == 0 or value == "0" or value == "0.0":
                        value = None

                    product.set_detail(detail_call, value)
        self.update_sidebar_product_info()
        self.send_toast(_("Product successfully edited"))

        window.destroy()

    def show_edit_item_dialog(self, btn=None):
        print("show_edit_item_dialog")
        item_index = self.selected_item
        if item_index < len(self.model):
            item = self.selection_model.get_item(self.selected_item).get_item()
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
            box2 = Gtk.Box(homogeneous=True, margin_end=4, margin_start=4)
            list_box_add.append(box2)
            box2.append(Gtk.Label(label=self.details_names[i][0], xalign=0,
                    hexpand=True, name=self.details_names[i][1]))
            value = item.get_detail(self.details_names[i][1])
            if self.details_names[i][2] == "STR":
                box2.append(Gtk.Label(label=value, hexpand=True, margin_top=4,
                        margin_bottom=4, xalign=0, name=self.details_names[i][2]))
            elif self.details_names[i][2] == "int":
                spin_button = Gtk.SpinButton(climb_rate=1, hexpand=True, margin_top=4,
                        margin_bottom=4, name=self.details_names[i][2])
                spin_button.set_adjustment(Gtk.Adjustment(step_increment=1, lower=0, value=0, upper=100000000))
                box2.append(spin_button)
                if value != None:
                    spin_button.set_value(float(value))
            elif self.details_names[i][2] == "cost":
                spin_button = Gtk.SpinButton(climb_rate=1, digits=2, hexpand=True,
                        margin_top=4, margin_bottom=4, name=self.details_names[i][2])
                spin_button.set_adjustment(Gtk.Adjustment(step_increment=0.01, lower=0, value=0, upper=100000000))
                box2.append(spin_button)
                if value != None:
                    spin_button.set_value(float(value))
            elif self.details_names[i][2] == "DATE":
                box2.append(Gtk.Label(label=value, hexpand=True, margin_top=4, margin_bottom=4,
                        xalign=0, name=self.details_names[i][2]))
            elif self.details_names[i][2] == "date":
                box2.append(Gtk.Label(label=self.get_formatted_date(), hexpand=True, margin_top=4,
                        margin_bottom=4, xalign=0, name=self.details_names[i][2]))
            elif self.details_names[i][2] == "cat":
                drop_down = Gtk.DropDown.new_from_strings(self.items_categories)
                drop_down.set_name(name=self.details_names[i][2])
                #drop_down.set_size_request(100, 0)
                #drop_down.set_enable_search(True)
                drop_down.set_margin_top(4)
                drop_down.set_margin_bottom(4)
                drop_down.set_selected(self.find_index(self.items_categories, value))

                # category_drop_down = Gtk.ComboBoxText(margin_top=4, margin_bottom=4,margin_end=4,
                #         name=self.details_names[i][2])
                # for category in self.items_categories:
                #     category_drop_down.append_text(category)
                box2.append(drop_down)
                #category_drop_down.set_active(self.find_index(self.items_categories, value))

            elif self.details_names[i][2] == "value":
                spin_button = Gtk.SpinButton(climb_rate=1, digits=2, hexpand=True, margin_top=4, margin_bottom=4)
                spin_button.set_width_chars(6)
                spin_button.set_adjustment(Gtk.Adjustment(step_increment=0.1, lower=0, value=0, upper=100000000))
                number, unit = self.split_string_with_unit(value)
                spin_button.set_value(float(number))
                drop_down = Gtk.DropDown.new_from_strings(self.units_of_measure)
                drop_down.set_size_request(100, 0)
                drop_down.set_enable_search(True)
                drop_down.set_margin_start(6)
                drop_down.set_margin_top(4)
                drop_down.set_margin_bottom(4)
                drop_down.set_selected(self.find_index(self.units_of_measure, unit))
                box4 = Gtk.Box(name=self.details_names[i][2])
                box4.append(spin_button)
                box4.append(drop_down)
                box2.append(box4)
            else:
                entry = Gtk.Entry(placeholder_text=_("Write here"),hexpand=True, margin_top=4,
                        margin_bottom=4, name=self.details_names[i][2])
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
            return 0, "  "
        index_of_space = str(input_string).find(" ")
        if index_of_space != -1:
            first_part = input_string[:index_of_space]
            second_part = input_string[index_of_space + 1:]
            try:
                float(first_part)
            except:
                return 0, "  "
            return first_part, second_part
        try:
            float(input_string)
        except:
            return 0, "  "
        return input_string, "  "

    def edit_existing_item(self, btn, list_box, item, window):
        print("edit_existing_item")
        for i in range(len(self.details_names)):
            value_widget_row = list_box.get_row_at_index(i)

            if value_widget_row != None:
                value_widget = value_widget_row.get_child().get_first_child().get_next_sibling()
                detail_call = value_widget_row.get_child().get_first_child().get_name()
                detail_type = value_widget.get_name()

                if detail_call != None and detail_type != None:
                    if detail_type == "STR":
                        value = value_widget.get_label()
                    elif detail_type == "int":
                        value = int(value_widget.get_value())
                    elif detail_type == "cost":
                        value = float(value_widget.get_value())
                    elif detail_type == "value":
                        value = str(round(float(value_widget.get_first_child().get_value()), 2))
                        unit_index = value_widget.get_first_child().get_next_sibling().get_selected()
                        value += " " + str(self.units_of_measure[unit_index])
                    elif detail_type == "cat":
                        value = self.items_categories[value_widget.get_selected()]
                    else:
                        value = value_widget.get_text()

                    if value == 0 or value == "0" or value == "0.0":
                        value = None

                    item.set_detail(detail_call, value)
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
        pass

    def add_column(self, column_name, detail_call, detail_type, column_view):
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
        column_view.append_column(col)

    def scroll_to_the_top(self, change, data):
        print("scroll")
        self.content_scrolled_window.get_vadjustment().set_value(0)

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
            if str(obj_1_detail).lower() < str(obj_2_detail).lower():
                return -1
            elif str(obj_1_detail).lower() == str(obj_2_detail).lower():
                return 0
            return 1

    def show_items(self):
        self.split_view.set_collapsed(False)
        self.content_headerbar.set_show_title_buttons(False)
        self.search_button_toggle.set_visible(True)
        self.column_visibility_button.set_visible(True)
        self.products_column_visibility_button.set_visible(False)
        self.search_revealer.set_reveal_child(self.search_button_toggle.get_active())

        self.content_scrolled_window.set_child(None)
        self.content_scrolled_window.set_child(self.cv)
        if self.settings.get_boolean("enable-horizontal-scrolling"):
            self.content_scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.action_bar_revealer.set_reveal_child(True)

        if self.selected_item != None:
            self.cv.get_model().select_item(self.selected_item, True)
        self.row_filter.changed(Gtk.FilterChange.DIFFERENT)
        self.selected_item = self.selection_model.get_selection().get_maximum()
        self.update_sidebar_item_info()

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

    def quit_window(self, btn, window):
        window.destroy()

    def add_new_item_or_product_dialog(self, btn):
        if self.last_page == self.items_index:
            self.add_new_item_dialog()
        if self.last_page == self.products_index:
            self.add_new_product_dialog()

    def add_new_product_dialog(self, arg=None):
        print("add_new_product_dialog")
        add_product_window = Adw.Window(resizable=True)
        add_product_window.set_title("Add product")

        add_product_window.set_default_size(600, 700)
        add_product_window.set_modal(True)
        add_product_window.set_transient_for(self)
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
        cancel_button.connect("clicked", self.quit_window, add_product_window)
        add_button = Gtk.Button(label=_("Add"), hexpand=True, margin_top=6, margin_bottom=6, css_classes=["suggested-action"])

        box3.append(cancel_button)
        box3.append(add_button)
        box.append(box3)

        for i in range(len(self.product_details_names)):
            box2 = Gtk.Box(homogeneous=True)
            list_box_add.append(box2)
            box2.append(Gtk.Label(label=self.product_details_names[i][0], margin_start=6, xalign=0,
                    hexpand=True))
            if self.product_details_names[i][2] == "str":
                box2.append(Gtk.Entry(placeholder_text=_("Write here"),hexpand=True, margin_end=4, margin_top=4,
                        margin_bottom=4))
            if self.product_details_names[i][2] == "STR":
                box2.append(Gtk.Label(label=self.generate_new_id(), hexpand=True, margin_end=4, margin_top=4,
                        margin_bottom=4, xalign=0))
            if self.product_details_names[i][2] == "int":
                spin_button = Gtk.SpinButton(climb_rate=1, hexpand=True, margin_end=4, margin_top=4, margin_bottom=4)
                spin_button.set_adjustment(Gtk.Adjustment(step_increment=1, lower=0, value=0, upper=100000000))
                box2.append(spin_button)
            if self.product_details_names[i][2] == "cost":
                spin_button = Gtk.SpinButton(climb_rate=1, digits=2, hexpand=True, margin_end=4, margin_top=4, margin_bottom=4)
                spin_button.set_adjustment(Gtk.Adjustment(step_increment=0.01, lower=0, value=0, upper=100000000))
                box2.append(spin_button)
            if self.product_details_names[i][2] == "DATE":
                box2.append(Gtk.Label(label=self.get_formatted_date(), hexpand=True, margin_end=4, margin_top=4,
                        margin_bottom=4, xalign=0))
            if self.product_details_names[i][2] == "date":
                box2.append(Gtk.Label(label=self.get_formatted_date(), hexpand=True, margin_end=4, margin_top=4,
                        margin_bottom=4, xalign=0))
            if self.product_details_names[i][2] == "value":
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
            if self.product_details_names[i][2] == "cat":
                category_drop_down = Gtk.ComboBoxText(margin_top=4, margin_bottom=4,margin_end=4)
                for category in self.items_categories:
                    category_drop_down.append_text(category)
                box2.append(category_drop_down)

        box6.append(Gtk.Separator())
        custom_info_box = Gtk.Box(orientation=1)
        box6.append(custom_info_box)

        box7 = Gtk.Box(hexpand=True)
        label = Gtk.Label(label="Add Parts", hexpand=True, margin_top=6, margin_bottom=6, css_classes=["title-3"])
        add_custom_info_button = Gtk.Button(icon_name="list-add-symbolic", margin_start=6, margin_top=6, margin_bottom=6,margin_end=12)

        box7.append(label)
        box7.append(add_custom_info_button)

        possible_parts_list = []

        for item in self.model:
            item_name_in_list = str(item.item_value or "") + " " + str(item.item_name or "") + " " + str(item.item_package or "")
            possible_parts_list.append(item_name_in_list)

        for product in self.products_model:
            product_name_in_list = str(product.product_name or "") + " " + str(product.product_package or "")
            possible_parts_list.append(product_name_in_list)

        custom_info_box.append(box7)
        #custom_info_box.append()
        custom_info_list_box = Gtk.ListBox(selection_mode = 0, vexpand=True, margin_end=6)
        add_custom_info_button.connect("clicked", self.add_part_to_listbox, custom_info_list_box, possible_parts_list)

        custom_info_box.append(custom_info_list_box)

        add_button.connect("clicked", self.add_product_to_list, list_box_add, add_product_window, custom_info_list_box)

        add_product_window.set_content(box)
        add_product_window.present()

    def add_part_to_listbox(self, btn, list_box, parts_list):
        row_index = 0

        box2 = Gtk.Box(margin_end=4, margin_start=6, margin_top=4, margin_bottom=4, spacing=6)
        list_box.append(box2)
        name = "Custom info"
        part_drop_down = Gtk.DropDown.new_from_strings(parts_list)
        part_drop_down.set_enable_search(True)
        part_drop_down.set_hexpand(True)
        box2.append(part_drop_down)

        quantity_used_spin_button = Gtk.SpinButton()
        quantity_used_spin_button.set_adjustment(Gtk.Adjustment(step_increment=1, lower=0, value=0, upper=100000000))
        box2.append(quantity_used_spin_button)

        delete_button = Gtk.Button(icon_name="user-trash-symbolic")
        delete_button.connect("clicked", self.delete_custom_item_row, list_box)
        box2.append(delete_button)

    def add_product_to_list(self, btn, list_box, window, parts_list_box):
        new_product = Product()
        for i in range(len(self.product_details_names)):
            value_widget = list_box.get_row_at_index(i).get_child().get_first_child().get_next_sibling()
            detail_type = self.product_details_names[i][2]
            detail_name = self.product_details_names[i][1]
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
            new_product.set_detail(detail_name, value)

        parts = 0
        while parts_list_box.get_row_at_index(parts) != None:
            quantity = parts_list_box.get_row_at_index(parts).get_child().get_first_child().get_next_sibling().get_value()
            part_index = parts_list_box.get_row_at_index(parts).get_child().get_first_child().get_selected()

            if part_index == "" or quantity == "":
                continue

            new_part = Part()

            if part_index < len(self.model):
                item = self.model[part_index]
                for detail in self.part_item_product_translation:
                    value = item.get_detail(detail[1])
                    new_part.set_detail(detail[0], value)
                new_part.set_detail("used_quantity", quantity)

            else:
                part = self.products_model[part_index - len(self.model)]
                for detail in self.part_item_product_translation:
                    value = part.get_detail(detail[2])
                    new_part.set_detail(detail[0], value)
                new_part.set_detail("used_quantity", quantity)
            new_product.append_part(new_part)
            parts += 1

        # value = list_box.get_row_at_index(index).get_child().get_first_child().get_next_sibling().get_text()
        # name = list_box.get_row_at_index(index).get_child().get_first_child().get_text()

        self.products_model.append(new_product)
        self.selected_product = len(self.products_model) - 1
        self.update_sidebar_product_info()
        window.destroy()

    def add_new_item_dialog(self, args=None):
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
                for category in self.items_categories:
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
        characters = string.ascii_uppercase + string.digits
        id_length = 5
        new_id = ''.join(random.choice(characters) for _ in range(id_length))
        for i in range(len(self.model)):
            if new_id == self.model[i].item_id:
                new_id = self.generate_new_id()
                for i in range(len(self.products_model)):
                    if new_id == self.products_model[i].product_id:
                        new_id = self.generate_new_id()
        return new_id

    def toggle_sidebar(self, btn):
        self.split_view.set_collapsed(self.split_view.get_collapsed)

    def on_navigation_row_activated(self, list_box, exc):
        selected_row = list_box.get_selected_row()

        self.navigation_select_page(selected_row.get_index())

    def show_products(self):
        print("show products")
        self.split_view.set_collapsed(False)
        self.content_headerbar.set_show_title_buttons(False)
        self.column_visibility_button.set_visible(False)
        self.products_column_visibility_button.set_visible(True)
        self.search_button_toggle.set_visible(False)
        self.search_revealer.set_reveal_child(False)
        self.item_info_revealer.set_reveal_child(False)
        self.action_bar_revealer.set_transition_duration(0)
        self.action_bar_revealer.set_reveal_child(False)
        self.action_bar_revealer.set_transition_duration(250)
        self.products_box = Gtk.Box(margin_start=10, margin_top=10, margin_bottom=10, margin_end=10)
        #self.content_scrolled_window.set_child(self.products_box)

        self.content_scrolled_window.set_child(None)
        self.content_scrolled_window.set_child(self.products_cv)
        if self.settings.get_boolean("enable-horizontal-scrolling"):
            self.content_scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.action_bar_revealer.set_reveal_child(True)

        if self.selected_product != None:
            self.products_cv.get_model().select_item(self.selected_product, True)
        self.update_sidebar_product_info()

    def show_invoice(self, arg=None):
        print("show invoices")
        self.content_headerbar.set_show_title_buttons(True)
        self.split_view.set_collapsed(True)
        self.search_button_toggle.set_visible(False)
        self.search_revealer.set_reveal_child(False)
        self.item_info_revealer.set_reveal_child(False)
        self.action_bar_revealer.set_transition_duration(0)
        self.action_bar_revealer.set_reveal_child(False)
        self.action_bar_revealer.set_transition_duration(250)
        self.invoices_box = Gtk.Box(margin_start=10, margin_top=10, margin_bottom=10, margin_end=10, orientation=1)
        self.content_scrolled_window.set_child(self.invoices_box)

        invoice_status_page = Adw.StatusPage(title="Work in progress",
                icon_name="accessories-text-editor-symbolic", hexpand=True, vexpand=True,
                description="Invoices are still not supported")

        self.invoices_box.append(invoice_status_page)

        new_invoice = Gtk.Button(css_classes=["pill","suggested-action"],
                label="New Invoice", halign=Gtk.Align.CENTER, margin_bottom=50)
        new_invoice.connect("clicked", self.make_new_invoice)
        self.invoices_box.append(new_invoice)

        info_page_status_page = Adw.StatusPage(title="Work in progress",
                icon_name="info-symbolic", hexpand=True, vexpand=True,
                description="Invoice info page")

        self.info_scrolled_window_product_custom.set_child(info_page_status_page)

    def make_new_invoice(self, btn):
        make_invoice_box = Gtk.Box(homogeneous=True)
        self.content_scrolled_window.set_child(make_invoice_box)

        list_box = Gtk.ListBox(selection_mode = 0, vexpand=True, margin_end=6)
        scrolled_window = Gtk.ScrolledWindow(margin_start=6, margin_top=6, margin_bottom=6, hexpand=True)
        scrolled_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled_window.set_child(list_box)
        box4 = Gtk.Box(orientation=1, spacing=6, margin_start=6, margin_end=6,
                margin_top=6, margin_bottom=6, css_classes=["card"])
        box4.append(scrolled_window)
        make_invoice_box.append(box4)

        invoice_options = ["Customer Name", "Customer code", "Issue Date", "Invoice Due"]

        for option in invoice_options:
            box2 = Gtk.Box(homogeneous=True, margin_end=4, margin_start=4)
            box2.append(Gtk.Label(label=option, xalign=0, hexpand=True))
            entry = Gtk.Entry(placeholder_text=_("Write here"),hexpand=True, margin_top=4,
                            margin_bottom=4)
            list_box.append(box2)
            box2.append(entry)

        box2 = Gtk.Box(margin_end=4, margin_start=4, orientation=1, height_request=300)
        box2.append(Gtk.Label(label="Items", xalign=0, hexpand=True, margin_top=4))

        self.invoice_items_model = Gio.ListStore(item_type=Item)

        invoice_items_column_view = Gtk.ColumnView(single_click_activate=False, reorderable=True,
                css_classes=["flat"], vexpand=True)

        tree_model = Gtk.TreeListModel.new(self.invoice_items_model, False, True, self.model_func)
        tree_sorter = Gtk.TreeListRowSorter.new(invoice_items_column_view.get_sorter())
        sorter_model = Gtk.SortListModel(model=tree_model, sorter=tree_sorter)

        self.invoice_selection_model = Gtk.SingleSelection.new(model=tree_model)
        #selection_model.connect("selection-changed", self.on_selection_changed)

        invoice_items_column_view.set_model(self.invoice_selection_model)

        for detail in self.details_names:
            self.add_column(detail[0], detail[1], detail[2], invoice_items_column_view)

        invoice_items_column_view_scrolled_window = Gtk.ScrolledWindow(margin_start=6, margin_top=6, margin_bottom=6, hexpand=True)
        invoice_items_column_view_scrolled_window.set_child(invoice_items_column_view)
        box2.append(invoice_items_column_view_scrolled_window)
        list_box.append(box2)

        box3 = Gtk.Box(spacing=6, margin_start=6, margin_end=6, homogeneous=True)
        cancel_button = Gtk.Button(label=_("Cancel"), hexpand=True, margin_top=6, margin_bottom=6)
        cancel_button.connect("clicked", self.show_invoice)
        add_button = Gtk.Button(label=_("Save"), hexpand=True, margin_top=6, margin_bottom=6, css_classes=["suggested-action"])
        #add_button.connect("clicked", self.edit_existing_item, list_box_add, item, add_item_window)
        box3.append(cancel_button)
        box3.append(add_button)
        box4.append(box3)

        #make_invoice_box.append(scrolled_window)

        items_scrolled_window = Gtk.ScrolledWindow(hexpand=True)
        items_scrolled_window.set_child(self.cv)
        #make_invoice_box.append(items_scrolled_window)

    def navigation_select_page(self, index):
        selected_row = self.sidebar_navigation_listBox.get_row_at_index(index)
        self.sidebar_navigation_listBox.select_row(selected_row)

        self.last_page = index

        if selected_row.get_child().get_label() == "Dashboard":
            self.show_dashboard()
        elif selected_row.get_child().get_label() == "Items":
            self.show_items()
            self.delete_filter_rows()
        elif selected_row.get_child().get_label() == "Products":
            self.show_products()
            #self.update_sidebar_product_info()
            self.delete_filter_rows()
        elif selected_row.get_child().get_label() == "Invoice":
            self.show_invoice()
        elif selected_row.get_child().get_label() == "Low Stock":
            self.show_low_stock()
            self.delete_filter_rows()
        elif selected_row.get_child().get_label() == "Out Of Stock":
            self.show_out_of_stock()
            self.delete_filter_rows()
        elif selected_row.get_child().get_label() == "Production":
            self.show_production()
            self.delete_filter_rows()

    def show_production(self):
        print("show_production")
        self.split_view.set_collapsed(False)
        self.content_headerbar.set_show_title_buttons(False)
        self.search_button_toggle.set_visible(False)
        self.search_revealer.set_reveal_child(False)
        self.item_info_revealer.set_reveal_child(False)
        self.action_bar_revealer.set_transition_duration(0)
        self.action_bar_revealer.set_reveal_child(False)
        self.action_bar_revealer.set_transition_duration(250)

        self.products_box = Gtk.Box(margin_start=10, margin_top=10, margin_bottom=10, margin_end=10)
        #self.content_scrolled_window.set_child(self.products_box)

        info_page_status_page = Adw.StatusPage(title="Work in progress",
                icon_name="info-symbolic", hexpand=True, vexpand=True,
                description="Production info page")

        wip_status_page = Adw.StatusPage(title="Work in progress",
                icon_name="build-alt-symbolic", hexpand=True, vexpand=True,
                description="Production is still not supported")

        self.info_scrolled_window_product_custom.set_child(info_page_status_page)
        self.content_scrolled_window.set_child(wip_status_page)
        #self.content_scrolled_window.set_child(self.products_cv)

    def show_low_stock(self):
        self.split_view.set_collapsed(False)
        self.content_headerbar.set_show_title_buttons(False)
        self.search_button_toggle.set_visible(True)
        self.column_visibility_button.set_visible(True)
        self.products_column_visibility_button.set_visible(False)
        self.search_revealer.set_reveal_child(self.search_button_toggle.get_active())

        self.content_scrolled_window.set_child(None)
        self.content_scrolled_window.set_child(self.cv)

        if self.settings.get_boolean("enable-horizontal-scrolling"):
            self.content_scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.action_bar_revealer.set_reveal_child(True)

        if self.selected_item != None:
            self.cv.get_model().select_item(self.selected_item, True)
        self.row_filter.changed(Gtk.FilterChange.DIFFERENT)
        self.selected_item = self.selection_model.get_selection().get_maximum()
        self.update_sidebar_item_info()

    def show_out_of_stock(self):
        self.split_view.set_collapsed(False)
        self.content_headerbar.set_show_title_buttons(False)
        self.search_button_toggle.set_visible(True)
        self.column_visibility_button.set_visible(True)
        self.products_column_visibility_button.set_visible(False)
        self.search_revealer.set_reveal_child(self.search_button_toggle.get_active())

        self.content_scrolled_window.set_child(None)
        self.content_scrolled_window.set_child(self.cv)

        if self.settings.get_boolean("enable-horizontal-scrolling"):
            self.content_scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.action_bar_revealer.set_reveal_child(True)


        if self.selected_item != None:
            self.cv.get_model().select_item(self.selected_item, True)
        self.row_filter.changed(Gtk.FilterChange.DIFFERENT)
        self.selected_item = self.selection_model.get_selection().get_maximum()
        self.update_sidebar_item_info()

    def show_dashboard(self):
        self.split_view.set_collapsed(True)
        self.content_headerbar.set_show_title_buttons(True)
        self.search_button_toggle.set_visible(False)
        self.search_revealer.set_reveal_child(False)
        self.content_scrolled_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.NEVER)
        self.content_scrolled_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.item_info_revealer.set_reveal_child(False)
        self.action_bar_revealer.set_transition_duration(0)
        self.action_bar_revealer.set_reveal_child(False)
        self.action_bar_revealer.set_transition_duration(250)
        self.dashboard_box = Gtk.FlowBox(margin_start=10, margin_top=10, margin_bottom=10, hexpand=True,
                margin_end=10, valign=Gtk.Align.START, selection_mode=Gtk.SelectionMode.NONE,
                max_children_per_line=4)
        self.content_scrolled_window.set_child(self.dashboard_box)

        info_page_status_page = Adw.StatusPage(title="Work in progress",
                icon_name="info-symbolic", hexpand=True, vexpand=True,
                description="Dashboard info page")

        self.info_scrolled_window_product_custom.set_child(info_page_status_page)

        items_widget = self.dashboard_simple_widget("Items", len(self.model))
        items_widget.connect("clicked", self.on_go_items_button_clicked)
        self.dashboard_box.append(items_widget)

        low_stock_widget = self.dashboard_simple_widget("Low Stock", self.get_low_stock())
        low_stock_widget.connect("clicked", self.on_go_to_low_stock_button_clicked)
        self.dashboard_box.append(low_stock_widget)

        out_of_stock_widget = self.dashboard_simple_widget("Out of Stock", self.get_out_of_stock())
        out_of_stock_widget.connect("clicked", self.on_go_to_out_of_stock_button_clicked)
        self.dashboard_box.append(out_of_stock_widget)

        self.dashboard_box.append(self.dashboard_simple_widget("Value", str(self.get_inventory_value()) + " €"))
        self.dashboard_box.append(self.dashboard_progress_widget("Items to 100", len(self.model), 100))

    def on_go_to_low_stock_button_clicked(self, btn):
        self.navigation_select_page(self.low_stock_index)

    def on_go_to_out_of_stock_button_clicked(self, btn):
        self.navigation_select_page(self.out_of_stock_index)

    def on_go_items_button_clicked(self, btn):
        self.navigation_select_page(self.items_index)

    def get_inventory_value(self):
        total = 0
        for i in range(len(self.model)):
            cost = self.model[i].item_cost
            stock = self.model[i].item_quantity
            if cost != None and stock != None:
                total += cost * stock
        return total

    def get_out_of_stock(self):
        out_of_stock_items_n = 0
        for item in self.model:
            stock = item.item_quantity
            if stock == None:
                out_of_stock_items_n += 1
                continue
            if stock == 0:
                out_of_stock_items_n += 1
        return out_of_stock_items_n

    def get_low_stock(self):
        low_stock_items_n = 0
        for item in self.model:
            stock = item.item_quantity
            threshold = item.item_low_stock
            if stock == None or threshold == None:
                continue
            if stock <= threshold:
                low_stock_items_n += 1
        return low_stock_items_n

    def add_dashboard_widget(self, name, x, y, width, height):
        pass

    def dashboard_big_text_widget(self, info_name, info):
        box = Gtk.Box(css_classes=["card"], margin_start=6, margin_end=6,
                margin_top=6, margin_bottom=6, hexpand=True, spacing = 6, height_request=100)
        box.append(Gtk.Image.new_from_icon_name("package-x-generic-symbolic"))
        box2 = Gtk.Box(orientation=1)
        box.append(box2)
        box2.append(Gtk.Label(label=info_name, hexpand=True, xalign=0, margin_start=10, margin_top=10, margin_bottom=10))
        box2.append(Gtk.Label(label=info, hexpand=True, xalign=1, margin_end=10))
        return box

    def dashboard_simple_widget(self, info_name, info):
        button = Gtk.Button(css_classes=["card"], margin_start=6, margin_end=6, vexpand=True,
                margin_top=6, margin_bottom=6, hexpand=True, height_request=100)
        box = Gtk.Box()
        button.set_child(box)
        image = Gtk.Image(icon_name="package-x-generic-symbolic", pixel_size=40, margin_start=30)

        box.append(image)
        box2 = Gtk.Box(orientation=1, margin_end=6)
        box.append(box2)
        box2.append(Gtk.Label(css_classes=["title-2"], label=info_name, hexpand=True, margin_start=10, margin_top=10, margin_bottom=10))
        box2.append(Gtk.Label(label=info, hexpand=True, margin_end=10, vexpand=True))
        return button
        
    def dashboard_progress_widget(self, info_name, info, total):
        box = Gtk.Box(css_classes=["card"], margin_start=6, margin_end=6,
                margin_top=6, margin_bottom=6, hexpand=True, spacing = 6, orientation=1, height_request=100)
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
            



