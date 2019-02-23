from tornado.web import RequestHandler
from tornado.httpclient import AsyncHTTPClient, HTTPResponse
import requests

from wwac.helpers.statsd import statsd_client


class PingHandler(RequestHandler):
    _response = {
        'status': 'ok'
    }

    def get(self):
        self.write(self._response)
        self.set_status(200)
        self.finish()


class ProxyHandler(RequestHandler):

    def prepare(self):
        url = self.get_argument('url', None)
        if not url:
            self.send_error(400)
        else:
            self.url = f'https://{url}'

    def get(self, *args, **kwargs):
        statsd_client.incr(f'{self.__class__.__name__}.get')
        with statsd_client.timer(f'{self.__class__.__name__}.get'):
            response: requests.Response = requests.get(self.url)
            code, content = response.status_code, response.content
            self.set_status(code)
            self.write(content)


class AsyncHandler(ProxyHandler):
    async def get(self, *args, **kwargs):
        statsd_client.incr(f'{self.__class__.__name__}.get')
        with statsd_client.timer(f'{self.__class__.__name__}.get'):
            http_client = AsyncHTTPClient()
            response: HTTPResponse = await http_client.fetch(self.url)
            code, content = response.code, response.body
            self.set_status(code)
            self.write(content)
