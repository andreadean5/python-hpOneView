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

__title__ = 'resource'
__version__ = '0.0.1'
__copyright__ = '(C) Copyright (2012-2016) Hewlett Packard Enterprise ' \
                ' Development LP'
__license__ = 'MIT'
__status__ = 'Development'

import logging
from urllib.parse import quote
from hpOneView.resources.task_monitor import TaskMonitor
from hpOneView.exceptions import HPOneViewUnknownType

RESOURCE_CLIENT_RESOURCE_WAS_NOT_PROVIDED = 'Resource was not provided'
RESOURCE_CLIENT_INVALID_FIELD = 'Invalid field was provided'
RESOURCE_CLIENT_INVALID_ID = 'Invalid id was provided'
RESOURCE_CLIENT_UNKNOWN_OBJECT_TYPE = 'Unknown object type'
UNRECOGNIZED_URI = 'Unrecognized URI for this resource'

logger = logging.getLogger(__name__)


class ResourceClient(object):
    """
    This class implements common functions for HpOneView API rest
    """

    def __init__(self, con, uri):
        self._connection = con
        self._uri = uri
        self._task_monitor = TaskMonitor(con)

    def get_all(self, start=0, count=-1, filter='', query='', sort='', view='', fields='', uri=None):
        """
        Gets all items according with the given arguments.

        More than one request can be send to get the items, regardless the query parameter 'count', since the actual
        number of items in the response may differ from the requested count. Some types of resource has a limited
        number of items returned on each call. For those resources, additional calls are made to the API to retrieve
        any other items matching the given filter. The actual number of items can also diverge from the requested call
        if the requested number of items would take too long.

        The use of optional parameters for OneView 2.0 is described at:
        http://h17007.www1.hpe.com/docs/enterprise/servers/oneview2.0/cic-api/en/api-docs/current/index.html

        NOTE: Single quote - "'" - inside a query parameter is not supported by OneView API.

        Args:
            start:
                The first item to return, using 0-based indexing.
                If not specified, the default is 0 - start with the first available item.
            count:
                The number of resources to return. A count of -1 requests all the items (default).
            filter:
                A general filter/query string to narrow the list of items returned. The default is no filter - all
                resources are returned.
            query:
                A single query parameter can do what would take multiple parameters or multiple GET requests using
                filter. Use query for more complex queries. NOTE: This parameter is experimental for OneView 2.0.
            sort:
                The sort order of the returned data set. By default, the sort order is based on create time, with the
                oldest entry first.
            view:
                Returns a specific subset of the attributes of the resource or collection by specifying the name of a
                predefined view. The default view is expand (show all attributes of the resource, and all elements of
                collections or resources).
            fields:
                Nome of the fields.
            uri:
                A specific URI (optional)

        Returns:
            list: A list of items matching the specified filter.
        """
        if filter:
            filter = "&filter=" + quote(filter)

        if query:
            query = "&query=" + quote(query)

        if sort:
            sort = "&sort=" + quote(sort)

        if view:
            view = "&view=" + quote(view)

        if fields:
            fields = "&fields=" + quote(fields)

        path = uri if uri else self._uri
        self.__validate_resource_uri(path)

        symbol = '?' if '?' not in path else '&'

        uri = "{0}{1}start={2}&count={3}{4}{5}{6}{7}{8}".format(path, symbol, start, count, filter, query, sort,
                                                                view, fields)

        logger.debug('Getting all resources with uri: {0}'.format(uri))

        result = self.__do_requests_to_getall(uri, count)

        return result

    def delete(self, resource, force=False, timeout=-1, custom_headers=None):

        if not resource:
            logger.exception(RESOURCE_CLIENT_RESOURCE_WAS_NOT_PROVIDED)
            raise ValueError(RESOURCE_CLIENT_RESOURCE_WAS_NOT_PROVIDED)

        if isinstance(resource, dict):
            if 'uri' in resource and resource['uri']:
                uri = resource['uri']
            else:
                logger.exception(RESOURCE_CLIENT_UNKNOWN_OBJECT_TYPE)
                raise HPOneViewUnknownType(RESOURCE_CLIENT_UNKNOWN_OBJECT_TYPE)
        else:
            uri = self._uri + "/" + resource

        if force:
            uri += '?force=True'

        logger.debug("Delete resource (uri = %s, resource = %s)" %
                     (self._uri, str(resource)))

        task, body = self._connection.delete(uri, custom_headers=custom_headers)

        if not task:
            # 204 NO CONTENT
            # Successful return from a synchronous delete operation.
            return True

        task = self._task_monitor.wait_for_task(task, timeout=timeout)

        return task

    def get_schema(self):
        logger.debug('Get schema (uri = %s, resource = %s)' %
                     (self._uri, self._uri))
        return self._connection.get(self._uri + '/schema')

    def get(self, id_or_uri):
        """
        Args:
            id_or_uri: Could be either the resource id or the resource uri
        Returns:
             The requested resource
        """
        uri = self.build_uri(id_or_uri)
        logger.debug('Get resource (uri = %s, ID = %s)' %
                     (uri, str(id_or_uri)))
        return self._connection.get(uri)

    def get_collection(self, id_or_uri, filter=''):
        """
        Retrieves a collection of resources.

        Use this function when the 'start' and 'count' parameters are not allowed in the GET call.
        Otherwise, use get_all instead.

        Optional filtering criteria may be specified.

        Args:
            id_or_uri: Could be either the resource id or the resource uri.
            filter: General filter/query string.

        Returns:
             Collection of the requested resource.
        """
        if filter:
            filter = "?filter=" + quote(filter)

        uri = "{uri}{filter}".format(uri=self.build_uri(id_or_uri), filter=filter)
        logger.debug('Get resource collection (uri = %s)' % uri)
        response = self._connection.get(uri)
        return self.__get_members(response)

    def update_with_zero_body(self, uri, timeout=-1, custom_headers=None):
        """
        Makes a PUT request to update a resource, when no request body is required.

        Args:
            uri:
                Could be either the resource id or the resource uri.
            timeout:
                Timeout in seconds. Wait task completion by default. The timeout does not abort the operation
                in OneView, just stops waiting for its completion.
            custom_headers:
                Allows set specific HTTP headers.

        Returns: Updated resource.
        """
        logger.debug('Update with zero length body (uri = %s)' % uri)

        return self.__do_put(uri, None, timeout, custom_headers)

    def update(self, resource, uri=None, force=False, timeout=-1, custom_headers=None):
        """
        Makes a PUT request to update a resource, when a request body is required.

        Args:
            uri:
                Could be either the resource id or the resource uri.
            force:
                If set to true the operation completes despite any problems with network connectivity or errors
                on the resource itself. The default is false.
            timeout:
                Timeout in seconds. Wait task completion by default. The timeout does not abort the operation
                in OneView, just stops waiting for its completion.
            custom_headers:
                Allows set specific HTTP headers.

        Returns: Updated resource.
        """
        if not resource:
            logger.exception(RESOURCE_CLIENT_RESOURCE_WAS_NOT_PROVIDED)
            raise ValueError(RESOURCE_CLIENT_RESOURCE_WAS_NOT_PROVIDED)

        logger.debug('Update async (uri = %s, resource = %s)' %
                     (self._uri, str(resource)))

        if not uri:
            uri = resource['uri']

        if force:
            uri += '?force=True'

        return self.__do_put(uri, resource, timeout, custom_headers)

    def create_with_zero_body(self, uri=None, timeout=-1, custom_headers=None):
        """
        Makes a POST request to create a resource, when no request body is required.

        Args:
            uri:
                Could be either the resource id or the resource uri.
            timeout:
                Timeout in seconds. Wait task completion by default. The timeout does not abort the operation
                in OneView, just stops waiting for its completion.
            custom_headers:
                Allows set specific HTTP headers.

        Returns: Created resource.
        """
        if not uri:
            uri = self._uri

        logger.debug('Create with zero body (uri = %s)' % uri)

        return self.__do_post(uri, None, timeout, custom_headers)

    def create(self, resource, uri=None, timeout=-1, custom_headers=None):
        """
        Makes a POST request to create a resource, when a request body is required.

        Args:
            uri:
                Could be either the resource id or the resource uri.
            timeout:
                Timeout in seconds. Wait task completion by default. The timeout does not abort the operation
                in OneView, just stops waiting for its completion.
            custom_headers:
                Allows set specific HTTP headers.

        Returns: Created resource.
        """
        if not resource:
            logger.exception(RESOURCE_CLIENT_RESOURCE_WAS_NOT_PROVIDED)
            raise ValueError(RESOURCE_CLIENT_RESOURCE_WAS_NOT_PROVIDED)

        if not uri:
            uri = self._uri

        logger.debug('Create (uri = %s, resource = %s)' %
                     (uri, str(resource)))

        return self.__do_post(uri, resource, timeout, custom_headers)

    def patch(self, id_or_uri, operation, path, value, timeout=-1, custom_headers=None):
        """
        Uses the PATCH to update a resource.
        Only one operation can be performed in each PATCH call.

        Args:
            id_or_uri: Could be either the resource id or the resource uri
            operation: Patch operation
            path: Path
            value: Value
            timeout: Timeout in seconds. Wait task completion by default. The timeout does not abort the operation
                in OneView, just stops waiting for its completion.

        Returns: Updated resource.
        """
        uri = self.build_uri(id_or_uri)

        logger.debug('Patch resource (uri = %s, op = %s, path = %s, value = %s)' % (
            uri, operation, path, value))

        patch_request = [{'op': operation, 'path': path, 'value': value}]
        task, entity = self._connection.patch(uri, patch_request, custom_headers=custom_headers)

        if not task:
            return entity

        return self._task_monitor.wait_for_task(task, timeout)

    def get_by(self, field, value, uri=None):
        """
        This function uses get_all passing a filter
        The search is case insensitive
        Args:
            field: field name to filter
            value: value to filter
            uri: resource uri

        Returns: dict

        """
        if not field:
            logger.exception(RESOURCE_CLIENT_INVALID_FIELD)
            raise ValueError(RESOURCE_CLIENT_INVALID_FIELD)

        if not uri:
            uri = self._uri
        self.__validate_resource_uri(uri)

        logger.debug('Get by (uri = %s, field = %s, value = %s)' %
                     (uri, field, str(value)))

        filter = "\"'{0}'='{1}'\"".format(field, value)
        return self.get_all(filter=filter, uri=uri)

    def get_by_name(self, name):
        """
        Retrieve a resource by his name
        Args:
            name: resource name

        Returns: dict
        """
        result = self.get_by('name', name)
        if not result:
            return None
        else:
            return result[0]

    def get_utilization(self, id_or_uri, fields=None, filter=None, refresh=False, view=None):
        """
        Retrieves historical utilization data for the specified resource, metrics, and time span.

        Args:
            id_or_uri: resource identification
            fields:
                Name of the supported metric(s) to be retrieved in the format METRIC[,METRIC]...
                If unspecified, all metrics supported are returned.

            filter:
                Filters should be in the format FILTER_NAME=VALUE[,FILTER_NAME=VALUE]...
                E.g.: 'startDate=2016-05-30T11:20:44.541Z,endDate=2016-05-30T19:20:44.541Z'

                startDate
                    Start date of requested starting time range in ISO 8601 format. If omitted, the startDate is
                    determined by the endDate minus 24 hours.
                endDate
                    End date of requested starting time range in ISO 8601 format. When omitted the endDate includes
                    the latest data sample available.

                If an excessive number of samples would otherwise be returned, the results will be segmented. The
                caller is responsible for comparing the returned sliceStartTime with the requested startTime in the
                response. If the sliceStartTime is greater than the oldestSampleTime and the requested start time,
                the caller is responsible for repeating the request with endTime set to sliceStartTime to obtain the
                next segment. This process is repeated until the full data set is retrieved.

                If the resource has no data, the UtilizationData is still returned, but will contain no samples and
                sliceStartTime/sliceEndTime will be equal. oldestSampleTime/newestSampleTime will still be set
                appropriately (null if no data is available). If the filter just does not happen to overlap the data
                that a resource does have, then the metric history service will return null sample values for any
                missing samples.

            refresh:
                Specifies that if necessary an additional request will be queued to obtain the most recent
                utilization data from the iLO. The response will not include any refreshed data. To track the
                availability of the newly collected data, monitor the TaskResource identified by the refreshTaskUri
                property in the response. If null, no refresh was queued.

            view:
                Specifies the resolution interval length of the samples to be retrieved. This is reflected in the
                resolution in the returned response. Utilization data is automatically purged to stay within storage
                space constraints. Supported views are listed below.

                native
                    Resolution of the samples returned will be one sample for each 5-minute time period. This is the
                    default view and matches the resolution of the data returned by the iLO. Samples at this resolution
                    are retained up to one year.
                hour
                    Resolution of the samples returned will be one sample for each 60-minute time period. Samples are
                    calculated by averaging the available 5-minute data samples that occurred within the hour, except
                    for PeakPower which is calculated by reporting the peak observed 5-minute sample value data during
                    the hour. Samples at this resolution are retained up to three years.
                day
                    Resolution of the samples returned will be one sample for each 24-hour time period. One day is a
                    24-hour period that starts at midnight GMT regardless of the time zone in which the appliance or
                    client is located. Samples are calculated by averaging the available 5-minute data samples that
                    occurred during the day, except for PeakPower which is calculated by reporting the peak observed
                    5-minute sample value data during the day. Samples at this resolution are retained up to three
                    years.

        Returns: dict

        """

        if not id_or_uri:
            raise ValueError(RESOURCE_CLIENT_INVALID_ID)

        query = ''

        if filter:
            query += self.__make_query_filter(filter)

        if fields:
            query += "&fields=" + quote(fields)

        if refresh:
            query += "&refresh=true"

        if view:
            query += "&view=" + quote(view)

        if query:
            query = "?" + query[1:]

        uri = "{0}/utilization{1}".format(self.build_uri(id_or_uri), query)

        return self._connection.get(uri)

    def build_uri(self, id_or_uri):
        if not id_or_uri:
            logger.exception(RESOURCE_CLIENT_INVALID_ID)
            raise ValueError(RESOURCE_CLIENT_INVALID_ID)

        if "/" in id_or_uri:
            self.__validate_resource_uri(id_or_uri)
            return id_or_uri
        else:
            return self._uri + "/" + id_or_uri

    def __validate_resource_uri(self, path):
        if self._uri not in path:
            logger.exception('Get by uri : unrecognized uri: (%s)' % path)
            raise HPOneViewUnknownType(UNRECOGNIZED_URI)

    def __make_query_filter(self, filter):
        filters = filter.split(",")
        formated_filter = "&filter=".join(quote(f) for f in filters)
        return "&filter=" + formated_filter

    def __get_members(self, mlist):
        if mlist and 'members' in mlist:
            return mlist['members']
        else:
            return []

    def __do_post(self, uri, resource, timeout, custom_headers):
        task, entity = self._connection.post(uri, resource, custom_headers=custom_headers)

        if not task:
            return entity

        return self._task_monitor.wait_for_task(task, timeout)

    def __do_put(self, uri, resource, timeout, custom_headers):
        task, body = self._connection.put(uri, resource, custom_headers=custom_headers)

        if not task:
            return body

        return self._task_monitor.wait_for_task(task, timeout)

    def __do_requests_to_getall(self, uri, count):
        items = []
        request_needed = True

        while request_needed:
            logger.debug('Making HTTP request to get all resources. Uri: {0}'.format(uri))
            response = self._connection.get(uri)
            members = self.__get_members(response)
            uri = response.get('nextPageUri')
            items += members
            logger.debug("Response getAll: nextPageUri = {0}, members list length: {1}".format(uri, str(len(members))))
            request_needed = uri and not len(members) == 0 and (len(items) < count or count == -1)

        logger.debug('Total # of members found = {0}'.format(str(len(items))))
        return items
