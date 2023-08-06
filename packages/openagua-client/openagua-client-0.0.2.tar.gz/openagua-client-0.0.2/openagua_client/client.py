from os import environ
import requests


class Client:
    datetime = None
    _step = 0
    paused = False
    stopped = False

    def __init__(self, request_host=None, api_endpoint=None, api_key=None):

        if api_endpoint is None:
            if request_host:
                api_endpoint = request_host + 'api/v1'
            else:
                api_endpoint = 'https://www.openagua.org/api/v1'

        # set up api
        self.api_key = api_key or environ.get('OA_SECRET_KEY')
        self.api_endpoint = api_endpoint
        self.api_headers = {'X-API-KEY': self.api_key}

    def __getattr__(self, name):
        def method(*args, **kwargs):
            if name[:4] == 'add_':
                return self.request_post(name, **kwargs)
            elif name[:4] == 'get_':
                return self.request_get(name, *args, **kwargs)
            elif name[:7] == 'update_':
                return self.request_put(name, *args, **kwargs)
            else:
                return getattr(self, name)(*args, **kwargs)

        return method

    def request_post(self, fn, **kwargs):
        resource = fn[4:]  # add_
        url = '{}/{}'.format(self.api_endpoint, resource + 's')
        resp = requests.post(url, headers=self.api_headers, json=kwargs)
        if resp.status_code == 200:
            return resp.json()
        else:
            return {'status_code': resp.status_code}

    def request_get(self, fn, *args, **kwargs):
        resource = fn[4:]  # get_
        resource_id = args[0]
        url = '{}/{}/{}'.format(self.api_endpoint, resource + 's', resource_id)
        resp = requests.get(url, headers=self.api_headers, params=kwargs)
        if resp.status_code == 200:
            return resp.json()
        else:
            return {'status_code': resp.status_code}

    def request_put(self, fn, *args, **kwargs):
        resource = fn[7:]  # update_
        resource_id = args[0]
        url = '{}/{}/{}'.format(self.api_endpoint, resource + 's', resource_id)
        resp = requests.get(url, headers=self.api_headers, params=kwargs)
        if resp.status_code == 200:
            return resp.json()
        else:
            return {'status_code': resp.status_code}
