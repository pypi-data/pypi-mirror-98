import logging

import pyodbc

from .abstract import Abstract_DB
from soft_collect.config import settings as s

logger = logging.getLogger(__name__)


def get_default_driver():
    drivers = [dri for dri in pyodbc.drivers() if "SQL Server" in dri]
    return drivers[0]


class SQLServer(Abstract_DB):
    def select(self, sql):
        with self.set_up_connection() as conn:
            c = conn.cursor()
            c.execute(sql)
            row = c.fetchone()
            while row:
                yield row
                row = c.fetchone()

    def fetch_all(self, sql):
        with self.set_up_connection() as conn:
            c = conn.cursor()
            return c.execute(sql).fetchall()

    def set_up_connection(self, _retry=2):
        logger.info(f"Creating connection to SQL Server in {s.ip}")

        if not pyodbc.drivers():
            raise Exception("No SQL Server Driver found, please install it.")
        driver = "{" + s.get("DRIVER", get_default_driver()) + "}"

        conn_str = s.get("CONN_STR", None)

        credentials_kargs = {}
        if s.get("USER", None):
            credentials_kargs = {"user": s.user, "password": s.password}
        try:
            connection = pyodbc.connect(
                conn_str,
                driver=driver,
                server=s.ip,
                port=s.get("PORT", None),
                database=s.base,
                **credentials_kargs,
            )
        except BaseException as e:
            logger.error(f"Can't set up a connection with {s.ip}/{s.base}, {e}")
            if _retry:
                return self.set_up_connection(_retry - 1)
            raise e

        return connection
