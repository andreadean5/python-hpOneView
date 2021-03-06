# -*- coding: utf-8 -*-
###
# (C) Copyright (2012-2016) Hewlett Packard Enterprise Development LP
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
###

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from future import standard_library

standard_library.install_aliases()

__title__ = 'Enclosure Groups'
__version__ = '0.0.1'
__copyright__ = '(C) Copyright (2012-2016) Hewlett Packard Enterprise ' \
                ' Development LP'
__license__ = 'MIT'
__status__ = 'Development'

from hpOneView.resources.resource import ResourceClient


class EnclosureGroups(object):
    URI = '/rest/enclosure-groups'

    def __init__(self, con):
        self._connection = con
        self._client = ResourceClient(con, self.URI)
        self.__default_values = {"type": "EnclosureGroupV200"}

    def get_all(self, start=0, count=-1, filter='', sort=''):
        """
        Gets a list of enclosure groups.

        Args:
            start:
                The first item to return, using 0-based indexing.
                If not specified, the default is 0 - start with the first available item.
            count:
                The number of resources to return. A count of -1 requests all the items.
                The actual number of items in the response may differ from the requested
                count if the sum of start and count exceed the total number of items.
            filter:
                A general filter/query string to narrow the list of items returned. The
                default is no filter - all resources are returned.
            sort:
                The sort order of the returned data set. By default, the sort order is based
                on create time, with the oldest entry first.

        Returns:
            list: A list of enclosure groups.
        """
        return self._client.get_all(start, count, filter=filter, sort=sort)

    def get(self, id_or_uri):
        """
        Gets a enclosure group by ID or by uri
        Args:
            id_or_uri: Could be either the enclosure group id or the enclosure group uri

        Returns:
            dict: enclosure group
        """
        return self._client.get(id_or_uri)

    def get_script(self, id_or_uri):
        """
        Gets the configuration script of the enclosure-group resource with the specified URI.

        Returns:
            dict:
        """

        uri = self._client.build_uri(id_or_uri) + "/script"

        return self._client.get(uri)

    def get_by(self, field, value):
        """
        Get all enclosure groups that matches the filter
        The search is case insensitive

        Args:
            field: field name to filter
            value: value to filter

        Returns:
            list: A list of enclosure groups.
        """
        return self._client.get_by(field, value)

    def create(self, resource, timeout=-1):
        """
         Creates an enclosure group. An interconnect bay mapping must be provided for each
          of the interconnect bays in the enclosure. For this release, the same logical
          interconnect group must be provided for each interconnect bay mapping.
        Args:
            resource (dict): Object to create
            timeout:
                Timeout in seconds. Wait task completion by default. The timeout does not abort the operation
                in OneView, just stops waiting for its completion.

        Returns:
            dict: Created enclosure group
        """
        data = self.__default_values.copy()
        data.update(resource)
        return self._client.create(data, timeout=timeout)

    def delete(self, resource, timeout=-1):
        """
         Deletes an enclosure group. An enclosure group cannot be deleted if any enclosures
         are currently part of that enclosure group.

        Args:
            resource (dict): object to delete
            timeout:
                Timeout in seconds. Wait task completion by default. The timeout does not abort the operation
                in OneView, just stops waiting for its completion.

        Returns:
            boolean: True when success

        """
        return self._client.delete(resource, timeout=timeout)

    def update(self, resource, timeout=-1):
        """
        Updates an enclosure group with new attributes.
        Args:
            resource (dict): Object to update
            timeout:
                Timeout in seconds. Wait task completion by default. The timeout does not abort the operation
                in OneView, just stops waiting for its completion.

        Returns:
            dict: Updated enclosure group

        """
        data = self.__default_values.copy()
        data.update(resource)
        return self._client.update(data, timeout=timeout)

    def update_script(self, id_or_uri, script_body):
        """
        Updates the configuration script of the enclosure-group with the specified URI.
        Args:
            id_or_uri: id or resource uri
            script_body:  configuration script

        Returns:
            dict: Updated enclosure group

        """
        uri = self._client.build_uri(id_or_uri) + "/script"

        return self._client.update(script_body, uri=uri)
