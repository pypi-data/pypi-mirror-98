from typing import Callable, Awaitable, Any, List
from asyncio import sleep
import importlib.resources as pkg_resources
import yaml
from aiohttp import web
from rororo import (
    OperationTableDef,
    setup_openapi,
)
from openapi_core.shortcuts import create_spec
from nteu_gateway.nteu_gateway_name import NTEU_GATEWAY_NAME
from nteu_gateway.nteu_gateway import NTEUGateway
from nteu_gateway.server_handler.translate import translate
from aiohttp.web import middleware


@middleware
async def default_index(request, handler):
    try:
        filename = request.match_info['filename']
        if not filename:
            filename = 'index.html'
        request.match_info['filename'] = filename
    except KeyError:
        pass
    return await handler(request)


class NTEUGatewayServer:
    def __init__(self, web_application: web.Application, site: web.TCPSite):
        self._web_application = web_application
        self._site = site

    def get_site(self):
        return self._site
    site = property(get_site)

    @staticmethod
    async def create(
            host: str,
            port: int,
            openapi: str,
            segmenter_host: str,
            segmenter_port: int,
            segmenter_use_white: bool,
            batch_size: int,
            max_concurrent_batches: int,
            src_lang: str,
            tgt_lang: str,
            translate_fn: Callable[[List[str]], Awaitable[None]]


    ) -> "NTEUGatewayServer":
        # Web app
        web_application = web.Application(client_max_size=1000000)

        # Inject nteu gateway in web application
        nteu_gateway = NTEUGateway(
            segmenter_host,
            segmenter_port,
            segmenter_use_white,
            batch_size,
            max_concurrent_batches,
            src_lang,
            tgt_lang,
            translate_fn
        )
        web_application[NTEU_GATEWAY_NAME] = nteu_gateway

        # Register startup handler
        web_application.on_startup.append(NTEUGatewayServer.initialize)

        # OpenAPI
        operations = OperationTableDef()
        operations.register(translate)

        with open(openapi) as f:
            openapi_schema = yaml.load(f, Loader=yaml.CSafeLoader)
        openapi_spec = create_spec(openapi_schema)

        web_application = setup_openapi(
            web_application,
            operations,
            schema=openapi_schema, spec=openapi_spec
        )

        web_application.add_routes([web.static('/', "static")])
        web_application.middlewares.append(default_index)

        # Site
        runner = web.AppRunner(web_application)
        await runner.setup()
        site = web.TCPSite(runner, host, port)

        return NTEUGatewayServer(web_application, site)

    @staticmethod
    async def initialize(web_application: web.Application):
        # Start ner APP
        await web_application[NTEU_GATEWAY_NAME].initialize()

    @staticmethod
    async def run(host: str,
                  port: int,
                  openapi: str,
                  segmenter_host: str,
                  segmenter_port: int,
                  segmenter_use_white: bool,
                  batch_size: int,
                  max_concurrent_batches: int,
                  src_lang: str,
                  tgt_lang: str,
                  translate_fn: Callable[[List[str]], Awaitable[None]]):

        # Create server
        server = await NTEUGatewayServer.create(
            host,
            port,
            openapi,
            segmenter_host,
            segmenter_port,
            segmenter_use_white,
            batch_size,
            max_concurrent_batches,
            src_lang,
            tgt_lang,
            translate_fn
        )

        await server.site.start()

        while True:
            await sleep(3600)