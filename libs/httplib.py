import requests

class Http:
    def __init__(self, base_url: str = None, params: dict = None,
                 headers: dict = None, timeout: int = None):

        self.base_url = base_url
        self.session = requests.Session()
        self.timeout = timeout

        if params is not None:
            self.session.params = params
        if headers is not None:
            self.session.headers = headers

    def request(self, method, url, headers: dict = None, data: dict = None,
                is_json: bool = False, timeout: int = None):
        print(f'发送{method}请求到{url}')
        if timeout is None:
            timeout = self.timeout

        if isinstance(url, str) and not url.startswith('http'):
            url = '%s%s' % (self.base_url, url)
        data, json = (None, data) if is_json else (data, None)
        res = self.session.request(method, url, headers=headers, data=data, json=json,timeout=timeout)
        try:
            return res.json()
        except Exception:
            return res.text

    def get(self, url, headers: dict = None, data: dict = None, is_json: bool = False, timeout: int = None):
        return self.request('GET', url, headers=headers, data=data, is_json=is_json)

    def post(self, url, headers: dict = None, data: dict = None, is_json: bool = False, timeout: int = None):
        return self.request('POST', url, headers=headers, data=data, is_json=is_json)

    def put(self, url, headers: dict = None, data: dict = None, is_json: bool = False, timeout: int = None):
        return self.request('PUT', url, headers=headers, data=data, is_json=is_json)

    def delete(self, url, headers: dict = None, data: dict = None, is_json: bool = False, timeout: int = None):
        return self.request('DELETE', url, headers=headers, data=data, is_json=is_json)
