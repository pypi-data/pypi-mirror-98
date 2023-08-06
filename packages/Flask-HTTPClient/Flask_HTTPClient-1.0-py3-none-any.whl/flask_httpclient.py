"""
@File    :   flask_httpclient.py
@Time    :   2021/03/14 3:47 下午
@Author  :   hjy
@Version :   1.0
@Contact :   haojunyu2012@gmail.com
@License :   (C)Copyright 2020-
@Desc    :   flask扩展：http客户端
"""

import requests


class HTTPError(Exception):
    ...


class HTTPClient(object):
    def __init__(self, app=None, base_url=None, timeout=None, config_prefix='HTTP_CLIENT',  **kwargs):
        self.base_url = base_url
        self.timeout = timeout
        self.config_prefix = config_prefix
        self.other = kwargs

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        if self.base_url is None:
            self.base_url = app.config[f'{self.config_prefix}_URL']
        if self.timeout is None:
            self.timeout = app.config.get(f'{self.config_prefix}_TIMEOUT', 1)
        self.session = requests.Session()

        # request请求重试
        if self.other.get('retry'):
            request_retry = requests.adapters.HTTPAdapaters(
                max_retries=self.other['retry'])
            self.session.mount('https://', request_retry)
            self.session.mount('http://', request_retry)

        self.app = app

        """
        if not hasattr(app, "extensions"):
            app.extensions = {}

        app.extensions.setdefault(config_prefix, {})
        app.extensions[config_prefix][self] = self.session
        """

    def _request_wrapper(self, method, api, **kwargs):
        url = self.base_url + api
        self.app.logger.info(
            f"sending {method} request to {self.url + api} ...  kwargs is {repr(kwargs)}")

        res = self.session.request(method, self.url + api, **kwargs)
        if res.status_code != 200:
            raise HTTPError(f"Http status code is not 200, status code {res.status_code}, "
                            f"response is {res.content}")
        # 返回有可能不是json格式
        if 'text/html' in res.headers['Content-Type']:
            self.app.logger.info(f"sending {method} request to {self.url + api} over ... response is "
                                 f"{repr(res.content)}")
            return res.text
        else:
            self.app.logger.info(f"sending {method} request to {self.url + api} over ... response is "
                                 f"{repr(res.json())}")
            return res.json() or dict()

        return self.session.request(method, url, **kwargs)

    def get(self, api, **kwargs):
        return self._request_wrapper('GET', api, **kwargs)

    def options(self, api, **kwargs):
        return self._request_wrapper('OPTIONS', api, **kwargs)

    def head(self, api, **kwargs):
        return self._request_wrapper('HEAD', api, **kwargs)

    def post(self, api, **kwargs):
        return self._request_wrapper('POST', api, **kwargs)

    def put(self, api, **kwargs):
        return self._request_wrapper('PUT', api, **kwargs)

    def patch(self, api, **kwargs):
        return self._request_wrapper('PATCH', api, **kwargs)

    def delete(self, api, **kwargs):
        return self._request_wrapper('DELETE', api, **kwargs)

    def __del__(self):
        try:
            if hasattr(self, "session"):
                self.session.close()
        except Exception as e:
            self.app.logger.exception(e)
