#!/usr/bin/env python
# -*- coding: utf-8 -*-
import gtk

from db_handler import get_cursor


class Details():
    def __init__(self, name):
        self.name = name
        self.window = gtk.Window()
        self.window.set_title("Details")
        self.window.set_size_request(350, 400)
        self.window.set_position(gtk.WIN_POS_CENTER)
        self.ready_data()
        self.create_widgets()
        self.window.show_all()

    def create_widgets(self):
        vbox = gtk.VBox()
        hbox = gtk.HBox()
        hbox_up = gtk.HBox()
        hbox_middle = gtk.HBox()
        hbox_bottom = gtk.HBox()

        hbox_up.pack_start(gtk.HSeparator())
        hbox_up.pack_start(gtk.Label('Today'))
        hbox_up.pack_start(gtk.HSeparator())

        hbox_middle.pack_start(gtk.HSeparator())
        hbox_middle.pack_start(gtk.Label('Tomorrow'))
        hbox_middle.pack_start(gtk.HSeparator())

        hbox.pack_start(self.vbox1, True, True, 0)
        hbox.pack_start(self.vbox2, True, True, 0)
        hbox_bottom.pack_start(self.vbox3, True, True, 0)
        hbox_bottom.pack_start(self.vbox4, True, True, 0)

        vbox.pack_start(hbox_up)
        vbox.pack_start(hbox)
        vbox.pack_start(hbox_middle)
        vbox.pack_start(hbox_bottom)

        self.window.add(vbox)
        self.window.show_all()

    def ready_data(self):
        data = get_cursor('weather_data')(location_name=self.name)[0]

        self.vbox1 = gtk.VBox(False, 8)
        self.vbox2 = gtk.VBox(False, 8)

        self.vbox3 = gtk.VBox(False, 2)
        self.vbox4 = gtk.VBox(False, 2)

        city = gtk.Label("City: " + data['location_name'])
        country = gtk.Label("Country: " + data['country_name'])
        temp = gtk.Label("Temprature: " + data['temp'])
        low = gtk.Label("Low: " + data['low'])
        high = gtk.Label("High: " + data['high'])
        mood = gtk.Label("Mood: " + data['text'])
        sunset = gtk.Label("Sunset: " + data['astronomy'].sunset)
        sunrise = gtk.Label("Sunrise: " + data['astronomy'].sunrise)
        humidity = gtk.Label("Humidity: " + data['atmosphere'].humidity)
        pressure = gtk.Label("Pressure: " + data['atmosphere'].pressure)
        rising = gtk.Label("Rising: " + data['atmosphere'].rising)
        visibility = gtk.Label("Visibility: " + data['atmosphere'].visibility)
        tmw_day = gtk.Label("Day: " + data['tmw'].day)
        tmw_low = gtk.Label("Low: " + data['tmw'].low)
        tmw_high = gtk.Label("High: " + data['tmw'].high)
        tmw_mood = gtk.Label("Mood: " + data['tmw'].text)
        tmw_date = gtk.Label("Date: " + data['tmw'].date)

        self.vbox1.pack_start(city)
        self.vbox1.pack_start(temp)
        self.vbox1.pack_start(low)
        self.vbox1.pack_start(sunrise)
        self.vbox1.pack_start(humidity)
        self.vbox1.pack_start(rising)
        self.vbox2.pack_start(country)
        self.vbox2.pack_start(mood)
        self.vbox2.pack_start(high)
        self.vbox2.pack_start(sunset)
        self.vbox2.pack_start(pressure)
        self.vbox2.pack_start(visibility)

        self.vbox3.pack_start(tmw_day)
        self.vbox3.pack_start(tmw_date)
        self.vbox3.pack_start(tmw_mood)
        self.vbox4.pack_start(tmw_low)
        self.vbox4.pack_start(tmw_high)
