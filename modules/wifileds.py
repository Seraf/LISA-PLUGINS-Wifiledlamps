# -*- coding: UTF-8 -*-
import json, os, inspect
from pymongo import MongoClient
from lisa import configuration
import wifileds
from wifileds import limitlessled

import gettext

path = os.path.realpath(os.path.abspath(os.path.join(os.path.split(
    inspect.getfile(inspect.currentframe()))[0],os.path.normpath("../lang/"))))
_ = translation = gettext.translation(domain='wifileds', localedir=path, languages=[configuration['lang']]).ugettext

class Wifileds:
    def __init__(self):
        self.configuration_lisa = configuration
        mongo = MongoClient(host=self.configuration_lisa['database']['server'],
                            port=self.configuration_lisa['database']['port'])
        self.configuration = mongo.lisa.plugins.find_one({"name": "Wifileds"})
        self.led_connection = wifileds.limitlessled.connect(self.configuration['configuration']['address'],
                                                            self.configuration['configuration']['port'])

    def switch(self, jsonInput):
        if jsonInput['outcome']['entities']['wifileds_actions']['value'] == 'on':
            self.led_connection.rgb.all_on()
            body = _('lights are on')
        elif jsonInput['outcome']['entities']['wifileds_actions']['value'] == 'off':
            self.led_connection.rgb.all_off()
            body = _('lights are off')
        return {"plugin": "Wifileds",
                "method": "switch",
                "body": body
        }
