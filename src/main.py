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

from gi.repository import Gtk, Gio, Adw
from .window import InventarioWindow

from gettext import gettext as _
import locale
from os import path
from os.path import abspath, dirname, join, realpath
import os

class InventarioApplication(Adw.Application):
    """The main application singleton class."""

    def __init__(self):
        super().__init__(application_id='io.github.nokse22.inventario',
                         flags=Gio.ApplicationFlags.DEFAULT_FLAGS)
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
        self.win.item_info_revealer.set_reveal_child(False)
        self.win.settings.set_string("last-inventory-path", "")

    def on_save_action(self, widget=None, _=None):
        path = self.win.settings.get_string("last-inventory-path")
        self.win.save_inventory_file(path)

    def on_save_as_action(self, widget, _):
        self.win.save_inventory_file_as()

    def on_import_action(self, widget, _):
        pass

    def on_open_inventory_action(self, widget, _):
        self.win.open_file_chooser()

    def do_activate(self):
        """Called when the application is activated.

        We raise the application's main window, creating it if
        necessary.
        """
        self.win = self.props.active_window
        if not self.win:
            self.win = InventarioWindow(application=self)
        self.win.present()

        self.win.open_file_on_startup()
        self.win.update_sidebar_item_info()

    def on_show():
        print('Doing stuff.')
        sleep(3)
        print('Done stuff.')

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

        settingsPage = Adw.PreferencesPage(title="Generals")
        settingsPage.set_icon_name("applications-system-symbolic")
        pref.add(settingsPage)

        self.general_group = Adw.PreferencesGroup(title=("General settings"))
        settingsPage.add(self.general_group)

        row = Adw.ActionRow(title=("Remember window size"))
        switch = Gtk.Switch(valign=Gtk.Align.CENTER)
        row.add_suffix(switch)
        self.win.settings.bind("window-save", switch, 'active', Gio.SettingsBindFlags.DEFAULT)
        self.general_group.add(row)

        row = Adw.ActionRow(title=("Open last inventory on startup"))
        switch = Gtk.Switch(valign=Gtk.Align.CENTER)
        row.add_suffix(switch)
        self.win.settings.bind("open-last-on-start", switch, 'active', Gio.SettingsBindFlags.DEFAULT)
        self.general_group.add(row)

        row = Adw.ActionRow(title=("Enable horizontal scrolling"))
        switch = Gtk.Switch(valign=Gtk.Align.CENTER)
        row.add_suffix(switch)
        self.win.settings.bind("enable-horizontal-scrolling", switch, 'active', Gio.SettingsBindFlags.DEFAULT)
        self.general_group.add(row)

        row = Adw.ActionRow(title=("Enable rows separators"), subtitle=("It will take effect at the next start"))
        switch = Gtk.Switch(valign=Gtk.Align.CENTER)
        row.add_suffix(switch)
        self.win.settings.bind("enable-rows-separators", switch, 'active', Gio.SettingsBindFlags.DEFAULT)
        self.general_group.add(row)

        row = Adw.ActionRow(title=("Enable columns separators"), subtitle=("It will take effect at the next start"))
        switch = Gtk.Switch(valign=Gtk.Align.CENTER)
        row.add_suffix(switch)
        self.win.settings.bind("enable-columns-separators", switch, 'active', Gio.SettingsBindFlags.DEFAULT)
        self.general_group.add(row)

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
