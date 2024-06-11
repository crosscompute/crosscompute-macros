from pathlib import Path

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.types import String, TypeDecorator

from .security import hash_text


class EncryptedString(TypeDecorator):
    impl = String
    cache_ok = False
    encoding = 'utf-8'
    context = None

    def process_bind_param(self, value, dialect):
        if not value:
            return
        encoded_value = bytes(value, encoding=self.encoding)
        return self.context.encrypt(encoded_value)

    def process_result_value(self, value, dialect):
        if not value:
            return
        encoded_value = self.context.decrypt(value)
        return bytes.decode(encoded_value, encoding=self.encoding)


class HashedString(TypeDecorator):
    impl = String
    cache_ok = False

    def process_bind_param(self, value, dialect):
        if not value:
            return
        return hash_text(value)

    def process_result_value(self, value, dialect):
        return value


def get_database_engine(database_uri):
    if database_uri.startswith('sqlite') and not database_uri.endswith('://'):
        database_path = Path(database_uri.split(':///', maxsplit=1)[1])
        database_folder = database_path.parent
        database_folder.mkdir(parents=True, exist_ok=True)
    return create_async_engine(database_uri)


def define_get_database_session(database_engine):
    return async_sessionmaker(
        database_engine,
        autoflush=False,
        expire_on_commit=False)


async def make_tables(database_engine, database_metadata):
    async with database_engine.begin() as database_connection:
        await database_connection.run_sync(database_metadata.create_all)
