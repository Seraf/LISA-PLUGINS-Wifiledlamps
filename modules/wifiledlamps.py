# -*- coding: UTF-8 -*-
import json, os, inspect, sys
from pymongo import MongoClient
from lisa import configuration
import wifileds

import gettext

path = os.path.realpath(os.path.abspath(os.path.join(os.path.split(
    inspect.getfile(inspect.currentframe()))[0],os.path.normpath("../lang/"))))
_ = translation = gettext.translation(domain='wifiledlamps', localedir=path, languages=[configuration['lang']]).ugettext

class Wifiledlamps:
    def __init__(self, lisa=None):
        self.lisa = lisa
        self.configuration_lisa = configuration
        mongo = MongoClient(host=self.configuration_lisa['database']['server'],
                            port=self.configuration_lisa['database']['port'])
        self.configuration = mongo.lisa.plugins.find_one({"name": "Wifiledlamps"})
        self.led_connection = wifileds.limitlessled.connect(self.configuration['configuration']['controller']['address'],
                                                            self.configuration['configuration']['controller']['port'])

    def switch(self, jsonInput):
        if jsonInput['outcome']['entities']['wifiledlamps_actions']['value'] == 'on':
            self.led_connection.rgb.all_on()
            body = _('lights are on')
        elif jsonInput['outcome']['entities']['wifiledlamps_actions']['value'] == 'off':
            self.led_connection.rgb.all_off()
            body = _('lights are off')
        else:
            body = _('no valid command')
        return {"plugin": "Wifiledlamps",
                "method": "switch",
                "body": body
        }
