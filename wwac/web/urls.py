from tornado.web import RequestHandler
from typing import List, Tuple

from wwac.web.handlers import (
    PingHandler,
    ProxyHandler,
    AsyncHandler,
)

ping_url = (r'/ping/', PingHandler)

custom_urls = [
    (r'/sync-proxy/', ProxyHandler),
    (r'/async-proxy/', AsyncHandler),
]


def get_all_urls() -> List[Tuple[str, RequestHandler]]:
    return custom_urls + [ping_url]
