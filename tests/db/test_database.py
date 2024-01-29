import pytest
from sqlalchemy import text
from sqlalchemy.orm import Session

from db.database import get_session, engine, Base


class TestDatabase:
    def test_get_session(self):
        with get_session() as sess:
            print(sess)
            print(type(sess))
            assert sess is not None
            assert isinstance(sess, Session)

    def test_tables_are_registered(self):
        assert 'brand' in Base.metadata.tables
        assert 'product' in Base.metadata.tables

    def test_create_tables(self):
        Base.metadata.create_all(bind=engine)
        session = get_session()
        # if database is not sqlite, use this
        if 'sqlite' not in str(engine.url):
            result = session.execute(text('show tables'))
        else:
            result = session.execute(text('select name from sqlite_master where type = "table"'))
        tables = [row[0] for row in result]
        print(tables)
        assert 'brand' in tables
        assert 'product' in tables


if __name__ == '__main__':
    pytest.main(['-s', 'test_database.py'])
