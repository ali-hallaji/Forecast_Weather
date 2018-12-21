#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "Ali Hallaji"
__copyright__ = "Copyright 2k18, The Weather Forecast Application"
__credits__ = ["Moonshot"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Ali Hallaji"
__email__ = "Ali.Hallaji1@gmail.com"
__status__ = "Test"
import os
import gtk

from db_handler import get_cursor
from add_location import AddLocation
from list_location import ListLocation
from weather_handler import update_data
from weather_handler import insert_data
from history_chart import HistoryChart
from details import Details


class Application():
    def __init__(self):
        self.remove_info = False
        self.window = gtk.Window()
        self.window.set_title("Moonshot Weather Forecast")
        self.window.set_icon_from_file('icons/Weather_icons.png')
        self.window.connect("key-press-event", self._key_press_event)
        self.window.set_position(gtk.WIN_POS_CENTER)
        self.window.connect("destroy", gtk.main_quit)
        self.window.set_default_size(400, 350)
        # self.window.set_decorated(False)
        self.create_widgets()
        self.window.show_all()
        gtk.main()

    def create_widgets(self):
        self.vbox = gtk.VBox(spacing=0)
        self.hbox_combo = gtk.HBox(spacing=0)
        self.hbox_note = gtk.HBox(spacing=0)
        self.hbox_info = gtk.HBox(spacing=0)
        self.hbox_inner1 = gtk.HBox(spacing=0)
        self.hbox_inner2 = gtk.HBox(spacing=0)
        self.hbox_mood_pic = gtk.HBox(spacing=0)
        self.hbox_up_design = gtk.HBox(spacing=0)
        self.hbox_end_design = gtk.HBox(spacing=0)
        self.hbox_chart_detail = gtk.HBox(spacing=0)

        toolbar = gtk.Toolbar()
        toolbar.set_style(gtk.TOOLBAR_ICONS)
        toolbar.set_orientation(gtk.ORIENTATION_HORIZONTAL)

        quit_btn = gtk.ToolButton(gtk.STOCK_QUIT)
        quit_btn.set_tooltip_text('Exit')
        quit_btn.connect("clicked", self.exit_func)

        sep1 = gtk.SeparatorToolItem()

        add_location_btn = gtk.ToolButton(gtk.STOCK_NEW)
        add_location_btn.connect("clicked", self.add_location)
        add_location_btn.set_tooltip_text('Add Location')

        list_location_btn = gtk.ToolButton(gtk.STOCK_PRINT_PREVIEW)
        list_location_btn.connect("clicked", self.list_location)
        list_location_btn.set_tooltip_text('List Location')

        refresh_btn = gtk.ToolButton(gtk.STOCK_REFRESH)
        refresh_btn.connect("clicked", self.refresh_data)
        refresh_btn.set_tooltip_text('Refresh Data')

        sep2 = gtk.SeparatorToolItem()

        info_btn = gtk.ToolButton(gtk.STOCK_INFO)
        info_btn.set_tooltip_text('Help')
        info_btn.connect("clicked", self.show_help)

        toolbar.insert(quit_btn, 0)
        toolbar.insert(sep1, 1)
        toolbar.insert(add_location_btn, 2)
        toolbar.insert(list_location_btn, 3)
        toolbar.insert(refresh_btn, 4)
        toolbar.insert(sep2, 5)
        toolbar.insert(info_btn, 6)

        select_label = gtk.Label("Select a location")
        select_label.set_justify(gtk.JUSTIFY_CENTER)

        self.hbox_up_design.pack_start(gtk.HSeparator())
        self.hbox_up_design.pack_start(gtk.Label('***'))
        self.hbox_up_design.pack_start(gtk.HSeparator())

        self.hbox_combo.pack_start(select_label)
        self.hbox_combo.pack_start(self.main_combo())

        msg = "Note: Please select a location from the Combobox and if \n"
        msg += "there weren't any location please add a location from 'Add \n"
        msg += "Location' icon on the toolbar"

        self.note_label = gtk.Label(msg)
        self.note_label.set_justify(gtk.JUSTIFY_CENTER)
        self.hbox_note.pack_start(self.note_label)

        self.vbox_inner1 = gtk.VBox(spacing=0)
        self.vbox_inner2 = gtk.VBox(spacing=0)

        self.initial_show_data()

        self.hbox_end_design.pack_start(gtk.HSeparator())
        self.hbox_end_design.pack_start(gtk.Label('***'))
        self.hbox_end_design.pack_start(gtk.HSeparator())

        self.mood = gtk.Image()
        self.hbox_mood_pic.pack_start(self.mood)

        self.hbox_info.pack_start(self.vbox_inner1)
        self.hbox_info.pack_start(self.vbox_inner2)

        self.details_btn = gtk.Button('Details')
        self.update_btn = gtk.Button('Update')
        self.history_btn = gtk.Button('History')

        self.details_btn.set_sensitive(False)
        self.update_btn.set_sensitive(False)
        self.history_btn.set_sensitive(False)

        self.history_btn.connect("clicked", self.make_chart)
        self.update_btn.connect("clicked", self.single_update)
        self.details_btn.connect("clicked", self.details)

        self.hbox_chart_detail.pack_start(self.details_btn)
        self.hbox_chart_detail.pack_start(self.update_btn)
        self.hbox_chart_detail.pack_start(self.history_btn)

        self.vbox.pack_start(toolbar, expand=False, fill=False, padding=0)
        self.vbox.pack_start(gtk.HSeparator())
        self.vbox.pack_start(self.hbox_combo, True, True, 0)
        self.vbox.pack_start(self.hbox_up_design)
        self.vbox.pack_start(self.hbox_note, True, False, 0)
        self.vbox.pack_start(self.hbox_mood_pic, True, True, 0)
        self.vbox.pack_start(self.hbox_info, True, True, 0)
        self.vbox.pack_start(self.hbox_end_design)
        self.vbox.pack_start(self.hbox_chart_detail, True, True, 0)

        self.window.add(self.vbox)

    def initial_show_data(self):
        self.name_label = gtk.Label("Name: -")
        self.temp_label = gtk.Label("Temp: -")
        self.text_label = gtk.Label("Mood: -")
        self.high_label = gtk.Label("High: -")
        self.low_label = gtk.Label("Low: -")
        self.country_name_label = gtk.Label("Country: -")

        self.vbox_inner1.pack_start(self.name_label)
        self.vbox_inner1.pack_start(self.temp_label)
        self.vbox_inner1.pack_start(self.text_label)
        self.vbox_inner2.pack_start(self.high_label)
        self.vbox_inner2.pack_start(self.low_label)
        self.vbox_inner2.pack_start(self.country_name_label)

    def make_chart(self, widget, data=None):
        HistoryChart(self.selected_combo_name)

    def single_update(self, widget):
        self.refresh_gui()
        insert_data(self.selected_combo_name)

    def add_location(self, widget):
        AddLocation(self)

    def details(self, widget):
        Details(self.selected_combo_name)

    def list_location(self, widget):
        ListLocation()

    def refresh_gui(self):
      while gtk.events_pending():
          gtk.main_iteration_do(block=False)

    def refresh_data(self, widget):
        update_data()

    def show_help(self, widget):
        dialog = gtk.Dialog()
        info = gtk.Label('Help')
        image = gtk.Image()
        image.set_from_file('icons/moonshop_forecast.png')
        dialog.vbox.pack_start(image)
        dialog.show_all()

    def show_data(self, name):
        if not self.remove_info:
            self.vbox.remove(self.hbox_note)
            self.remove_info = True

        data = get_cursor('weather_data')(location_name=name)[0]
        self.name_label.set_text("Location Name: " + data['location_name'])
        self.temp_label.set_text("Temprature: " + data['temp'])
        self.text_label.set_text("Mood: " + data['text'])
        self.high_label.set_text("High: " + data['high'])
        self.low_label.set_text("Low: " + data['low'])
        self.country_name_label.set_text("Country: " + data['country_name'])

        pixbuf = gtk.gdk.pixbuf_new_from_file("icons/{}.png".format(data['code'].lower()))
        pixbuf = pixbuf.scale_simple(250, 250, gtk.gdk.INTERP_BILINEAR)
        self.mood.set_from_pixbuf(pixbuf)
        # self.mood.set_from_file("icons/{}.png".format(data['code'].lower()))

        self.details_btn.set_sensitive(True)
        self.update_btn.set_sensitive(True)
        self.history_btn.set_sensitive(True)

    def on_changed_combo(self, combo):
        tree_iter = combo.get_active_iter()
        if tree_iter is not None:
            model = combo.get_model()
            name = model[tree_iter][0]
            if name != '-----':
                self.show_data(name)
                self.selected_combo_name = name

    def main_combo(self, update=False):
        self.store = gtk.ListStore(str)
        if not update:
            self.cb = gtk.ComboBox()
            cell = gtk.CellRendererText()
            self.cb.pack_start(cell)
            self.cb.add_attribute(cell, 'text', 0)
            self.cb.connect("changed", self.on_changed_combo)

        self.cb.set_model(self.store)
        self.store.append(['-----'])
        for location in get_cursor('locations'):
            self.store.append([location['location']])

        self.cb.set_active(0)
        return self.cb

    def _key_press_event(self, widget, event):
        keyval = event.keyval
        keyval_name = gtk.gdk.keyval_name(keyval)

    def exit_func(self, widget, callback_data=None):
        self.window.destroy()
        gtk.main_quit()
        return

if __name__ == "__main__":
    app = Application()
