import base64
import json
from base64 import b64encode
from os import getpid
from socket import gethostname
from threading import currentThread
from typing import Optional, List, Dict, Iterable, Union
from urllib.parse import urlencode, quote


from requests.structures import CaseInsensitiveDict


class ScrapeConfigError(Exception):
    pass


class ScrapeConfig:

    PUBLIC_DATACENTER_POOL = 'public_datacenter_pool'
    PUBLIC_RESIDENTIAL_POOL = 'public_residential_pool'

    url: str
    retry: bool = True
    method: str = 'GET'
    country: Optional[str] = None
    render_js: bool = False
    cache: bool = False
    cache_clear:bool = False
    ssl:bool = False
    dns:bool = False
    asp:bool = False
    debug: bool = False
    raise_on_upstream_error:bool = True
    cache_ttl:Optional[int] = None
    proxy_pool:Optional[str] = None
    session: Optional[str] = None
    tags: Optional[List[str]] = None
    correlation_id: Optional[str] = None
    cookies: Optional[CaseInsensitiveDict] = None
    body: Optional[str] = None
    data: Optional[Dict] = None
    headers: Optional[CaseInsensitiveDict] = None
    graphql: Optional[str] = None
    js: str = None
    rendering_wait: int = None
    session_sticky_proxy:bool = True
    screenshots:Optional[Dict]=None

    def __init__(
        self,
        url: str,
        retry: bool = True,
        method: str = 'GET',
        country: Optional[str] = 'DE',
        render_js: bool = False,
        cache: bool = False,
        cache_clear:bool = False,
        ssl:bool = False,
        dns:bool = False,
        asp:bool = False,
        debug: bool = False,
        raise_on_upstream_error:bool = True,
        cache_ttl:Optional[int] = None,
        proxy_pool:Optional[str] = None,
        session: Optional[str] = None,
        tags: Optional[List[str]] = None,
        correlation_id: Optional[str] = None,
        cookies: Optional[CaseInsensitiveDict] = None,
        body: Optional[str] = None,
        data: Optional[Dict] = None,
        headers: Optional[Union[CaseInsensitiveDict, Dict[str, str]]] = None,
        graphql: Optional[str] = None,
        js: str = None,
        rendering_wait: int = None,
        screenshots:Optional[Dict]=None,
        session_sticky_proxy:bool = True
    ):
        assert(type(url) is str)

        cookies = cookies or {}
        headers = headers or {}

        self.cookies = CaseInsensitiveDict(cookies)
        self.headers = CaseInsensitiveDict(headers)
        self.url = url
        self.retry = retry
        self.method = method
        self.country = country
        self.session_sticky_proxy = session_sticky_proxy
        self.render_js = render_js
        self.cache = cache
        self.cache_clear = cache_clear
        self.asp = asp
        self.session = session
        self.debug = debug
        self.cache_ttl = cache_ttl
        self.proxy_pool = proxy_pool
        self.tags = tags
        self.correlation_id = correlation_id
        self.body = body
        self.data = data
        self.graphql = graphql
        self.js = js
        self.rendering_wait = rendering_wait
        self.raise_on_upstream_error = raise_on_upstream_error
        self.screenshots = screenshots
        self.key = None
        self.dns = dns
        self.ssl = ssl

        if cookies:
            _cookies = []

            for name, value in cookies.items():
                _cookies.append(name + '=' + value)

            if 'cookie' in self.headers:
                if self.headers['cookie'][-1] != ';':
                    self.headers['cookie'] += ';'
            else:
                self.headers['cookie'] = ''

            self.headers['cookie'] += '; '.join(_cookies)

        if self.body and self.data:
            raise ScrapeConfigError('You cannot pass both parameters body and data. You must choose')

        if method in ['POST', 'PUT', 'PATCH']:
            if self.body is None and self.data is not None:
                if 'content-type' not in self.headers:
                    self.headers['content-type'] = 'application/x-www-form-urlencoded'
                    self.body = urlencode(data)
                else:
                    if self.headers['content-type'] == 'application/json':
                        self.body = json.dumps(data)
                    elif 'application/x-www-form-urlencoded' == self.headers['content-type']:
                        self.body = urlencode(data)
                    else:
                        raise ScrapeConfigError('Content Type %s not support, use body parameter to pass pre encoded body according to your content type' % self.headers['content-type'])
            elif self.body is None and self.data is None:
                self.headers['content-type'] = 'text/plain'

    def _bool_to_http(self, _bool:bool) -> str:
        return 'true' if _bool is True else 'false'

    def generate_distributed_correlation_id(self):
        self.correlation_id = abs(hash('-'.join([gethostname(), str(getpid()), str(currentThread().ident)])))

    def to_api_params(self, key:str) -> Dict:
        params = {
            'key': self.key if self.key is not None else key,
            'url': quote(self.url),
            'country': self.country,
        }

        for name, value in self.headers.items():
            params['headers[%s]' % name] = value

        if self.render_js is True:
            params['render_js'] = self._bool_to_http(self.render_js)

        if self.asp is True:
            params['asp'] = self._bool_to_http(self.asp)

        if self.retry is False:
            params['retry'] = self._bool_to_http(self.retry)

        if self.cache is True:
            params['cache'] = self._bool_to_http(self.cache)

        if self.dns is True:
            params['dns'] = self._bool_to_http(self.dns)

        if self.ssl is True:
            params['ssl'] = self._bool_to_http(self.ssl)

        if self.tags:
            params['tags'] = ','.join(self.tags)

        if self.correlation_id:
            params['correlation_id'] = self.correlation_id

        if self.screenshots is not None:
            for name, element in self.screenshots.items():
                params['screenshots[%s]' % name] = element

        if self.session:
            params['session'] = self.session
            params['session_sticky_proxy'] = self._bool_to_http(self.session_sticky_proxy)

        if self.debug is True:
            params['debug'] = self._bool_to_http(self.debug)

        if self.cache_clear is True:
            params['cache_clear'] = self._bool_to_http(self.cache_clear)

        if self.cache_ttl is not None:
            params['cache_ttl'] = self.cache_ttl

        if self.graphql:
            params['graphql_query'] = quote(self.graphql)

        if self.proxy_pool is not None:
            params['proxy_pool'] = self.proxy_pool

        if self.js:
            params['js'] = b64encode(self.js.encode('utf-8')).decode('utf-8')

        if self.rendering_wait:
            params['rendering_wait'] = self.rendering_wait

        return params

    @staticmethod
    def from_exported_config(config:str) -> 'ScrapeConfig':
        try:
            from msgpack import loads as msgpack_loads
        except ImportError as e:
            print('You must install msgpack package - run: pip install msgpack')
            raise

        data = msgpack_loads(base64.b64decode(config))

        headers = {}

        for name, value in data['headers'].items():
            if isinstance(value, Iterable):
                headers[name] = '; '.join(value)
            else:
                headers[name] = value

        return ScrapeConfig(
            url=data['url'],
            retry=data['retry'],
            headers=headers,
            session=data['session'],
            session_sticky_proxy=data['session_sticky_proxy'],
            cache=data['cache'],
            cache_ttl=data['cache_ttl'],
            cache_clear=data['cache_clear'],
            render_js=data['render_js'],
            method=data['method'],
            asp=data['asp'],
            body=data['body'],
            ssl=data['ssl'],
            dns=data['dns'],
            country=data['country'],
            debug=data['debug'],
            correlation_id=data['correlation_id'],
            tags=data['tags'],
            graphql=data['graphql_query'],
            js=data['js'],
            rendering_wait=data['rendering_wait'],
            screenshots=data['screenshots'] or {},
            proxy_pool=data['proxy_pool']
        )
