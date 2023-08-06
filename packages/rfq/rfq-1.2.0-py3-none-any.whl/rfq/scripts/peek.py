import sys
import json

from rfq.rfq import Queue


def main(args):
    topic = args.topic
    msgid = args.msgid

    q = Queue()

    msg = q.peek(topic=topic, msgid=msgid)

    if not msg:
        sys.exit(1)

    print(json.dumps(msg))
