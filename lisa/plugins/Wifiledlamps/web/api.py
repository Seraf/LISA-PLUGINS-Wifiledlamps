from tastypie import authorization
from django.conf.urls import patterns, url, include
from tastypie import resources
from tastypie.utils import trailing_slash
import json
from lisa.server.web.weblisa.api.mixins import CustomApiKeyAuthentication
from tastypie.authentication import MultiAuthentication, SessionAuthentication
import wifileds
from ..modules.wifiledlamps import Wifiledlamps


class WifiledlampsResource(resources.Resource):
    def __init__(self):
        super(WifiledlampsResource, self).__init__()
        self.Plugin = Wifiledlamps()

    class Meta:
        resource_name = 'wifiledlamps'
        allowed_methods = ()
        authorization = authorization.Authorization()
        object_class = Wifiledlamps
        authentication = MultiAuthentication(CustomApiKeyAuthentication())
        extra_actions = [
            {
                'name': 'switch',
                'http_method': 'POST',
                'resource_type': 'list',
                'fields': {
                    'on_off': {
                        'type': 'string',
                        'required': True,
                        'description': 'on or off',
                        'paramType': 'body'
                    },
                    'rooms': {
                        'type': 'list',
                        'required': True,
                        'description': "Provide a list of rooms : ['all','bedroom','kitchen'] ...",
                        'paramType': 'body'
                    },
                    'color': {
                        'type': 'string',
                        'required': False,
                        'description': "Color to use",
                        'paramType': 'body'
                    },
                    'intensity': {
                        'type': 'string',
                        'required': False,
                        'description': 'Intensity to use',
                        'paramType': 'body'
                    },
                    'groups': {
                        'type': 'list',
                        'required': False,
                        'description': "Which groups to use (1,2,3,4). By default, will use all.",
                        'paramType': 'body'
                    },
                    'lamptype': {
                        'type': 'string',
                        'required': False,
                        'description': "rgb, white or rgbw. By default, will use rgbw.",
                        'paramType': 'body'
                    },
                }
            }
        ]

    def base_urls(self):
        return [
            url(r"^plugin/(?P<resource_name>%s)%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('dispatch_list'), name="api_dispatch_list"),
            url(r"^plugin/(?P<resource_name>%s)/schema%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_schema'), name="api_get_schema"),
            url(r"^(?P<resource_name>%s)/switch%s" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('switch'), name="api_wifiledlamps_switch"),
        ]

    def switch(self, request, **kwargs):
        self.method_check(request, allowed=['post', 'get'])
        self.is_authenticated(request)
        self.throttle_check(request)

        from tastypie.http import HttpAccepted, HttpNotModified

        data = self.deserialize(request, request.body, format=request.META.get('CONTENT_TYPE', 'application/json'))
        on_off = data.get('on_off', '')
        rooms = data.get('rooms', '')
        groups = data.get('groups', [1, 2, 3, 4])
        color = data.get('color', '')
        intensity = data.get('intensity', '')
        lamptype = data.get('lamptype', 'rgbw')

        for room in self.Plugin.configuration_plugin['configuration']['controller']:
            if room['room'] in rooms:
                self.led_connection = wifileds.limitlessled.connect(room['address'],
                                                                    room['port'])
                if on_off == 'on':
                    if groups:
                        for group in groups:
                            if lamptype == 'white':
                                self.led_connection.white.zone_on(group)
                            elif lamptype == 'rgb':
                                self.led_connection.rgb.zone_on(group)
                            else:
                                self.led_connection.rgbw.zone_on(group)
                    else:
                        if lamptype == 'white':
                            self.led_connection.white.all_on()
                        elif lamptype == 'rgb':
                            self.led_connection.rgb.all_on()
                        else:
                            self.led_connection.rgbw.all_on()
                else:
                    if groups:
                        for group in groups:
                            if lamptype == 'white':
                                self.led_connection.white.zone_off(group)
                            elif lamptype == 'rgb':
                                self.led_connection.rgb.zone_off(group)
                            else:
                                self.led_connection.rgbw.zone_off(group)
                    else:
                        if lamptype == 'white':
                            self.led_connection.white.all_off()
                        elif lamptype == 'rgb':
                            self.led_connection.rgb.all_off()
                        else:
                            self.led_connection.rgbw.all_off()

        self.log_throttled_access(request)
        return self.create_response(request, {'status': 'success', 'log': "ok"}, HttpAccepted)
