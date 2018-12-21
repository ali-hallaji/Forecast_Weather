#!/usr/bin/env python
# -*- coding: utf-8 -*-
import gtk

from db_handler import get_cursor


class ListLocation():
    def __init__(self):
        self.window = gtk.Window()
        self.window.set_title("List Location")
        self.window.set_size_request(300, 200)
        self.window.set_position(gtk.WIN_POS_CENTER)
        self.create_widgets()
        self.window.show_all()

    def create_widgets(self):
        vbox = gtk.VBox(False, 8)

        sw = gtk.ScrolledWindow()
        sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)

        vbox.pack_start(sw, True, True, 0)

        store = self.location_store_model()

        treeView = gtk.TreeView(store)
        treeView.connect("row-activated", self.on_activated)
        treeView.set_rules_hint(True)
        sw.add(treeView)

        self.create_columns(treeView)
        self.statusbar = gtk.Statusbar()

        vbox.pack_start(self.statusbar, False, False, 0)

        self.window.add(vbox)
        self.window.show_all()

    def create_columns(self, treeView):
        rendererText = gtk.CellRendererText()
        column = gtk.TreeViewColumn("Row", rendererText, text=0)
        column.set_sort_column_id(0)
        treeView.append_column(column)

        rendererText = gtk.CellRendererText()
        column = gtk.TreeViewColumn("Location", rendererText, text=1)
        column.set_sort_column_id(1)
        treeView.append_column(column)

        rendererText = gtk.CellRendererText()
        column = gtk.TreeViewColumn("Created Date", rendererText, text=2)
        column.set_sort_column_id(2)
        treeView.append_column(column)


    def on_activated(self, widget, row, col):
        model = widget.get_model()
        text = str(model[row][0]) + ", " + model[row][1] + ", " + model[row][2]
        self.statusbar.push(0, text)

    def on_destroy(self, widget):
        self.window.hide()

    def location_store_model(self):
        store = gtk.ListStore(int, str, str)

        counter = 1
        for location in get_cursor('locations'):
            store.append(
                [
                    counter,
                    location['location'],
                    location['created_date'].strftime('%Y-%m-%d %H:%M:%S')
                ]
            )
            counter += 1

        return store

