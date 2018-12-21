#!/usr/bin/env python
# -*- coding: utf-8 -*-
import gtk

from db_handler import get_cursor
from weather_handler import insert_data


class AddLocation():
    def __init__(self, parent):
        self.window = gtk.Window()
        self.window.set_position(gtk.WIN_POS_CENTER)
        self.window.set_title("Add Location")
        self.window.connect("key-press-event", self._key_press_event)
        self.parent = parent
        self.create_widgets()
        self.window.show_all()

    def create_widgets(self):
        self.vbox = gtk.VBox(spacing=20)
        self.hbox_1 = gtk.HBox(spacing=20)
        self.label_city = gtk.Label("Location Name")
        self.entry_location_name = gtk.Entry()
        self.entry_location_name.set_max_length(50)
        self.hbox_1.pack_start(self.label_city)
        self.hbox_1.pack_start(self.entry_location_name)
        self.hbox_2 = gtk.HBox(spacing=20)

        insert_btn = gtk.Button("Insert")
        insert_btn.connect("clicked", self.insert_signal)
        cancel_btn = gtk.Button("Cancel")
        cancel_btn.connect("clicked", self.on_destroy)

        self.hbox_2.pack_start(insert_btn)
        self.hbox_2.pack_start(cancel_btn)

        self.vbox.pack_start(self.hbox_1)
        self.vbox.pack_start(self.hbox_2)

        self.window.add(self.vbox)

    def _key_press_event(self, widget, event):
        keyval = event.keyval
        keyval_name = gtk.gdk.keyval_name(keyval)

        if keyval_name == 'Return':
            self.insert_signal(widget)
        elif keyval_name == 'Escape':
            self.on_destroy(widget)

    def on_destroy(self, widget):
        self.window.hide()

    def insert_signal(self, widget, callback_data=True):
        cursor = get_cursor('locations')
        location_name = self.entry_location_name.get_text()

        if not location_name:
            md = gtk.MessageDialog(None,
                gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_ERROR,
                gtk.BUTTONS_CLOSE, "Please enter your location name!")
            md.run()
            md.destroy()
            return

        result = insert_data(location_name.title())
        if result == 'Invalid Name!':
            md = gtk.MessageDialog(None,
                gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_ERROR,
                gtk.BUTTONS_CLOSE, "Please enter valid location name!")
            md.run()
            md.destroy()
            return

        md = gtk.MessageDialog(None,
            gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO,
            gtk.BUTTONS_CLOSE, "Your location inserted successfuly.")
        md.run()
        md.destroy()

        self.parent.main_combo(True)
        self.window.hide()

