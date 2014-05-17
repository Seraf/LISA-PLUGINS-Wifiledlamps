# -*- coding: UTF-8 -*-

from lisa.server.plugins.IPlugin import IPlugin
import gettext
import inspect
import os
import wifileds


class Wifiledlamps(IPlugin):
    def __init__(self):
        super(Wifiledlamps, self).__init__()
        self.configuration_plugin = self.mongo.lisa.plugins.find_one({"name": "Wifiledlamps"})
        self.path = os.path.realpath(os.path.abspath(os.path.join(os.path.split(
            inspect.getfile(inspect.currentframe()))[0],os.path.normpath("../lang/"))))
        self._ = translation = gettext.translation(domain='wifiledlamps',
                                                   localedir=self.path,
                                                   fallback=True,
                                                   languages=[self.configuration_lisa['lang']]).ugettext
        self.led_connection = wifileds.limitlessled.connect(self.configuration_plugin['configuration']['controller']['address'],
                                                            self.configuration_plugin['configuration']['controller']['port'])

    def switch(self, jsonInput):
        if jsonInput['outcome']['entities']['wifiledlamps_actions']['value'] == 'on':
            self.led_connection.rgb.all_on()
            body = self._('lights are on')
        elif jsonInput['outcome']['entities']['wifiledlamps_actions']['value'] == 'off':
            self.led_connection.rgb.all_off()
            body = self._('lights are off')
        else:
            body = self._('no valid command')
        return {"plugin": "Wifiledlamps",
                "method": "switch",
                "body": body
        }
