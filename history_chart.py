#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import gtk
import json
import webkit

from db_handler import get_cursor


class HistoryChart():
    def __init__(self, name):
        self.pwd = os.path.dirname(os.path.abspath(__file__))
        self.make_data(name, self.pwd)
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title("History Chart")
        self.window.set_size_request(550, 400)
        self.window.set_position(gtk.WIN_POS_CENTER)
        self.create_widgets()
        self.window.show_all()

    def make_data(self, name, pwd):
        cursor = get_cursor('weather_data')
        data = cursor(location_name=name)[0]['history']
        label = []
        out_data = []
        for item in data:
            label.append(item[1])
            out_data.append(item[0])
        name += " History Chart"
        all = {'out_labels': label, 'out_data': out_data, 'name': name}

        path = pwd + "/web/data.json"
        _file = open(path, "w")
        _file.write("all={}".format(json.dumps(all)))
        _file.close()

    def create_widgets(self):
        vbox = gtk.VBox(spacing=0)

        view = webkit.WebView()

        sw = gtk.ScrolledWindow()

        sw.add(view)
        view.open("file:///{}/web/chart.html".format(self.pwd))

        vbox.pack_start(sw)
        self.window.add(vbox)
        self.window.show_all()

    def on_destroy(self, widget):
        self.window.destroy()
        self.window.hide()
        return
