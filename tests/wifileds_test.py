import json, os, sys
from twisted.trial import unittest
from twisted.test import proto_helpers
sys.path.append(os.path.normpath(os.path.join(os.path.abspath("../../../"))))
import libs
from lisa import configuration

class WifiledsTestCase(unittest.TestCase):
    def setUp(self):
        factory = libs.LisaInstance
        self.proto = factory.buildProtocol(('127.0.0.1', 0))
        self.tr = proto_helpers.StringTransport()
        self.proto.makeConnection(self.tr)


    def _test(self, sentence, expected):
        self.proto.dataReceived(json.dumps({"type": "Chat", "zone": "Test",
                                            "from": "Test",
                                            "body": '%s' % (sentence)
        }))
        jsonAnswer = json.loads(self.tr.value())
        self.assertEqual(jsonAnswer['body'], expected)


    def test_hello(self):
        if configuration['lang'] == 'en':
            return self._test(sentence='chat test', expected='chat OK')
        elif configuration['lang'] == 'fr':
            return self._test(sentence='Bonjour', expected='Bonjour. Comment allez vous ?')

    def test_time(self):
        from datetime import datetime
        if configuration['lang'] == 'fr':
            now = datetime.now()
            return self._test(sentence='il est quelle heure', expected=now.strftime("Il est %H heures et %M minutes"))
        elif configuration['lang'] == 'en':
            now = datetime.now()
            return self._test(sentence='what time is it', expected=now.strftime("It is %H:%M%p"))
