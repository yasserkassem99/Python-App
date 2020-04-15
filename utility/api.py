import requests
import threading


class Api:
    def __init__(self, method=None, params={}, path=''):
        self.base_uri = 'https://api-dev-dot-waybill-project.appspot.com/'
        self.integration_token = 'tMkHWUvtBtMXf22fmy4mBLuAqvQX4kDw'
        self.path = path
        self.data = {
            'method': method,
            'integration_token': self.integration_token,
        }
        # get the parmas
        for k, v in params.items():
            self.data[k] = v

    def get(self):
        r = requests.get(f'{self.base_uri}{self.path}', params=self.data)
        result = r.json()
        return result
