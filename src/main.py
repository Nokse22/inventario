# main.py
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

import sys
import gi, os

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Gio, Adw, Gdk, GLib
from .window import InventarioWindow

import threading
import gettext
import locale
from os import path
from os.path import abspath, dirname, join, realpath
import os
import time

class InventarioApplication(Adw.Application):
    """The main application singleton class."""

    def __init__(self):
        super().__init__(application_id='io.github.nokse22.inventario',
                         flags=Gio.ApplicationFlags.DEFAULT_FLAGS)

        css = '''
        .electronics{
            color: #f6f5f4;
            font-weight: bold;
            background-color: #1c71d8;
            border-radius: 4px;
        }
        .mechanical{
            color: #f6f5f4;
            font-weight: bold;
            background-color: #26a269;
            border-radius: 4px;
        }
        .consumable{
            color: #f6f5f4;
            font-weight: bold;
            background-color: #b5835a;
            border-radius: 4px;
        }
        '''
        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(css, -1)
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        self.create_action('quit', lambda *_: self.quit(), ['<primary>q'])
        self.create_action('about', self.on_about_action)
        self.create_action('preferences', self.on_preferences_action, ['<primary>comma'])

        self.create_action('new-inventory', self.on_new_inventory_action, ['<primary>n'])
        self.create_action('save', self.on_save_action, ['<primary>s'])
        self.create_action('save-as', self.on_save_as_action, ['<primary><shift>s'])
        self.create_action('import', self.on_import_action, ['<primary>i'])
        self.create_action('open-inventory', self.on_open_inventory_action, ['<primary>o'])

    def on_new_inventory_action(self, widget, _):
        path = self.win.settings.get_string("last-inventory-path")
        self.win.save_inventory_file(path)
        self.win.model.remove_all()
        self.win.products_model.remove_all()
        self.win.item_info_revealer.set_reveal_child(False)
        self.win.settings.set_string("last-inventory-path", "")

    def on_save_action(self, widget=None, _=None):
        path = self.win.settings.get_string("last-inventory-path")
        self.win.save_inventory_file(path)

    def on_save_as_action(self, widget, _):
        self.win.save_inventory_file_as()

    def on_import_action(self, widget, _):
        self.win.open_file_to_import()

    def on_open_inventory_action(self, widget, _):
        self.win.open_file_chooser()

    def do_activate(self):
        """Called when the application is activated.

        We raise the application's main window, creating it if
        necessary.
        """
        self.win = self.props.active_window
        if not self.win:
            start = time.time()
            self.win = InventarioWindow(application=self)
            end = time.time()
            print(end - start)
        self.win.present()

        start = time.time()
        self.win.open_file_on_startup()
        end = time.time()
        print(end - start)

        self.win.navigation_select_page(self.win.last_page)

        GLib.timeout_add(self.win.settings.get_int("autosave-delay") * 1000, self.win.autosave)

    def on_about_action(self, widget, _):
        """Callback for the app.about action."""
        about = Adw.AboutWindow(transient_for=self.props.active_window,
                                application_name='Inventario',
                                application_icon='io.github.nokse22.inventario',
                                developer_name='Nokse',
                                website='https://github.com/Nokse22/inventario',
                                issue_url='https://github.com/Nokse22/inventario/issues',
                                version='0.1.0',
                                developers=['Nokse'],
                                copyright='© 2023 Nokse')
        about.present()

    def on_preferences_action(self, widget, _):
        """Callback for the app.preferences action."""

        pref = Adw.PreferencesWindow()
        pref.set_modal(True)
        pref.set_transient_for(self.props.active_window)

        settingsPage = Adw.PreferencesPage(title=gettext.gettext("Generals"))
        settingsPage.set_icon_name("applications-system-symbolic")
        pref.add(settingsPage)

        self.general_group = Adw.PreferencesGroup(title=gettext.gettext("General settings"))
        settingsPage.add(self.general_group)

        row = Adw.ActionRow(title=gettext.gettext("Remember window size"))
        switch = Gtk.Switch(valign=Gtk.Align.CENTER)
        row.add_suffix(switch)
        self.win.settings.bind("window-save", switch, 'active', Gio.SettingsBindFlags.DEFAULT)
        self.general_group.add(row)

        row = Adw.ActionRow(title=gettext.gettext("Open last inventory on startup"))
        switch = Gtk.Switch(valign=Gtk.Align.CENTER)
        row.add_suffix(switch)
        self.win.settings.bind("open-last-on-start", switch, 'active', Gio.SettingsBindFlags.DEFAULT)
        self.general_group.add(row)

        row = Adw.ActionRow(title=gettext.gettext("Enable rows separators"), subtitle=gettext.gettext("It will take effect at the next start"))
        switch = Gtk.Switch(valign=Gtk.Align.CENTER)
        row.add_suffix(switch)
        self.win.settings.bind("enable-rows-separators", switch, 'active', Gio.SettingsBindFlags.DEFAULT)
        self.general_group.add(row)

        row = Adw.ActionRow(title=gettext.gettext("Enable columns separators"), subtitle=gettext.gettext("It will take effect at the next start"))
        switch = Gtk.Switch(valign=Gtk.Align.CENTER)
        row.add_suffix(switch)
        self.win.settings.bind("enable-columns-separators", switch, 'active', Gio.SettingsBindFlags.DEFAULT)
        self.general_group.add(row)

        row = Adw.ActionRow(title=gettext.gettext("Enable coloured categories"), subtitle=gettext.gettext("It will take effect after changing page"))
        switch = Gtk.Switch(valign=Gtk.Align.CENTER)
        row.add_suffix(switch)
        self.win.settings.bind("enable-coloured-categories", switch, 'active', Gio.SettingsBindFlags.DEFAULT)
        self.general_group.add(row)

        currency_symbols = ["€", "$", "£", "¥", "C$", "A$", "Fr", "¥", "₹", "₽", "₩", "R$", "$ or Mex$", "R", "NZ$"]
        row = Adw.ComboRow(title=("Currency"))
        drop_down = Gtk.DropDown.new_from_strings(currency_symbols) #valign=Gtk.Align.CENTER
        list_store = Gtk.StringList()
        for symbol in currency_symbols:
            list_store.append(symbol)
        row.set_model(list_store)
        #row.add_suffix(drop_down)
        #self.win.settings.bind("currency", row, 'selected', Gio.SettingsBindFlags.DEFAULT)
        self.general_group.add(row)

        group = Adw.PreferencesGroup(title=gettext.gettext("Save settings"))
        settingsPage.add(group)

        row = Adw.ActionRow(title=gettext.gettext("Enable autosave"))
        switch = Gtk.Switch(valign=Gtk.Align.CENTER)
        row.add_suffix(switch)
        self.win.settings.bind("automatic-save", switch, 'active', Gio.SettingsBindFlags.DEFAULT)
        group.add(row)

        row = Adw.SpinRow(title=gettext.gettext("Autosave every (seconds)"), subtitle=gettext.gettext("It will take effect after restarting the app"))
        row.set_range(1, 10000)
        row.get_adjustment().set_step_increment(1)
        self.win.settings.bind("autosave-delay", row, 'value', Gio.SettingsBindFlags.DEFAULT)
        group.add(row)

        pref.present()

    def boolean_row(self, name, value, callback):
        row = Adw.ActionRow(title=name)
        rowSwitch = Gtk.Switch(valign = Gtk.Align.CENTER)
        rowSwitch.set_active(value)
        row.add_suffix(rowSwitch)
        return row

    def create_action(self, name, callback, shortcuts=None):
        """Add an application action.

        Args:
            name: the name of the action
            callback: the function to be called when the action is
              activated
            shortcuts: an optional list of accelerators
        """
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)

    def do_shutdown(self):
        os.chdir(os.path.expanduser("~"))
        settings = Gio.Settings.new('io.github.nokse22.inventario')
        settings.set_int("last-page", self.win.last_page)
        self.on_save_action()
        Gtk.Application.do_shutdown(self)

def main(version):
    """The application's entry point."""
    app = InventarioApplication()
    return app.run(sys.argv)
