# coding: utf8
from urllib.parse import urlencode
from zoho.common.client import Client as CommonClient


READ_MODULE_LIST = ['leads', 'accounts', 'contacts', 'deals', 'campaigns', 'tasks', 'cases', 'events', 'calls',
                    'solutions', 'products', 'vendors', 'pricebooks', 'quotes', 'salesorders', 'purchaseorders',
                    'invoices', 'custom', 'notes', 'approvals', 'dashboards', 'search', 'activities']
# module purchaseorders, 'invoices', salesorders and quotes are temporarily disable for writing this
# due to the complexity of the module
WRITE_MODULE_LIST = ['leads', 'accounts', 'contacts', 'deals', 'campaigns', 'tasks', 'cases', 'events', 'calls',
                     'solutions', 'products', 'vendors', 'pricebooks', 'purchaseorders', 'custom', 'notes']


class Client(CommonClient):
    BASE_URL = 'https://www.zohoapis.com/crm/v2/'

    def get_module_list(self):
        """

        :return:
        """
        url = self.BASE_URL + "settings/modules"
        response = self._get(url)
        if response:
            return [i for i in response['modules'] if i['api_supported'] is True]
        else:
            return None

    def get_fields_list(self, module):
        """

        :param module:
        :return:
        """
        params = {'module': module}
        url = self.BASE_URL + "settings/fields" + "?" + urlencode(params)
        response = self._get(url)
        if response:
            try:
                result = [
                    {
                        'id': i['id'],
                        'label': i['field_label'],
                        'api_name': i['api_name'],
                        'max_length': i['length'],
                        'read_only': i['read_only'],
                        'data_type': i['data_type'],
                        'currency': i['currency'],
                        'lookup': i['lookup'],
                        'pick_list_values': i['pick_list_values']
                    } for i in response['fields']]
            except Exception as e:
                print(e)
        else:
            return None
        return result

    def create_webhook(self, module, gearplug_webhook_id, notify_url):
        """

        :param module:
        :param gearplug_webhook_id:
        :param notify_url:
        :return:
        """
        endpoint = 'actions/watch'
        event = ["{0}.create".format(module)]
        data = [{'notify_url': notify_url, 'channel_id': gearplug_webhook_id, 'events': event, }]
        data = {'watch': data}
        url = self.BASE_URL + endpoint
        try:
            response = self._post(url, data=data)
        except Exception as e:
            return False
        if response['watch'][-1]['code'] == "SUCCESS":
            return response['watch'][-1]['details']
        else:
            return False

    def delete_webhook(self, webhook_id, module):
        """

        :return:
        """
        events = ["{0}.create".format(module)]
        data = [{'channel_id': webhook_id, 'events': events, '_delete_events': 'true'}]
        data = {'watch': data}
        endpoint = 'actions/watch'
        url = self.BASE_URL + endpoint
        response = self._patch(url, data=data)
        if response['watch'][-1]['code'] == "SUCCESS":
            return response['watch'][-1]['details']
        else:
            return False

    def get_records(self, module_name):
        """

        :param module_name: module from which to read record (api_name)
        :return:
        """
        if module_name not in READ_MODULE_LIST:
            return None
        url = self.BASE_URL + str(module_name)
        response = self._get(url)
        all_data = [response['data']]
        while response['info']['more_records'] == 'true':
            page = response['info']['page']
            response = self._get(url, params={'page': int(page) + 1})
            all_data.append(response['data'])
        return all_data

    def get_specific_record(self, module, id):
        """

        :return:
        """
        endpoint = '{0}/{1}'.format(module, id)
        url = self.BASE_URL + str(endpoint)
        response = self._get(url)
        if response and 'data' in response and len(response['data']) > 0 and response['data'][0]['id'] == id:
            return response['data']
        else:
            return False

    def get_all_active_users(self):
        """

        :return: all active users
        """
        endpoint = 'users?type=ActiveUsers'
        url = self.BASE_URL + str(endpoint)
        response = self._get(url)
        if response and 'users' in response and isinstance(response['users'], list) and len(response['users']) > 0:
            return response['users']
        else:
            return False

    def get_all_organizations(self):
        """

        :return: all oganizations
        """
        endpoint = 'org'
        url = self.BASE_URL + str(endpoint)
        response = self._get(url)
        if response and 'org' in response and isinstance(response['org'], list) and len(response['users']) > 0:
            return response['org']
        else:
            return False

    def insert_record(self, module_name, data):
        """

        :param module_name:
        :param data:
        :return:
        """
        if module_name.lower() not in WRITE_MODULE_LIST:
            return None
        url = self.BASE_URL + str(module_name)
        data = dict(data)
        for k, v in data.items():
            if v == 'False':
                data[k] = False
            if v == 'True':
                data[k] = True
        formatted_data = {'data': []}
        formatted_data['data'].append(data)
        return self._post(url, data=formatted_data)
