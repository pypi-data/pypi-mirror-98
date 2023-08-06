from typing import Optional, Dict
import uuid
import random

from redis import Redis

import rfq.redis


def publish(topic: str, message: Dict[str, str], front: bool, redis: Optional[Redis] = None) -> str:
    r = rfq.redis.default() if redis is None else redis

    # https://github.com/python/cpython/blob/ba251c2ae6654bfc8abd9d886b219698ad34ac3c/Lib/uuid.py#L599-L612
    node = random.getrandbits(48) | (1 << 40)

    msgid = uuid.uuid1(node=node).hex

    with r.pipeline() as tx:
        tx.hset("rfq:{topic}:message:{msgid}".format(topic=topic, msgid=msgid), mapping=message)

        if front:
            tx.rpush("rfq:{topic}:backlog".format(topic=topic), msgid)
        else:
            tx.lpush("rfq:{topic}:backlog".format(topic=topic), msgid)

        tx.execute()

    return msgid
