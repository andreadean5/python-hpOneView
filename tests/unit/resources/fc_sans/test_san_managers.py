# -*- coding: utf-8 -*-
###
# (C) Copyright (2012-2016) Hewlett Packard Enterprise Development LP
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the 'Software'), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
###

from unittest import TestCase

import mock

from hpOneView.connection import connection
from hpOneView.resources.resource import ResourceClient
from hpOneView.resources.fc_sans.san_managers import SanManagers

TIMEOUT = -1


class SanManagersTest(TestCase):
    def setUp(self):
        host = '127.0.0.1'
        http_connection = connection(host)
        self._resource = SanManagers(http_connection)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_all(self, mock_get_all):
        query_filter = "name EQ 'TestName'"
        sort = 'name:ascending'

        self._resource.get_all(start=2, count=500, query=query_filter, sort=sort)
        mock_get_all.assert_called_once_with(start=2, count=500, query=query_filter, sort=sort)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_by_id(self, mock_get):
        id = "6fee02f3-b7c7-42bd-a528-04341e16bad6"

        self._resource.get(id)
        mock_get.assert_called_once_with(id_or_uri=id)

    @mock.patch.object(ResourceClient, 'create')
    def test_add_withId(self, mock_create):
        resource = {
            "connectionInfo": [
                {
                    "name": "Host",
                    "value": "brocade-device-manager.domain.com"
                },
                {
                    "name": "Port",
                    "value": 5989
                },
                {
                    "name": "Username",
                    "value": "Administrator"
                },
                {
                    "name": "Password",
                    "value": "password"
                },
                {
                    "name": "UseSsl",
                    "value": True
                }
            ]
        }

        provider_id = "534-345-345-55"
        rest_uri = "/rest/fc-sans/providers/534-345-345-55/device-managers"

        self._resource.add(resource, provider_uri_or_id=provider_id, timeout=TIMEOUT)
        mock_create.assert_called_once_with(resource=resource, uri=rest_uri, timeout=TIMEOUT)

    @mock.patch.object(ResourceClient, 'create')
    def test_add_withUri(self, mock_create):
        resource = {
            "connectionInfo": [
                {
                    "name": "Host",
                    "value": "brocade-device-manager.domain.com"
                },
                {
                    "name": "Port",
                    "value": 5989
                },
                {
                    "name": "Username",
                    "value": "Administrator"
                },
                {
                    "name": "Password",
                    "value": "password"
                },
                {
                    "name": "UseSsl",
                    "value": True
                }
            ]
        }

        provider_uri = "/rest/fc-sans/providers/534-345-345-55"
        rest_uri = "/rest/fc-sans/providers/534-345-345-55/device-managers"

        self._resource.add(resource, provider_uri_or_id=provider_uri, timeout=TIMEOUT)
        mock_create.assert_called_once_with(resource=resource, uri=rest_uri, timeout=TIMEOUT)

    @mock.patch.object(ResourceClient, 'get_by_name')
    def test_get_default_connection_info(self, mock_get_by_name):
        provider_name = "Brocade Network Advisor"
        self._resource.get_default_connection_info(provider_name)
        mock_get_by_name.assert_called_once_with(provider_name)

    @mock.patch.object(ResourceClient, 'get_by_name')
    def test_get_provider_uri(self, mock_get_by_name):
        provider_name = "Brocade Network Advisor"
        self._resource.get_provider_uri(provider_name)
        mock_get_by_name.assert_called_once_with(provider_name)

    @mock.patch.object(ResourceClient, 'update')
    def test_update(self, mock_update):
        uri = "/rest/fc-sans/device-managers/4ff2327f-7638-4b66-ad9d-283d4940a4ae"
        manager = dict(name="Device Manager Test", description="Direct Attach SAN Manager")

        self._resource.update(resource=manager, id_or_uri=uri)
        mock_update.assert_called_once_with(resource=manager, uri=uri)
