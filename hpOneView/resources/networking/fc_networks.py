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

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from future import standard_library

standard_library.install_aliases()

__title__ = 'fc-networks'
__version__ = '0.0.1'
__copyright__ = '(C) Copyright (2012-2016) Hewlett Packard Enterprise ' \
                ' Development LP'
__license__ = 'MIT'
__status__ = 'Development'

from hpOneView.resources.resource import ResourceClient


class FcNetworks(object):
    URI = '/rest/fc-networks'

    def __init__(self, con):
        self._connection = con
        self._client = ResourceClient(con, self.URI)
        self.__default_values = {
            'autoLoginRedistribution': False,
            'type': 'fc-networkV2',
            'linkStabilityTime': 30,
            'fabricType': 'FabricAttach',
        }

    def get_all(self, start=0, count=-1, filter='', sort=''):
        """
        Gets a paginated collection of Fibre Channel networks. The collection is based on optional
        sorting and filtering, and constrained by start and count parameters.

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
            list: A list of Fibre Channel networks.
        """
        return self._client.get_all(start, count, filter=filter, sort=sort)

    def delete(self, resource, force=False, timeout=-1):
        """
        Deletes a Fibre Channel network.
        Any deployed connections that are using the network are placed in the 'Failed' state.

        Args:
            resource: dict object to delete
            force:
                 If set to true the operation completes despite any problems with
                 network connectivity or errors on the resource itself. The default is false.
            timeout:
                Timeout in seconds. Wait task completion by default. The timeout does not abort the operation
                in OneView, just stops waiting for its completion.

        Returns:
            bool:

        """
        return self._client.delete(resource, force=force, timeout=timeout)

    def get(self, id):
        """
        Gets the Fibre Channel network with the specified ID
        Args:
            id: ID of Fibre Channel network

        Returns: dict
        """
        return self._client.get(id)

    def create(self, resource, timeout=-1):
        """
        Creates a Fibre Channel network.

        Args:
            resource: dict object to create
            timeout:
                Timeout in seconds. Wait task completion by default. The timeout does not abort the operation
                in OneView, just stop waiting for its completion.

        Returns: Created resource.

        """
        data = self.__default_values.copy()
        data.update(resource)
        return self._client.create(data, timeout=timeout)

    def update(self, resource, timeout=-1):
        """
        Updates a Fibre Channel network.

        Args:
            resource: dict object to update
            timeout:
                Timeout in seconds. Wait task completion by default. The timeout does not abort the operation
                in OneView, just stop waiting for its completion.

        Returns: Updated resource.

        """
        data = self.__default_values.copy()
        data.update(resource)
        return self._client.update(data, timeout=timeout)

    def get_by(self, field, value):
        """
        Get all Fibre Channel networks that matches the filter
        The search is case insensitive

        Args:
            field: field name to filter
            value: value to filter

        Returns:
            list: A list of Fibre Channel networks.
        """
        return self._client.get_by(field, value)
