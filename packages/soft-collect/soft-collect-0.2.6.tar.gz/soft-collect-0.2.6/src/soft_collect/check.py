# TODO Use this file to validate S3, DB and CAS Connection
from .cas import CAS
from .config import settings
from .db import get_DB_client
from .save import get_save_client


def check_s3():
    print("Checking S3 connection...")
    get_save_client("s3")


def check_db():
    print("Checking DB connection...")
    get_DB_client(settings.dbm)


def check_cas():
    print("Checking CAS connection")
    CAS(save="local", **settings.cas).head()


def check_all(s3=True, db=True, cas=True):
    if s3:
        check_s3()
    if db:
        check_db()
    if cas:
        check_cas()
