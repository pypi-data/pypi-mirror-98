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

# GObject
from gi.repository import Gtk, Pango


# ------------------------------------------------------------------------------
#   Class
# ------------------------------------------------------------------------------

class ListBoxItem(Gtk.ListBoxRow):

    def __init__(self):
        """ Constructor
        """

        Gtk.ListBoxRow.__init__(self)

        # ------------------------------------
        #   Initialize variables
        # ------------------------------------

        self.__widget = None

        # ------------------------------------
        #   Prepare interface
        # ------------------------------------

        # Init widgets
        self.__init_widgets()

        # Init packing
        self.__init_packing()

    def __init_widgets(self):
        """ Initialize interface widgets
        """

        # ------------------------------------
        #   Grids
        # ------------------------------------

        self.grid = Gtk.Box()
        self.grid_labels = Gtk.Box()

        # Properties
        self.grid.set_homogeneous(False)
        self.grid.set_border_width(6)
        self.grid.set_spacing(12)

        self.grid_labels.set_orientation(Gtk.Orientation.VERTICAL)
        self.grid_labels.set_homogeneous(False)
        self.grid_labels.set_spacing(2)

        # ------------------------------------
        #   Labels
        # ------------------------------------

        self.label_title = Gtk.Label()

        self.label_description = Gtk.Label()

        # Properties
        self.label_title.set_line_wrap(True)
        self.label_title.set_halign(Gtk.Align.START)
        self.label_title.set_justify(Gtk.Justification.FILL)
        self.label_title.set_line_wrap_mode(Pango.WrapMode.WORD_CHAR)

        self.label_description.set_hexpand(True)
        self.label_description.set_line_wrap(True)
        self.label_description.set_use_markup(True)
        self.label_description.set_no_show_all(True)
        self.label_description.set_halign(Gtk.Align.START)
        self.label_description.set_valign(Gtk.Align.START)
        self.label_description.set_justify(Gtk.Justification.FILL)
        self.label_description.set_line_wrap_mode(Pango.WrapMode.WORD_CHAR)
        self.label_description.get_style_context().add_class(
            Gtk.STYLE_CLASS_DIM_LABEL)

    def __init_packing(self):
        """ Initialize widgets packing in main window
        """

        self.add(self.grid)

        self.grid.pack_start(self.grid_labels, True, True, 0)

        self.grid_labels.pack_start(self.label_title, True, True, 0)
        self.grid_labels.pack_start(self.label_description, True, True, 0)

    @staticmethod
    def new(text):
        """ Generate a new ListBoxItem with a specific label

        Parameters
        ----------
        text : str
            Label text
        """

        row = ListBoxItem()
        row.set_option_label(text)

        return row

    def set_option_label(self, text):
        """ Set the option label text

        Parameters
        ----------
        text : str
            Label text
        """

        self.label_title.set_text(text)

    def get_option_label(self):
        """ Retrieve the option label text

        Returns
        -------
        str
            Label text
        """

        return self.label_title.get_text()

    def set_description_label(self, text):
        """ Set the description label text

        Parameters
        ----------
        text : str
            Label text
        """

        if len(text) > 0:
            self.label_description.set_markup(
                "<span size=\"small\">%s</span>" % text)

            self.label_title.set_valign(Gtk.Align.END)

        else:
            self.label_title.set_valign(Gtk.Align.CENTER)

        self.label_description.set_visible(len(text) > 0)

    def set_widget(self, widget):
        """ Set a new internal widget

        Parameters
        ----------
        widget : Gtk.Widget
            Internal widget to set
        """

        # Remove previous widget
        if self.__widget is not None:
            self.grid.remove(self.__widget)

        # Add new widget
        if widget is not None:
            widget.set_valign(Gtk.Align.CENTER)

            if type(widget) in (Gtk.Switch, Gtk.Button, Gtk.SpinButton,
                                Gtk.Image, Gtk.MenuButton):
                widget.set_halign(Gtk.Align.END)
                widget.set_hexpand(False)

                self.grid.set_homogeneous(False)

                self.grid.pack_start(widget, False, False, 0)

            else:
                widget.set_halign(Gtk.Align.FILL)
                widget.set_hexpand(True)

                self.grid.set_homogeneous(True)

                self.grid.pack_start(widget, True, True, 0)

        self.__widget = widget

    def get_widget(self):
        """ Retrieve internal widget

        Returns
        -------
        Gtk.Widget
            Internal widget
        """

        return self.__widget


class ScrolledListBox(Gtk.ScrolledWindow):

    def __init__(self):
        """ Constructor
        """

        Gtk.ScrolledWindow.__init__(self)

        # ----------------------------------------
        #   Prepare interface
        # ----------------------------------------

        # Init widgets
        self.__init_widgets()

        # Init packing
        self.__init_packing()

    def __init_widgets(self):
        """ Initialize interface widgets
        """

        self.set_propagate_natural_height(True)

        # ----------------------------------------
        #   Games list
        # ----------------------------------------

        self.listbox = Gtk.ListBox()

        # Properties
        self.listbox.set_activate_on_single_click(True)
        self.listbox.set_selection_mode(Gtk.SelectionMode.NONE)

    def __init_packing(self):
        """ Initialize widgets packing in main window
        """

        self.add(self.listbox)
