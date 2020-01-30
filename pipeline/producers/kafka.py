import asyncio
import logging
import json

from aiokafka import AIOKafkaProducer

from pipeline import settings
from .base import Producer


log = logging.getLogger(__name__)


class KafkaProducer(Producer):
    async def connect(self) -> None:
        log.debug('Connecting to Kafka stream.')
        self.producer = AIOKafkaProducer(
            loop=self.loop,
            bootstrap_servers=self.hosts
        )
        await self.producer.start()
        self.connected = True

    async def disconnect(self) -> None:
        await self.producer.stop()
        self.connected = False

    async def produce_message(self, message: dict, topic: str=None) -> None:
        log.debug('Trying to produce message: {msg}'.format(msg=message))

        if not self.connected:
            log.debug('Producer not connected')
            return

        await super().produce_message(message=message, topic=topic)
        await self.producer.send_and_wait(topic, json.dumps(message).encode())