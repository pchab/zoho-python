# coding: utf8
from urllib.parse import urlencode
from zoho.common.client import Client as CommonClient


READ_MODULE_LIST = {
    'invoices': {},
    'recurringinvoices': {},
    'items': {}
}


class Client(CommonClient):
    BASE_URL = 'https://books.zoho.com/api/v3/'

    def get_records(self, module_name):
        """

        :param module_name:
        :return:
        """
        if module_name not in READ_MODULE_LIST:
            return None

        module_conf = READ_MODULE_LIST[module_name]

        url = self.BASE_URL + str(module_name)
        response = self._get(url)
        all_data = [response[module_conf['list_name']]]
        while response['page_context']['has_more_page']:
            page = response['page_context']['page']
            response = self._get(url, params={'page': int(page) + 1})
            all_data.append(response[module_conf['list_name']])
        return all_data
