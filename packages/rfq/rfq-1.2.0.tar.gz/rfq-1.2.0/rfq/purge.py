from typing import Optional, List, Union, Literal

from redis import Redis, WatchError

import rfq.redis


def purge(topic: str, queue: Union[Literal["backlog"], Literal["nextlog"]], redis: Optional[Redis] = None) -> List[str]:
    r = rfq.redis.default() if redis is None else redis

    msgids = []

    with r.pipeline() as p:
        while True:
            try:
                p.watch("rfq:{topic}:{queue}".format(topic=topic, queue=queue))

                msgid = p.lrange("rfq:{topic}:{queue}".format(topic=topic, queue=queue), -1, -1)

                if not msgid:
                    break

                msgid = msgid[0]

                p.multi()

                p.rpop("rfq:{topic}:{queue}".format(topic=topic, queue=queue))
                p.delete("rfq:{topic}:message:{msgid}".format(topic=topic, msgid=msgid))

                msgid = p.execute()[0]

                msgids.append(msgid)

            except WatchError:
                continue

    return msgids
