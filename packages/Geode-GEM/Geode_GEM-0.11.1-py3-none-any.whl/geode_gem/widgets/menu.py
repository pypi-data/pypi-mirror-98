# ------------------------------------------------------------------------------
#  Copyleft 2015-2021  PacMiam
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
# ------------------------------------------------------------------------------

# Geode
from geode_gem.widgets.common import GeodeGtkCommon

# GObject
from gi.repository import Gtk


# ------------------------------------------------------------------------------
#   Class
# ------------------------------------------------------------------------------

class CommonMenuItem(GeodeGtkCommon):

    __setters__ = {
        "set_use_underline": True,
    }

    def __init__(self, subclass, title, *args, **kwargs):
        """ Constructor

        Parameters
        ----------
        subclass : Gtk.MenuItem
            Subclass widget type
        title : str
            Menu item label
        """

        GeodeGtkCommon.__init__(self, subclass, **kwargs)

        # Properties
        self.set_label(title)

        if args:
            submenu = GeodeGtkMenu(*args)

            self.append_widget(submenu)
            self.set_submenu(submenu)


class GeodeGtkMenu(GeodeGtkCommon, Gtk.Menu):

    def __init__(self, *args, **kwargs):
        """ Constructor
        """

        GeodeGtkCommon.__init__(self, Gtk.Menu, **kwargs)

        for child in args:
            self.append(child)

    def append(self, child):
        """ Append a new child at the end of menu list

        Parameters
        ----------
        child : Gtk.MenuItem
            New menu item to append
        """

        # Generate a dynamic name for Gtk.SeparatorMenuItem
        if child is None:
            child = Gtk.SeparatorMenuItem.new()

        elif isinstance(child, Gtk.RadioMenuItem) and child.group is not None:
            child.join_group(self.get_widget(child.group))

        self.append_widget(child)

        super().append(child)

    def remove(self, child):
        """ Remove a specific widget from menu list

        Parameters
        ----------
        child : Gtk.MenuItem
            Menu item to remove
        """

        if hasattr(child, "identifier") and self.has_widget(child.identifier):
            del self.inner_widgets[child.identifier]

        super().remove(child)

    def clear(self):
        """ Remove all items from menu list
        """

        for child in self.get_children():
            self.remove(child)


class GeodeGtkMenuItem(CommonMenuItem, Gtk.MenuItem):

    def __init__(self, *args, **kwargs):
        """ See geode_gem.ui.widgets.menu.CommonMenuItem
        """

        CommonMenuItem.__init__(self, Gtk.MenuItem, *args, **kwargs)


class GeodeGtkCheckMenuItem(CommonMenuItem, Gtk.CheckMenuItem):

    def __init__(self, *args, **kwargs):
        """ See geode_gem.ui.widgets.menu.CommonMenuItem
        """

        CommonMenuItem.__init__(self, Gtk.CheckMenuItem, *args, **kwargs)


class GeodeGtkRadioMenuItem(CommonMenuItem, Gtk.RadioMenuItem):

    def __init__(self, *args, **kwargs):
        """ See geode_gem.ui.widgets.menu.CommonMenuItem
        """

        CommonMenuItem.__init__(self, Gtk.RadioMenuItem, *args, **kwargs)

        self.group = kwargs.get("group", None)
