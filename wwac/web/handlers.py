from tornado.web import RequestHandler
from tornado.httpclient import AsyncHTTPClient, HTTPResponse
import requests


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
        response: requests.Response = requests.get(self.url)
        code, content = response.status_code, response.content
        self.set_status(code)
        self.write(content)


class AsyncHandler(ProxyHandler):
    async def get(self, *args, **kwargs):
        http_client = AsyncHTTPClient()
        response: HTTPResponse = await http_client.fetch(self.url)
        code, content = response.code, response.body
        self.set_status(code)
        self.write(content)
