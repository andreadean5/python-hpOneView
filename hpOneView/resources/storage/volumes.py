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

__title__ = 'volumes'
__version__ = '0.0.1'
__copyright__ = '(C) Copyright (2012-2016) Hewlett Packard Enterprise ' \
                ' Development LP'
__license__ = 'MIT'
__status__ = 'Development'

from hpOneView.resources.resource import ResourceClient

INVALID_VOLUME_URI = "When no snapshot uri is provided, volume id or valume uri is required."


class Volumes(object):
    URI = '/rest/storage-volumes'

    def __init__(self, con):
        self._connection = con
        self._client = ResourceClient(con, self.URI)
        self.__snapshot_default_values = {
            "type": "Snapshot"
        }

    def get_all(self, start=0, count=-1, filter='', sort=''):
        """
        Gets a paginated collection of managed volumes. The collection is based on optional
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
            list: A list of managed volumes.
        """
        return self._client.get_all(start, count, filter=filter, sort=sort)

    def get(self, id_or_uri):
        """
        Gets the managed volume.

        Args:
            id_or_uri: Could be either the volume id or the volume uri.

        Returns: Managed volume.
        """
        return self._client.get(id_or_uri)

    def get_by(self, field, value):
        """
        Get all managed volumes that matches the given filter.
        The search is case insensitive.

        Args:
            field: Field name to filter.
            value: Value to filter.

        Returns:
            list: A list of managed volumes.
        """
        return self._client.get_by(field, value)

    def create(self, resource, timeout=-1):
        """
        Creates or adds a volume.

        It's possible to create the volume in 6 different ways:

          It's possible to create the volume in 6 different ways:

          1) Common = Storage System + Storage Pool
          2) Template = Storage Volume Template
          3) Common with snapshots = Storage System + Storage Pool + Snapshot Pool
          4) Management = Storage System + wwn
          5) Management by name = Storage System + Storage System Volume Name
          6) Snapshot = Snapshot Pool + Storage Pool + Snapshot.

          NOTE: The 4) and 5) are for adding a volume for management, it do not create new volumes.

        Args:
            resource: dict object to create
            timeout:
                Timeout in seconds. Wait task completion by default. The timeout does not abort the operation
                in OneView, just stop waiting for its completion.

        Returns:
            dict: Created or added resource.
        """
        return self._client.create(resource, timeout=timeout)

    def update(self, resource, force=False, timeout=-1):
        """
        Updates properties of a volume.

        Reverts a volume to the specified snapshot.

        Args:
            resource: dict object to update
            force:
                If set to true the operation completes despite any problems with network connectivity or errors on
                the resource itself. The default is false.
            timeout:
                Timeout in seconds. Wait task completion by default. The timeout does not abort the operation
                in OneView, just stop waiting for its completion.

        Returns: Updated resource.
        """
        return self._client.update(resource, timeout=timeout, force=force)

    def delete(self, resource, force=False, export_only=False, timeout=-1):
        """
        Deletes a managed volume.

        Args:
            resource: dict object to delete
            force:
                 If set to true the operation completes despite any problems with
                 network connectivity or errors on the resource itself. The default is false.
            timeout:
                Timeout in seconds. Wait task completion by default. The timeout does not abort the operation
                in OneView, just stops waiting for its completion.
            export_only:
                By default, volumes will be deleted from OneView and storage system.
                To delete the volume only from OneView, you must set its value to True.
                Setting its value to False has the same behaviour as the default behaviour.

        Returns:
            bool: indicating if the volume was successfully deleted.
        """
        custom_headers = {"exportOnly": export_only}
        return self._client.delete(resource, force=force, timeout=timeout, custom_headers=custom_headers)

    def __build_volume_snapshot_uri(self, volume_id_or_uri=None, snapshot_id_or_uri=None):
        if snapshot_id_or_uri and "/" in snapshot_id_or_uri:
            return snapshot_id_or_uri
        else:
            if not volume_id_or_uri:
                raise ValueError(INVALID_VOLUME_URI)
            volume_uri = self._client.build_uri(volume_id_or_uri)
            return volume_uri + "/snapshots/" + str(snapshot_id_or_uri or '')

    def get_snapshots(self, volume_id_or_uri, start=0, count=-1, filter='', sort=''):
        """
        Gets all snapshots of a volume. Returns a list of snapshots based on optional sorting and filtering, and
        constrained by start and count parameters.

        Args:
            volume_id_or_uri:
                Could be either the volume id or the volume uri
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
            list: A list of snapshots
        """
        uri = self.__build_volume_snapshot_uri(volume_id_or_uri)
        return self._client.get_all(start, count, filter=filter, sort=sort, uri=uri)

    def create_snapshot(self, volume_id_or_uri, snapshot, timeout=-1):
        """
        Creates a snapshot for the volume specified
        Args:
            volume_id_or_uri:
                Could be either the volume id or the volume uri
            snapshot (dict): Object to create
            timeout:
                Timeout in seconds. Wait task completion by default. The timeout does not abort the operation in
                OneView, just stops waiting for its completion.

        Returns:
            dict: Storage Volume

        """
        uri = self.__build_volume_snapshot_uri(volume_id_or_uri)
        data = self.__snapshot_default_values.copy()
        data.update(snapshot)
        return self._client.create(data, uri=uri, timeout=timeout)

    def get_snapshot(self, snapshot_id_or_uri, volume_id_or_uri=None):
        """
        Gets a snapshot of a volume
        Args:
            volume_id_or_uri:
                Could be either the volume id or the volume uri. It is optional if is passed a snapshot uri,
                but required if passed a snapshot id
            snapshot_id_or_uri:
                Could be either the snapshot id or the snapshot uri

        Returns:
            dict: The snapshot
        """
        uri = self.__build_volume_snapshot_uri(volume_id_or_uri, snapshot_id_or_uri)
        return self._client.get(uri)

    def delete_snapshot(self, resource, force=False, timeout=-1):
        """
        Deletes a snapshot from OneView and storage system.

        Args:
            resource (dict): object to remove
            force (bool):
                 If set to true the operation completes despite any problems with
                 network connectivity or errors on the resource itself. The default is false.
            timeout:
                Timeout in seconds. Wait task completion by default. The timeout does not abort the operation
                in OneView, just stops waiting for its completion.

        Returns:
            dict: Details of associated volume

        """
        return self._client.delete(resource, force=force, timeout=timeout)

    def get_snapshot_by(self, volume_id_or_uri, field, value):
        """
        Get all snapshots that match the filter
        The search is case insensitive

        Args:
            volume_id_or_uri: Could be either the volume id or the volume uri
            field: field name to filter
            value: value to filter

        Returns:
            list: snapshots

        """
        uri = self.__build_volume_snapshot_uri(volume_id_or_uri)
        return self._client.get_by(field, value, uri=uri)

    def get_extra_managed_storage_volume_paths(self, start=0, count=-1, filter='', sort=''):
        """
        Gets the list of extra managed storage volume paths.

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
            list: A list of extra managed storage volume paths.
        """
        uri = self.URI + '/repair?alertFixType=ExtraManagedStorageVolumePaths'
        return self._client.get_all(start, count, filter=filter, sort=sort, uri=uri)

    def repair(self, volume_id_or_uri, timeout=-1):
        """
        Removes extra presentations from a specified volume on the storage system.

        Args:
            volume_id_or_uri:
                Could be either the volume id or the volume uri.
            timeout:
                Timeout in seconds. Wait task completion by default. The timeout does not abort the operation in
                OneView, just stops waiting for its completion.

        Returns:
            dict: Storage Volume.
        """
        data = {
            "type": "ExtraManagedStorageVolumePaths",
            "resourceUri": self._client.build_uri(volume_id_or_uri)
        }
        custom_headers = {'Accept-Language': 'en_US'}
        uri = self.URI + '/repair'
        return self._client.create(data, uri=uri, timeout=timeout, custom_headers=custom_headers)

    def get_attachable_volumes(self, start=0, count=-1, filter='', query='', sort=''):
        """
        Gets the volumes that are connected on the specified networks based on the storage system port's expected
        network connectivity.

        A volume is attachable if it satisfies either of the following conditions:

        - The volume is shareable
        - The volume not shareable and not attached.

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
            query:
                A general query string to narrow the list of resources returned. The default
                is no query - all resources are returned.
            sort:
                The sort order of the returned data set. By default, the sort order is based
                on create time, with the oldest entry first.

        Returns:
            list: A list of attachable volumes which are managed by the appliance.
        """
        uri = self.URI + '/attachable-volumes'
        return self._client.get_all(start, count, filter=filter, query=query, sort=sort, uri=uri)
