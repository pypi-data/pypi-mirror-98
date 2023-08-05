# coding: utf-8

"""
    Pulp 3 API

    Fetch, Upload, Organize, and Distribute Software Packages  # noqa: E501

    The version of the OpenAPI document: v3
    Contact: pulp-list@redhat.com
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from pulpcore.client.pulp_2to3_migration.api_client import ApiClient
from pulpcore.client.pulp_2to3_migration.exceptions import (  # noqa: F401
    ApiTypeError,
    ApiValueError
)


class Pulp2ContentApi(object):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def list(self, **kwargs):  # noqa: E501
        """List pulp2 contents  # noqa: E501

        ViewSet for Pulp2Content model.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int limit: Number of results to return per page.
        :param int offset: The initial index from which to return the results.
        :param str ordering: Which field to use when ordering the results.
        :param str pulp2_content_type_id:
        :param list[str] pulp2_content_type_id__in: Filter results where pulp2_content_type_id is in a comma-separated list of values
        :param str pulp2_id:
        :param list[str] pulp2_id__in: Filter results where pulp2_id is in a comma-separated list of values
        :param int pulp2_last_updated: ISO 8601 formatted dates are supported
        :param int pulp2_last_updated__gt: Filter results where pulp2_last_updated is greater than value
        :param int pulp2_last_updated__gte: Filter results where pulp2_last_updated is greater than or equal to value
        :param int pulp2_last_updated__lt: Filter results where pulp2_last_updated is less than value
        :param int pulp2_last_updated__lte: Filter results where pulp2_last_updated is less than or equal to value
        :param list[int] pulp2_last_updated__range: Filter results where pulp2_last_updated is between two comma separated values
        :param str pulp3_content: Foreign Key referenced by HREF
        :param str fields: A list of fields to include in the response.
        :param str exclude_fields: A list of fields to exclude from the response.
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Paginatedpulp2to3MigrationPulp2ContentResponseList
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.list_with_http_info(**kwargs)  # noqa: E501

    def list_with_http_info(self, **kwargs):  # noqa: E501
        """List pulp2 contents  # noqa: E501

        ViewSet for Pulp2Content model.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int limit: Number of results to return per page.
        :param int offset: The initial index from which to return the results.
        :param str ordering: Which field to use when ordering the results.
        :param str pulp2_content_type_id:
        :param list[str] pulp2_content_type_id__in: Filter results where pulp2_content_type_id is in a comma-separated list of values
        :param str pulp2_id:
        :param list[str] pulp2_id__in: Filter results where pulp2_id is in a comma-separated list of values
        :param int pulp2_last_updated: ISO 8601 formatted dates are supported
        :param int pulp2_last_updated__gt: Filter results where pulp2_last_updated is greater than value
        :param int pulp2_last_updated__gte: Filter results where pulp2_last_updated is greater than or equal to value
        :param int pulp2_last_updated__lt: Filter results where pulp2_last_updated is less than value
        :param int pulp2_last_updated__lte: Filter results where pulp2_last_updated is less than or equal to value
        :param list[int] pulp2_last_updated__range: Filter results where pulp2_last_updated is between two comma separated values
        :param str pulp3_content: Foreign Key referenced by HREF
        :param str fields: A list of fields to include in the response.
        :param str exclude_fields: A list of fields to exclude from the response.
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(Paginatedpulp2to3MigrationPulp2ContentResponseList, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = [
            'limit',
            'offset',
            'ordering',
            'pulp2_content_type_id',
            'pulp2_content_type_id__in',
            'pulp2_id',
            'pulp2_id__in',
            'pulp2_last_updated',
            'pulp2_last_updated__gt',
            'pulp2_last_updated__gte',
            'pulp2_last_updated__lt',
            'pulp2_last_updated__lte',
            'pulp2_last_updated__range',
            'pulp3_content',
            'fields',
            'exclude_fields'
        ]
        all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout'
            ]
        )

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method list" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']

        if self.api_client.client_side_validation and 'pulp2_last_updated' in local_var_params and local_var_params['pulp2_last_updated'] > 2147483647:  # noqa: E501
            raise ApiValueError("Invalid value for parameter `pulp2_last_updated` when calling `list`, must be a value less than or equal to `2147483647`")  # noqa: E501
        if self.api_client.client_side_validation and 'pulp2_last_updated__gt' in local_var_params and local_var_params['pulp2_last_updated__gt'] > 2147483647:  # noqa: E501
            raise ApiValueError("Invalid value for parameter `pulp2_last_updated__gt` when calling `list`, must be a value less than or equal to `2147483647`")  # noqa: E501
        if self.api_client.client_side_validation and 'pulp2_last_updated__gte' in local_var_params and local_var_params['pulp2_last_updated__gte'] > 2147483647:  # noqa: E501
            raise ApiValueError("Invalid value for parameter `pulp2_last_updated__gte` when calling `list`, must be a value less than or equal to `2147483647`")  # noqa: E501
        if self.api_client.client_side_validation and 'pulp2_last_updated__lt' in local_var_params and local_var_params['pulp2_last_updated__lt'] > 2147483647:  # noqa: E501
            raise ApiValueError("Invalid value for parameter `pulp2_last_updated__lt` when calling `list`, must be a value less than or equal to `2147483647`")  # noqa: E501
        if self.api_client.client_side_validation and 'pulp2_last_updated__lte' in local_var_params and local_var_params['pulp2_last_updated__lte'] > 2147483647:  # noqa: E501
            raise ApiValueError("Invalid value for parameter `pulp2_last_updated__lte` when calling `list`, must be a value less than or equal to `2147483647`")  # noqa: E501
        collection_formats = {}

        path_params = {}

        query_params = []
        if 'limit' in local_var_params and local_var_params['limit'] is not None:  # noqa: E501
            query_params.append(('limit', local_var_params['limit']))  # noqa: E501
        if 'offset' in local_var_params and local_var_params['offset'] is not None:  # noqa: E501
            query_params.append(('offset', local_var_params['offset']))  # noqa: E501
        if 'ordering' in local_var_params and local_var_params['ordering'] is not None:  # noqa: E501
            query_params.append(('ordering', local_var_params['ordering']))  # noqa: E501
        if 'pulp2_content_type_id' in local_var_params and local_var_params['pulp2_content_type_id'] is not None:  # noqa: E501
            query_params.append(('pulp2_content_type_id', local_var_params['pulp2_content_type_id']))  # noqa: E501
        if 'pulp2_content_type_id__in' in local_var_params and local_var_params['pulp2_content_type_id__in'] is not None:  # noqa: E501
            query_params.append(('pulp2_content_type_id__in', local_var_params['pulp2_content_type_id__in']))  # noqa: E501
            collection_formats['pulp2_content_type_id__in'] = 'csv'  # noqa: E501
        if 'pulp2_id' in local_var_params and local_var_params['pulp2_id'] is not None:  # noqa: E501
            query_params.append(('pulp2_id', local_var_params['pulp2_id']))  # noqa: E501
        if 'pulp2_id__in' in local_var_params and local_var_params['pulp2_id__in'] is not None:  # noqa: E501
            query_params.append(('pulp2_id__in', local_var_params['pulp2_id__in']))  # noqa: E501
            collection_formats['pulp2_id__in'] = 'csv'  # noqa: E501
        if 'pulp2_last_updated' in local_var_params and local_var_params['pulp2_last_updated'] is not None:  # noqa: E501
            query_params.append(('pulp2_last_updated', local_var_params['pulp2_last_updated']))  # noqa: E501
        if 'pulp2_last_updated__gt' in local_var_params and local_var_params['pulp2_last_updated__gt'] is not None:  # noqa: E501
            query_params.append(('pulp2_last_updated__gt', local_var_params['pulp2_last_updated__gt']))  # noqa: E501
        if 'pulp2_last_updated__gte' in local_var_params and local_var_params['pulp2_last_updated__gte'] is not None:  # noqa: E501
            query_params.append(('pulp2_last_updated__gte', local_var_params['pulp2_last_updated__gte']))  # noqa: E501
        if 'pulp2_last_updated__lt' in local_var_params and local_var_params['pulp2_last_updated__lt'] is not None:  # noqa: E501
            query_params.append(('pulp2_last_updated__lt', local_var_params['pulp2_last_updated__lt']))  # noqa: E501
        if 'pulp2_last_updated__lte' in local_var_params and local_var_params['pulp2_last_updated__lte'] is not None:  # noqa: E501
            query_params.append(('pulp2_last_updated__lte', local_var_params['pulp2_last_updated__lte']))  # noqa: E501
        if 'pulp2_last_updated__range' in local_var_params and local_var_params['pulp2_last_updated__range'] is not None:  # noqa: E501
            query_params.append(('pulp2_last_updated__range', local_var_params['pulp2_last_updated__range']))  # noqa: E501
            collection_formats['pulp2_last_updated__range'] = 'csv'  # noqa: E501
        if 'pulp3_content' in local_var_params and local_var_params['pulp3_content'] is not None:  # noqa: E501
            query_params.append(('pulp3_content', local_var_params['pulp3_content']))  # noqa: E501
        if 'fields' in local_var_params and local_var_params['fields'] is not None:  # noqa: E501
            query_params.append(('fields', local_var_params['fields']))  # noqa: E501
        if 'exclude_fields' in local_var_params and local_var_params['exclude_fields'] is not None:  # noqa: E501
            query_params.append(('exclude_fields', local_var_params['exclude_fields']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['basicAuth', 'cookieAuth']  # noqa: E501

        return self.api_client.call_api(
            '/pulp/api/v3/pulp2content/', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Paginatedpulp2to3MigrationPulp2ContentResponseList',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def read(self, pulp_2to3_migration_pulp2_content_href, **kwargs):  # noqa: E501
        """Inspect a pulp2 content  # noqa: E501

        ViewSet for Pulp2Content model.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.read(pulp_2to3_migration_pulp2_content_href, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str pulp_2to3_migration_pulp2_content_href: (required)
        :param str fields: A list of fields to include in the response.
        :param str exclude_fields: A list of fields to exclude from the response.
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Pulp2to3MigrationPulp2ContentResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.read_with_http_info(pulp_2to3_migration_pulp2_content_href, **kwargs)  # noqa: E501

    def read_with_http_info(self, pulp_2to3_migration_pulp2_content_href, **kwargs):  # noqa: E501
        """Inspect a pulp2 content  # noqa: E501

        ViewSet for Pulp2Content model.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.read_with_http_info(pulp_2to3_migration_pulp2_content_href, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str pulp_2to3_migration_pulp2_content_href: (required)
        :param str fields: A list of fields to include in the response.
        :param str exclude_fields: A list of fields to exclude from the response.
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(Pulp2to3MigrationPulp2ContentResponse, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = [
            'pulp_2to3_migration_pulp2_content_href',
            'fields',
            'exclude_fields'
        ]
        all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout'
            ]
        )

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method read" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'pulp_2to3_migration_pulp2_content_href' is set
        if self.api_client.client_side_validation and ('pulp_2to3_migration_pulp2_content_href' not in local_var_params or  # noqa: E501
                                                        local_var_params['pulp_2to3_migration_pulp2_content_href'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `pulp_2to3_migration_pulp2_content_href` when calling `read`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'pulp_2to3_migration_pulp2_content_href' in local_var_params:
            path_params['pulp_2to3_migration_pulp2_content_href'] = local_var_params['pulp_2to3_migration_pulp2_content_href']  # noqa: E501

        query_params = []
        if 'fields' in local_var_params and local_var_params['fields'] is not None:  # noqa: E501
            query_params.append(('fields', local_var_params['fields']))  # noqa: E501
        if 'exclude_fields' in local_var_params and local_var_params['exclude_fields'] is not None:  # noqa: E501
            query_params.append(('exclude_fields', local_var_params['exclude_fields']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['basicAuth', 'cookieAuth']  # noqa: E501

        return self.api_client.call_api(
            '{pulp_2to3_migration_pulp2_content_href}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Pulp2to3MigrationPulp2ContentResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)
