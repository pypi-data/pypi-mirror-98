import asyncio
import functools
import io
import logging
from concurrent.futures import ThreadPoolExecutor

import pandas as pd
from rich.progress import Progress

from .cas import CAS
from .config import settings
from .db import get_DB_client
from .models.objects import ObjResult
from .save import get_save_client

logger = logging.getLogger(__name__)


class Collect:
    def __init__(self, save):
        self.sh = get_save_client(save)
        self.db = get_DB_client(settings.dbm)

        if settings.get("CAS", None):
            self.cas = CAS(save=save, **settings.cas)
        else:
            self.cas = None

    async def run(self, classes):
        if isinstance(classes, str):
            classes = [row for row in self.get_rows(level="CLASSES", sql=classes)]

        loop = asyncio.get_event_loop()
        executor = ThreadPoolExecutor(200)
        with Progress() as p:
            class_task = p.add_task("[red]CLASSES", total=len(classes))
            await asyncio.gather(
                *[
                    loop.run_in_executor(
                        executor,
                        functools.partial(
                            self.parallel_classes, p, class_task, cdclass
                        ),
                    )
                    for cdclass in classes
                ]
            )

    def parallel_classes(self, progress, task, cdclass):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        executor = ThreadPoolExecutor(200)

        logger.info(f"Getting documents for class {cdclass}")
        parallel_docs = asyncio.gather(
            *[
                loop.run_in_executor(
                    executor, functools.partial(self.parallel_docs, doc, cdclass),
                )
                for doc in self.get_rows(cdclass)
            ]
        )
        loop.run_until_complete(parallel_docs)
        logger.info(f"Finished class {cdclass}")
        progress.advance(task)

    def parallel_docs(self, doc, cdclass):
        logger.info(f"Getting key {doc} in class {cdclass}")
        if doc:
            self.get_objects(doc, cdclass)
        else:
            logger.error(f"Empty key in class {cdclass}, it will be ignored")

    def get_objects(self, key, cdclass):
        if self.sh.check_obj(cdclass, key):
            logger.info(f"Object {key} already exists")
            return True
        for row in self.db.get_objects(key):
            result = ObjResult(*row)
            if result.idcas and self.cas:
                logger.info(
                    f"CAS: id={result.idcas.strip()}, {cdclass}, {result.key}, {result.part}"
                )
                # loop = asyncio.get_event_loop()
                # result.obj = loop.run_until_complete(
                #     self.cas.retrieve_obj(result.idcas)
                # )
            if result.obj:
                self.sh.save_obj(
                    io.BytesIO(result.obj).read(), cdclass, result.key, result.part
                )
            else:
                logger.error(
                    f"The key {result.key} has a empty file in part {result.part}, it will be ignored"
                )

    def get_rows(self, cdclass=None, level="DOCS", sql=None):
        if not sql:
            sql = settings.keys_sql
        if not cdclass:
            cdclass = sql
        exists, docs = self.sh.check_meta(f"{level}_LIST_{cdclass}")
        if exists:
            logger.info(f"List of rows for {cdclass} already exists")
            docs.dropna(inplace=True)
            yield from [doc[0] for _, doc in docs.iterrows()]
        else:
            rows = self.db.get_rows(sql, format={"CLASSE": cdclass})
            rows = [row[0] for row in rows]
            df = pd.DataFrame(rows).dropna()
            self.sh.save_meta(df, f"{level}_LIST_{cdclass}")
            yield from rows
