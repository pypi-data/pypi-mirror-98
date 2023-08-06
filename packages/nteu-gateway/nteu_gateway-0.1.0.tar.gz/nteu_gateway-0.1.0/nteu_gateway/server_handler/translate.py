import asyncio
from nteu_gateway.logger import logger
from aiohttp import web
from rororo import openapi_context
from nteu_gateway.nteu_gateway_name import NTEU_GATEWAY_NAME
from nteu_gateway.nteu_gateway import NTEUGateway
from pyrsistent import thaw
from itertools import groupby


async def translate(request: web.Request) -> web.Response:
    try:
        # Gateway
        nteu_gateway: NTEUGateway = request.app[NTEU_GATEWAY_NAME]

        # Num Request
        request_id = nteu_gateway.create_request_id()
        logger.info(f'Handling translation request {request_id}')

        # Read request params
        with openapi_context(request) as context:
            texts = thaw(context.data.texts)
            priority = context.data.priority

        # Create translation_tasks
        translation_tasks, segmentation_masks = await asyncio.shield(
            nteu_gateway.create_translation_tasks(texts, priority, request_id))
        logger.info(f'Translation request {request_id} converted to {len(translation_tasks)} translation task(s)')

        # Wait
        for done in [task.done for task in translation_tasks]:
            await done.wait()

        # Check for error
        for task in translation_tasks:
            if task.error is not None:
                return web.Response(status=500, body=str(task.error))

        # Output
        translations = []
        for group, task_group in groupby(translation_tasks, key=lambda t: t.group):
            translation = segmentation_masks[group].format(*list(map(lambda x: x.translation, task_group)))
            translations.append({
                "text": texts[group],
                "translation": translation
            })

        logger.info(f'Request {request_id} done')

        return web.json_response({
            "translations": translations
        })
    except asyncio.CancelledError:
        try:
            for task in translation_tasks:
                nteu_gateway.remove_task(task)
        except NameError:
            pass
        return web.Response(status=499)
















