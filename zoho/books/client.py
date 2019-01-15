# coding: utf8
from zoho.common.client import Client as CommonClient
from collections import OrderedDict


class Client(CommonClient):
    BASE_URL = 'https://books.zoho.com/api/v3/'

    READ_MODULE_LIST = OrderedDict([
        ('invoices', {'list_name': 'invoices'}),
        ('recurringinvoices', {'list_name': 'recurring_invoices'}),
        ('items', {'list_name': 'items'}),
        ('creditnotes', {'list_name': 'creditnotes'})
    ])

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
        response = self._get(url)
        all_data = response[module_conf['list_name']]
        while response['page_context']['has_more_page']:
            page = response['page_context']['page']
            response = self._get(url, params={'page': int(page) + 1})
            all_data.extend(response[module_conf['list_name']])
        return all_data
