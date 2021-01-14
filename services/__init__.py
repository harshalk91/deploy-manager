from sqlalchemy import orm
from db_queries import engine

def read_only_queries():
    sm = orm.sessionmaker(bind=engine, autoflush=True, autocommit=False, expire_on_commit=True)
    db_session = orm.scoped_session(sm)
    db_session.close()

def read_write_queries():
    sm = orm.sessionmaker(bind=engine, autoflush=True, autocommit=False, expire_on_commit=True)
    db_session = orm.scoped_session(sm)
    db_session.commit()
    db_session.close()

