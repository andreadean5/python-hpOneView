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

__title__ = 'server-profile-template'
__version__ = '0.0.1'
__copyright__ = '(C) Copyright (2012-2016) Hewlett Packard Enterprise Development LP'
__license__ = 'MIT'
__status__ = 'Development'

from hpOneView.resources.resource import ResourceClient


class ServerProfiles(object):
    URI = '/rest/server-profiles'

    def __init__(self, con):
        self._connection = con
        self._client = ResourceClient(con, self.URI)
        self.__default_values = {
            'type': 'ServerProfileV5'
        }

    def create(self, resource, timeout=-1):
        """
         Creates a server profile using the information provided in the resource parameter. Connection requests can be
         one of the following types - port auto, auto and explicit. An explicit request is where the request includes
         the adapter, port and flexNic. An auto request is where none of the three are specified and a port auto
         request is where just the adapter and port are specified.

        Args:
            resource: dict object to create
            timeout:
                Timeout in seconds. Wait task completion by default. The timeout does not abort the operation
                in OneView, just stop waiting for its completion.

        Returns:
            dict: Created server profile.

        """
        data = self.__default_values.copy()
        data.update(resource)
        return self._client.create(resource=data, timeout=timeout)

    def update(self, resource, id_or_uri):
        """
        Allows a server profile object to have its configuration modified. These modifications can be as simple as a
        name or description change or much more complex changes around the assigned server and networking configuration.
        It should be noted that selection of a virtual or physical MAC or Serial Number is not mutable once a profile
        has been created, and attempts to change those elements will not be applied to the target profile. Connection
        requests can be one of the following types - port Auto, auto and explicit. An explicit request is where the
        request portId parameter includes the adapter, port and flexNic. An auto request is where portId is set to
        "Auto" and a port auto request is where just the portId parameter includes just the adapter and port.

        Args:
            id_or_uri: Could be either the server profile id or the server profile uri.
            resource (dict): Object to update.

        Returns:
            dict: The server profile resource.
        """
        data = self.__default_values.copy()
        data.update(resource)
        return self._client.update(resource=data, uri=id_or_uri)

    def patch(self, id_or_uri, operation, path, value, timeout=-1):
        """
        Performs a specific patch operation for the given server profile.
        The supported operation is:
            Update the server profile from the server profile template.
                Operation: replace
                Path: /templateCompliance
                Value: Compliant

        Args:
            id_or_uri:
                Could be either the server profile id or the server profile uri
            operation:
                The type of operation: one of "add", "copy", "move", "remove", "replace", or "test".
            path:
                The JSON path the operation is to use. The exact meaning depends on the type of operation.
            value:
                The value to add or replace for "add" and "replace" operations, or the value to compare against
                for a "test" operation. Not used by "copy", "move", or "remove".

        Returns:
            dict: Server profile resource.
        """
        return self._client.patch(id_or_uri, operation, path, value, timeout)

    def delete(self, resource, timeout=-1):
        """
        Deletes a server profile object from the appliance based on its server profile UUID.

        Args:
            resource (dict): Object to delete.
            timeout:
                Timeout in seconds. Wait task completion by default. The timeout does not abort the operation
                in OneView, just stops waiting for its completion.

        Returns:
            bool: Indicating if the server profile was successfully deleted.
        """
        return self._client.delete(resource=resource, timeout=timeout)

    def get_all(self, start=0, count=-1, filter='', sort=''):
        """
        Gets a list of server profile based on optional sorting and filtering, and constrained by start and
        count parameters.
        Gets a list of server profiles based on optional sorting and filtering, and constrained by start and count
        parameters. Providing a -1 for the count parameter will restrict the result set size to 64 server profiles.

        Args:
            start:
                The first item to return, using 0-based indexing.
                If not specified, the default is 0 - start with the first available item.
            count:
                The number of resources to return.
                Providing a -1 for the count parameter will restrict the result set size to 64 server profile
                templates. The maximum number of profile templates is restricted to 256, i.e., if user requests more
                than 256, this will be internally limited to 256.
                The actual number of items in the response may differ from the
                requested count if the sum of start and count exceed the total number of items, or if returning the
                requested number of items would take too long.
            filter:
                A general filter/query string to narrow the list of items returned. The
                default is no filter - all resources are returned.
                Filters are supported for the name, description, serialNumber, uuid, affinity, macType, wwnType,
                serialNumberType, serverProfileTemplateUri, templateCompliance, status and state attributes.
            sort:
                The sort order of the returned data set. By default, the sort order is based
                on create time, with the oldest entry first.

        Returns:
            list: A list of server profiles.

        """
        return self._client.get_all(start=start, count=count, filter=filter, sort=sort)

    def get(self, id_or_uri):
        """
        Retrieves a server profile managed by the appliance by ID or by uri.

        Args:
            id_or_uri: Could be either the server profile resource id or uri.

        Returns:
            dict: The server profile resource.
        """
        return self._client.get(id_or_uri=id_or_uri)

    def get_by(self, field, value):
        """
        Get all server profile that matches a specified filter.
        The search is case insensitive.

        Args:
            field: field name to filter
            value: value to filter

        Returns:
            list: A list of server profiles.
        """
        return self._client.get_by(field, value)

    def get_by_name(self, name):
        """
        Gets a server profile by name.

        Args:
            name: Name of the server profile.

        Returns:
            dict: The server profile resource.
        """
        return self._client.get_by_name(name)

    def get_schema(self):
        """
        Generates the ServerProfile schema.

        Returns:
            dict: The server profile schema.
        """
        return self._client.get_schema()

    def get_compliance_preview(self, id_or_uri):
        """
        Gets the preview of manual and automatic updates required to make the server profile
        consistent with its template.
        Args:
            id_or_uri: Could be either the server profile resource id or uri.

        Returns:
            dict: Server profile compliance preview.
        """
        uri = self._client.build_uri(id_or_uri) + '/compliance-preview'
        return self._client.get(uri)

    def get_profile_ports(self, **kwargs):
        """
        Retrieves the port model associated with a server or server hardware type and enclosure group.

        Args:
            enclosureGroupUri (str):
                The URI of the enclosure group associated with the resource.
            serverHardwareTypeUri (str):
                The URI of the server hardware type associated with the resource.
            serverHardwareUri (str):
                The URI of the server hardware associated with the resource.

        Returns:
            dict: Profile port.
        """
        uri = self.__build_uri_with_query_string(kwargs, '/profile-ports')
        return self._client.get(uri)

    def get_messages(self, id_or_uri):
        """
        Retrieve the error or status messages associated with the specified profile.

        Args:
            id_or_uri: Could be either the server profile resource id or uri.

        Returns:
            dict: Server Profile Health
        """
        uri = self._client.build_uri(id_or_uri) + '/messages'
        return self._client.get(uri)

    def get_transformation(self, id_or_uri, **kwargs):
        """
        Transforms an existing profile by supplying a new server hardware type and/or enclosure group. A profile
        will be returned with a new configuration based on the capabilities of the supplied server hardware type
        and/or enclosure group. All deployed connections will have their port assignment set to 'Auto'.
        Re-selection of the server hardware may also be required. The new profile can subsequently be used for update
        the server profile but is not guaranteed to pass validation. Any incompatibilities will be flagged when the
        transformed server profile is submitted.

        Args:
            id_or_uri:
                Could be either the server profile resource id or uri.
            enclosureGroupUri (str):
                The URI of the enclosure group associated with the resource.
            serverHardwareTypeUri (str):
                The URI of the server hardware type associated with the resource.
            serverHardwareUri (str):
                The URI of the server hardware associated with the resource.

        Returns:
            dict: Server Profile
        """
        uri = self.__build_uri_with_query_string(kwargs, '/transformation', id_or_uri)
        return self._client.get(uri)

    def get_available_networks(self, **kwargs):
        """
        Retrieves the list of Ethernet networks, Fibre Channel networks and network sets that are available to a
        server profile along with their respective ports.

         Args:
            enclosureGroupUri (str):
                The URI of the enclosure group associated with the resource.
            functionType (str):
                The FunctionType (Ethernet or FibreChannel) to filter the list of networks returned.
            serverHardwareTypeUri (str):
                The URI of the server hardware type associated with the resource.
            serverHardwareUri (str):
                The URI of the server hardware associated with the resource.
            view (str):
                Return a specific subset of the attributes of the resource or collection, by specifying the name of a
                predefined view. The default view is expand - show all attributes of the resource and all elements of
                collections of resources.

                Values:
                    Ethernet - Specifies that the connection is to an Ethernet network or a network set.
                    FibreChannel - Specifies that the connection is to a Fibre Channel network.

        Returns:
            list: Available networks.
        """
        uri = self.__build_uri_with_query_string(kwargs, '/available-networks')
        return self._client.get(uri)

    def get_available_servers(self, **kwargs):
        """
        Retrieves the list of available servers.

         Args:
            enclosureGroupUri (str):
                The URI of the enclosure group associated with the resource.
            serverHardwareTypeUri (str):
                The URI of the server hardware type associated with the resource.
            profileUri (str):
                The URI of the server profile resource.

        Returns:
            list: Available servers.
        """
        uri = self.__build_uri_with_query_string(kwargs, '/available-servers')
        return self._client.get(uri)

    def get_available_storage_system(self, **kwargs):
        """
        Retrieve a specific storage system and its associated volumes that are available to the server profile based
        on the given server hardware type and enclosure group.

         Args:
            enclosureGroupUri (str):
                The URI of the enclosure group associated with the resource.
            serverHardwareTypeUri (str):
                The URI of the server hardware type associated with the resource.
            storageSystemId (str):
                The storage system ID associated with the resource.

        Returns:
            dict: Available storage system.
        """
        uri = self.__build_uri_with_query_string(kwargs, '/available-storage-system')
        return self._client.get(uri)

    def get_available_storage_systems(self, start=0, count=-1, filter='', sort='', **kwargs):
        """
        Retrieves the list of the storage systems and their associated volumes that are available to the server profile
        based on the given server hardware type and enclosure group.

         Args:
            count:
                The number of resources to return. A count of -1 requests all the items. The actual number of items in
                 the response may differ from the requested count if the sum of start and count exceed the total
                 number of items, or if returning the requested number of items would take too long.
            start:
                The first item to return, using 0-based indexing. If not specified, the default is 0 - start with the
                first available item.
            filter:
                A general filter/query string to narrow the list of items returned. The default is no filter - all
                resources are returned.
            sort:
                The sort order of the returned data set. By default, the sort order is based on create time, with the
                oldest entry first.
            enclosureGroupUri (str):
                The URI of the enclosure group associated with the resource.
            serverHardwareTypeUri (str):
                The URI of the server hardware type associated with the resource.


        Returns:
            list: Available storage systems.
        """
        uri = self.__build_uri_with_query_string(kwargs, '/available-storage-systems')
        return self._client.get_all(start=start, count=count, filter=filter, sort=sort, uri=uri)

    def get_available_targets(self, **kwargs):
        """
        Retrieves a list of the target servers and empty device bays that are available for assignment to the server
        profile.

         Args:

            enclosureGroupUri (str):
                The URI of the enclosure group associated with the resource.
            serverHardwareTypeUri (str):
                The URI of the server hardware type associated with the resource.
            profileUri (str):
                The URI of the server profile associated with the resource

        Returns:
            list:???
        """
        uri = self.__build_uri_with_query_string(kwargs, '/available-targets')
        return self._client.get(uri)

    def __build_uri_with_query_string(self, kwargs, sufix_path, id_or_uri=None):
        uri = self.URI
        if id_or_uri:
            uri = self._client.build_uri(id_or_uri)

        query_string = '&'.join('{}={}'.format(key, kwargs[key]) for key in sorted(kwargs))
        return uri + sufix_path + '?' + query_string
