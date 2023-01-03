import time
import uuid

import cassandra.util


def convert_text_into_uuid(uuid_txt: str):
    return uuid.UUID(uuid_txt)


def generate_uuid() -> uuid.UUID:
    return cassandra.util.uuid_from_time(time.time())


def convert_uuid_into_text(uuid_arg: uuid.UUID) -> str:
    return str(uuid_arg)
