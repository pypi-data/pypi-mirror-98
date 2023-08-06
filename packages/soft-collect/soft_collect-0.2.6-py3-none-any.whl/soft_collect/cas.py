import asyncio
import logging
import socket
from typing import Union

import httpx

from .save import get_save_client


logger = logging.getLogger(__name__)
# TODO Print progress and change the saving path


class CAS:
    def __init__(
        self,
        save,
        host,
        port,
        username,
        password,
        protocol="http",
        context="/spsmb/ibm/ia",
    ) -> None:
        self.host = host
        self.port = port
        self.BASE_URL = f"{protocol}://{host}:{port}{context}"
        auth = (username, password)
        headers = {
            "content-type": "application/octet-stream",
            "User-Agent": "Softplan Broker Client v1.0",
        }
        limits = httpx.Limits(max_keepalive_connections=5, max_connections=10)
        self.client = httpx.AsyncClient(
            auth=auth, headers=headers, base_url=self.BASE_URL, limits=limits
        )

        self.sh = get_save_client(save)

    def head(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)

        try:
            s.connect((self.host, int(self.port)))
            s.shutdown(socket.SHUT_RD)
            return True

        # Connection Timed Out
        except socket.timeout:
            print("Connection timed out!")
            return False
        except OSError as e:
            print("OS Error:", e)
            return False

    async def retrieve_obj(self, id: str) -> bytes:
        RETRIEVE_OP = "/doRetrieve"

        async with self.client as client:
            logger.info(f"Requesting for file in CAS {id=}")
            res = await client.get(f"{RETRIEVE_OP}?id={id}")

        return res.content

    async def retrive_list_objs(self, list_ids: list) -> list:
        task_list = []
        for id, classe, key, part in list_ids:
            task_list.append(self.save_obj(id, classe, key, part))

        return await asyncio.gather(*task_list)

    async def save_obj(self, id, classe, key, part):
        obj = await self.retrieve_obj(id)
        self.sh.save_obj(obj, classe, key, part)

    async def run(self, ids: Union[str, list]):
        exec_function = {str: self.save_obj, list: self.retrive_list_objs}

        await exec_function[type(ids)](ids)
