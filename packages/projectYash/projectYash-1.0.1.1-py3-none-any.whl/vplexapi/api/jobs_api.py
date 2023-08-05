# coding: utf-8

"""
    VPlex REST API

    A definition for the next-gen VPlex API  # noqa: E501

    OpenAPI spec version: 0.1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from vplexapi.api_client import ApiClient


class JobsApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def cancel_vias_job(self, name, **kwargs):  # noqa: E501
        """Cancel a vias provisioning job  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.cancel_vias_job(name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str name: The name of a specific instance of the resource (required)
        :return: ViasJob
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.cancel_vias_job_with_http_info(name, **kwargs)  # noqa: E501
        else:
            (data) = self.cancel_vias_job_with_http_info(name, **kwargs)  # noqa: E501
            return data

    def cancel_vias_job_with_http_info(self, name, **kwargs):  # noqa: E501
        """Cancel a vias provisioning job  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.cancel_vias_job_with_http_info(name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str name: The name of a specific instance of the resource (required)
        :return: ViasJob
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['name']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method cancel_vias_job" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'name' is set
        if ('name' not in params or
                params['name'] is None):
            raise ValueError("Missing the required parameter `name` when calling `cancel_vias_job`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'name' in params:
            path_params['name'] = params['name']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # Authentication setting
        auth_settings = ['basicAuth', 'jwtAuth']  # noqa: E501

        return self.api_client.call_api(
            '/jobs/{name}/cancel', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ViasJob',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def create_vias_job(self, vias_payload, **kwargs):  # noqa: E501
        """Create a VIAS provisioning job  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_vias_job(vias_payload, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param ViasPayload vias_payload: (required)
        :return: ViasJob
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.create_vias_job_with_http_info(vias_payload, **kwargs)  # noqa: E501
        else:
            (data) = self.create_vias_job_with_http_info(vias_payload, **kwargs)  # noqa: E501
            return data

    def create_vias_job_with_http_info(self, vias_payload, **kwargs):  # noqa: E501
        """Create a VIAS provisioning job  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_vias_job_with_http_info(vias_payload, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param ViasPayload vias_payload: (required)
        :return: ViasJob
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['vias_payload']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method create_vias_job" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'vias_payload' is set
        if ('vias_payload' not in params or
                params['vias_payload'] is None):
            raise ValueError("Missing the required parameter `vias_payload` when calling `create_vias_job`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'vias_payload' in params:
            body_params = params['vias_payload']
        # Authentication setting
        auth_settings = ['basicAuth', 'jwtAuth']  # noqa: E501

        return self.api_client.call_api(
            '/jobs', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ViasJob',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def delete_vias_job(self, name, **kwargs):  # noqa: E501
        """Delete a VIAS provisioning jobs  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_vias_job(name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str name: The name of a specific instance of the resource (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.delete_vias_job_with_http_info(name, **kwargs)  # noqa: E501
        else:
            (data) = self.delete_vias_job_with_http_info(name, **kwargs)  # noqa: E501
            return data

    def delete_vias_job_with_http_info(self, name, **kwargs):  # noqa: E501
        """Delete a VIAS provisioning jobs  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_vias_job_with_http_info(name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str name: The name of a specific instance of the resource (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['name']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method delete_vias_job" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'name' is set
        if ('name' not in params or
                params['name'] is None):
            raise ValueError("Missing the required parameter `name` when calling `delete_vias_job`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'name' in params:
            path_params['name'] = params['name']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # Authentication setting
        auth_settings = ['basicAuth', 'jwtAuth']  # noqa: E501

        return self.api_client.call_api(
            '/jobs/{name}', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_vias_job(self, name, **kwargs):  # noqa: E501
        """Get the status of a VIAS provisioning job  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_vias_job(name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str name: The name of a specific instance of the resource (required)
        :param str fields: Select which fields are included in the response. 'name' is always included. See FieldSelectionExpression for details. 
        :return: ViasJob
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_vias_job_with_http_info(name, **kwargs)  # noqa: E501
        else:
            (data) = self.get_vias_job_with_http_info(name, **kwargs)  # noqa: E501
            return data

    def get_vias_job_with_http_info(self, name, **kwargs):  # noqa: E501
        """Get the status of a VIAS provisioning job  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_vias_job_with_http_info(name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str name: The name of a specific instance of the resource (required)
        :param str fields: Select which fields are included in the response. 'name' is always included. See FieldSelectionExpression for details. 
        :return: ViasJob
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['name', 'fields']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_vias_job" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'name' is set
        if ('name' not in params or
                params['name'] is None):
            raise ValueError("Missing the required parameter `name` when calling `get_vias_job`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'name' in params:
            path_params['name'] = params['name']  # noqa: E501

        query_params = []
        if 'fields' in params:
            query_params.append(('fields', params['fields']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # Authentication setting
        auth_settings = ['basicAuth', 'jwtAuth']  # noqa: E501

        return self.api_client.call_api(
            '/jobs/{name}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ViasJob',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_vias_jobs(self, **kwargs):  # noqa: E501
        """Get all the current VIAS provisioning jobs  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_vias_jobs(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str name: Filter results by name. See LexicalQueryExpression for details.
        :param str status: Filter results by status. See LexicalQueryExpression for details.
        :param int offset: Index of the first element to include in paginated results.<br> <b>'limit' must also be specified.</b>
        :param int limit: <p>Maximum number of elements to include in paginated results.<br> <b>'offset' must also be specified.<b>
        :param str sort_by: Specify the field priority order and direction for sorting.  See SortingOrderExpression for details. 
        :param str fields: Select which fields are included in the response. 'name' is always included. See FieldSelectionExpression for details. 
        :return: list[ViasJob]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_vias_jobs_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.get_vias_jobs_with_http_info(**kwargs)  # noqa: E501
            return data

    def get_vias_jobs_with_http_info(self, **kwargs):  # noqa: E501
        """Get all the current VIAS provisioning jobs  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_vias_jobs_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str name: Filter results by name. See LexicalQueryExpression for details.
        :param str status: Filter results by status. See LexicalQueryExpression for details.
        :param int offset: Index of the first element to include in paginated results.<br> <b>'limit' must also be specified.</b>
        :param int limit: <p>Maximum number of elements to include in paginated results.<br> <b>'offset' must also be specified.<b>
        :param str sort_by: Specify the field priority order and direction for sorting.  See SortingOrderExpression for details. 
        :param str fields: Select which fields are included in the response. 'name' is always included. See FieldSelectionExpression for details. 
        :return: list[ViasJob]
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['name', 'status', 'offset', 'limit', 'sort_by', 'fields']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_vias_jobs" % key
                )
            params[key] = val
        del params['kwargs']

        if 'offset' in params and params['offset'] < 0:  # noqa: E501
            raise ValueError("Invalid value for parameter `offset` when calling `get_vias_jobs`, must be a value greater than or equal to `0`")  # noqa: E501
        if 'limit' in params and params['limit'] > 100:  # noqa: E501
            raise ValueError("Invalid value for parameter `limit` when calling `get_vias_jobs`, must be a value less than or equal to `100`")  # noqa: E501
        if 'limit' in params and params['limit'] < 1:  # noqa: E501
            raise ValueError("Invalid value for parameter `limit` when calling `get_vias_jobs`, must be a value greater than or equal to `1`")  # noqa: E501
        collection_formats = {}

        path_params = {}

        query_params = []
        if 'name' in params:
            query_params.append(('name', params['name']))  # noqa: E501
        if 'status' in params:
            query_params.append(('status', params['status']))  # noqa: E501
        if 'offset' in params:
            query_params.append(('offset', params['offset']))  # noqa: E501
        if 'limit' in params:
            query_params.append(('limit', params['limit']))  # noqa: E501
        if 'sort_by' in params:
            query_params.append(('sort_by', params['sort_by']))  # noqa: E501
        if 'fields' in params:
            query_params.append(('fields', params['fields']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # Authentication setting
        auth_settings = ['basicAuth', 'jwtAuth']  # noqa: E501

        return self.api_client.call_api(
            '/jobs', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[ViasJob]',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def resubmit_vias_job(self, name, **kwargs):  # noqa: E501
        """Resubmit a vias provisioning job  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.resubmit_vias_job(name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str name: The name of a specific instance of the resource (required)
        :return: ViasJob
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.resubmit_vias_job_with_http_info(name, **kwargs)  # noqa: E501
        else:
            (data) = self.resubmit_vias_job_with_http_info(name, **kwargs)  # noqa: E501
            return data

    def resubmit_vias_job_with_http_info(self, name, **kwargs):  # noqa: E501
        """Resubmit a vias provisioning job  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.resubmit_vias_job_with_http_info(name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str name: The name of a specific instance of the resource (required)
        :return: ViasJob
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['name']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method resubmit_vias_job" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'name' is set
        if ('name' not in params or
                params['name'] is None):
            raise ValueError("Missing the required parameter `name` when calling `resubmit_vias_job`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'name' in params:
            path_params['name'] = params['name']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # Authentication setting
        auth_settings = ['basicAuth', 'jwtAuth']  # noqa: E501

        return self.api_client.call_api(
            '/jobs/{name}/resubmit', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ViasJob',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
