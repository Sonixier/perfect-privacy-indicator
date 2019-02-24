#!/usr/bin/env python3
import signal
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk, AppIndicator3, GObject
import time
import os
import requests
from threading import Thread
import texts

texts = texts.import_texts()

#This value determines at which intervals it is checked whether you are connected with perfect privacy or not
wait_seconds = 30

title = "Perfect-Privacy-Indicator"
pp_url = "https://checkip.perfect-privacy.com/csv"
current = None
indpath = os.getcwd() + "/"

class Indicator():
    def __init__(self):
        self.app = title
        iconpath = indpath + "vpn-grey.png"
        self.indicator = AppIndicator3.Indicator.new(
            self.app, iconpath,
            AppIndicator3.IndicatorCategory.OTHER)
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self.create_menu())
        self.update = Thread(target=self.show_seconds)
        self.update.setDaemon(True)
        self.update.start()

    def create_menu(self):
        menu = Gtk.Menu()
        item_1 = Gtk.MenuItem(texts["refresh_button"])
        item_1.connect('activate', self.refresh)
        menu.append(item_1)
        menu_sep = Gtk.SeparatorMenuItem()
        menu.append(menu_sep)
        # quit
        item_quit = Gtk.MenuItem(texts["quit_button"])
        item_quit.connect('activate', self.stop)
        menu.append(item_quit)
        menu.show_all()
        return menu

    def refresh(self, source):
        self.indicator.set_icon(indpath + "vpn-grey.png")
        notcur = get_state()
        if notcur == "true":
            os.system(
                'notify-send -i ' + indpath + 'vpn-green.png "' + texts["connected_title"] + '" "' + texts["connected"] + '"')
            self.indicator.set_icon(indpath + "vpn-green.png")

        if notcur == "false":
            os.system(
                'notify-send -i ' + indpath + 'vpn-red.png "' + texts["disconnected_title"] + '" "' + texts["disconnected"] + '"')
            self.indicator.set_icon(indpath + "vpn-red.png")

    def show_seconds(self):
        current = None
        while True:
            mention = get_state()
            if mention == "true":
                if current == "false":
                    os.system('notify-send -i ' + indpath + 'vpn-green.png "' + texts["connected_title"] + '" "' + texts["connected"] + '"')
                self.indicator.set_icon(indpath + "vpn-green.png")
            else:
                if current == "true":
                    os.system('notify-send -i ' + indpath + 'vpn-red.png "' + texts["disconnected_title"] + '" "' + texts["disconnected"] + '"')
                self.indicator.set_icon(indpath + "vpn-red.png")
            current = mention
            time.sleep(wait_seconds)

    def stop(self, source):
        Gtk.main_quit()

def get_state():
    try:
        r = requests.get(pp_url)
    except:
        return "false"
    return r.text.split(",")[7]

Indicator()
GObject.threads_init()
signal.signal(signal.SIGINT, signal.SIG_DFL)
Gtk.main()
