from typing import List
import traceback
import aiohttp
from itertools import product, chain, count
from nteu_gateway.translation_task import TranslationTask
import asyncio
from nteu_gateway.translation_task_priority_queue import TranslationTaskPriorityQueue
from nteu_gateway.utils.chunks import chunks
from nteu_gateway.logger import logger


class NTEUGateway:
    def __init__(self, segmenter_host: str,
                 segmenter_port: int,
                 segmenter_use_white: bool,
                 batch_size: int,
                 max_concurrent_batches: int,
                 src_lang: str,
                 tgt_lang: str,
                 translate_fn):

        self._segmenter_host = segmenter_host
        self._segmenter_port = segmenter_port
        self._segmenter_use_white = segmenter_use_white
        self._batch_size = batch_size
        self._max_concurrent_batches = max_concurrent_batches
        self._src_lang = src_lang
        self._tgt_lang = tgt_lang
        self._translate_fn = translate_fn

        self._translation_task_queue: TranslationTaskPriorityQueue = TranslationTaskPriorityQueue()
        self._processing_batches: int = 0
        self._translation_engine_feeder_task = None

        self._request_id = 0
        self._batch_id = 0

    def create_request_id(self):
        self._request_id += 1
        return self._request_id

    async def create_translation_tasks(self, texts: List[str], priority: int, request_id: int):
        # Segmentation
        url = f'http://{self._segmenter_host}:{self._segmenter_port}/segment'
        data = {
            'lang': self._src_lang,
            'texts': texts,
            'use_white_segmenter': self._segmenter_use_white
        }

        groups = []
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data) as response:
                if response.status == 200:
                    results = await response.json()
                    for result in results:
                        segments = result["segments"]
                        mask = result['mask']
                        groups.append((segments, mask))

        tasks = []
        masks = []
        for i, group in enumerate(groups):
            segments = group[0]
            for j, segment in enumerate(segments):
                task = TranslationTask(segment, i, j, priority, request_id)
                tasks.append(task)
            mask = group[1]
            masks.append(mask)

        # Add task to the queue
        for task in tasks:
            self._translation_task_queue.add_task(task)

        return tasks, masks

    async def _run_translation_engine_feeder(self):
        while True:
            # Extracts task to translate
            max_batches = self._max_concurrent_batches - self._processing_batches
            max_tasks = max_batches * self._batch_size
            tasks = []
            while len(tasks) < max_tasks:
                try:
                    task = self._translation_task_queue.pop_task()
                    tasks.append(task)
                except Exception:
                    break

            # Create the batches
            batches = chunks(tasks, self._batch_size)
            batches = list(batches)

            # Update processing_batches counter
            self._processing_batches = self._processing_batches + len(batches)

            # Create a task for each batch to translate
            for batch in batches:
                asyncio.create_task(self._translate_batch(batch))

            await asyncio.sleep(0.1)

    async def _translate_batch(self, tasks: List[TranslationTask]):
        self._batch_id += 1
        batch_id = self._batch_id

        info = "\n".join([f' - request: {t.request_id}, text: {t.group}, segment: {t.index_in_group}: {t.text}'
                          for t in tasks])
        logger.info(f'Send batch {batch_id} of {len(tasks)} translation task(s): \n{info}')
        try:
            texts = list(map(lambda t: t.text, tasks))
            translations = await self._translate_fn(texts)
            for task, translation in zip(tasks, translations):
                task.translation = translation

        except Exception as e:
            tb = traceback.format_exc()
            tb_str = str(tb)
            for task in tasks:
                # TODO
                task.error = "Error", tb_str

        self._processing_batches -= 1
        logger.info(f'Translated batch xxx {batch_id}')

        # task done events
        for task in tasks:
            task.done.set()

    def remove_task(self, task: TranslationTask):
        self._translation_task_queue.remove_task(task)

    async def initialize(self):
        self._translation_engine_feeder_task = asyncio.create_task(self._run_translation_engine_feeder())
