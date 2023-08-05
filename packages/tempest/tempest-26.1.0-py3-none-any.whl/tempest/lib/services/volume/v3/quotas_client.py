# Copyright 2014 OpenStack Foundation
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from urllib import parse as urllib

from oslo_serialization import jsonutils

from tempest.lib.api_schema.response.volume import quotas as schema
from tempest.lib.common import rest_client


class QuotasClient(rest_client.RestClient):
    """Client class to send CRUD Volume Quotas API requests"""

    def show_default_quota_set(self, tenant_id):
        """List the default volume quota set for a tenant."""

        url = 'os-quota-sets/%s/defaults' % tenant_id
        resp, body = self.get(url)
        body = jsonutils.loads(body)
        self.validate_response(schema.show_quota_set, resp, body)
        return rest_client.ResponseBody(resp, body)

    def show_quota_set(self, tenant_id, params=None):
        """List the quota set for a tenant."""

        url = 'os-quota-sets/%s' % tenant_id
        if params:
            url += '?%s' % urllib.urlencode(params)

        resp, body = self.get(url)
        body = jsonutils.loads(body)
        if params and params.get('usage', False):
            self.validate_response(schema.show_quota_set_usage, resp, body)
        else:
            self.validate_response(schema.show_quota_set, resp, body)
        return rest_client.ResponseBody(resp, body)

    def update_quota_set(self, tenant_id, **kwargs):
        """Updates quota set

        For a full list of available parameters, please refer to the official
        API reference:
        https://docs.openstack.org/api-ref/block-storage/v3/index.html#update-quotas-for-a-project
        """
        put_body = jsonutils.dumps({'quota_set': kwargs})
        resp, body = self.put('os-quota-sets/%s' % tenant_id, put_body)
        body = jsonutils.loads(body)
        self.validate_response(schema.update_quota_set, resp, body)
        return rest_client.ResponseBody(resp, body)

    def delete_quota_set(self, tenant_id):
        """Delete the tenant's quota set."""
        resp, body = self.delete('os-quota-sets/%s' % tenant_id)
        self.validate_response(schema.delete_quota_set, resp, body)
        return rest_client.ResponseBody(resp, body)
