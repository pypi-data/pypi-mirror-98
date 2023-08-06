from typing import Optional, Dict

from redis import Redis

import rfq.redis


def peek(topic: str, msgid: str, redis: Optional[Redis] = None) -> Dict[str, str]:
    r = rfq.redis.default() if redis is None else redis

    msg = r.hgetall("rfq:{topic}:message:{msgid}".format(topic=topic, msgid=msgid))

    if not msg:
        return None

    return msg
