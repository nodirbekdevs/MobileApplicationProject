from databases import Database
from sqlalchemy import MetaData
from ormar import ModelMeta

from .config import DB_DIALECT

metadata = MetaData()
database = Database(DB_DIALECT)


class BaseMeta(ModelMeta):
    database = database
    metadata = metadata
