# coding: utf8
from zoho.common.client import Client as CommonClient
from collections import OrderedDict


class Client(CommonClient):
    BASE_URL = 'https://books.zoho.com/api/v3/'

    READ_MODULE_LIST = OrderedDict([
        ('invoices', {'list_name': 'invoices'}),
        ('recurringinvoices', {'list_name': 'recurring_invoices'}),
        ('items', {'list_name': 'items'}),
        ('creditnotes', {'list_name': 'creditnotes'}),
        ('organizations', {'list_name': 'organizations'})
    ])

    def __init__(self, client_id, client_secret, redirect_uri, scope, access_type, organization_id=None, refresh_token=None):
        super(Client, self).__init__(client_id, client_secret, redirect_uri, scope, access_type, refresh_token)
        self._organization_id = organization_id

    @property
    def available_read_modules(self):
        return list(self.READ_MODULE_LIST)

    def get_records(self, module_name):
        """

        :param module_name:
        :return:
        """
        if module_name not in self.READ_MODULE_LIST:
            return None

        module_conf = self.READ_MODULE_LIST[module_name]

        url = self.BASE_URL + str(module_name)

        base_params = {'organization_id': self._organization_id} if self._organization_id is not None else {}

        response = self._get(url, params=base_params)
        all_data = response[module_conf['list_name']]
        while response.get('page_context', {}).get('has_more_page'):
            page = response['page_context']['page']
            response = self._get(url, params=dict({'page': int(page) + 1}, **base_params))
            all_data.extend(response[module_conf['list_name']])
        return all_data
