import json

from rosetta_dispatcher.idtool import idtool
from rosetta_dispatcher.model.dispatch_response_model import DispatchResponseModel
from rosetta_dispatcher.model.dispatch_types import DispatchRequestType, DispatchResponseStatus
import aioredis


class AioDispatchClient(object):
    @classmethod
    async def create(cls, redis_host: str, redis_port: int):
        result = AioDispatchClient(redis_host, redis_port)
        result.pool = await aioredis.create_pool(
            f'redis://{redis_host}:{redis_port}', encoding='utf-8',
            minsize=1, maxsize=16)
        # result.redis = await aioredis.create_redis(f'redis://{redis_host}:{redis_port}', encoding='utf-8')
        return result

    def __init__(self, redis_host: str, redis_port: int):
        self.redis_host = redis_host
        self.redis_port = redis_port
        self.pool = None

    async def process(self, service_queue: str, data: str, timeout: int = 500):
        reply_to = idtool.gen_uuid()
        correlation_id = idtool.gen_uuid()
        request = {
            'content_type': DispatchRequestType.JSON,
            'reply_to': reply_to,
            'correlation_id': correlation_id,
            'timeout': timeout,
            'data': data
        }

        with await self.pool as conn:
            # with await self.pool as conn:  # low-level redis connection
            await conn.execute(b'RPUSH', service_queue, json.dumps(request, ensure_ascii=False))
            result = await conn.execute(b'BLPOP', reply_to, timeout)
            if result and result[0] == reply_to:
                response = DispatchResponseModel.parse_obj(json.loads(result[1]))
                if response.correlation_id == correlation_id and response.status == DispatchResponseStatus.OK:
                    return response.data
        return None
