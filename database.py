from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base, DeferredReflection
from sqlalchemy.orm import scoped_session, sessionmaker


connection_string = 'mysql://mytest:mytest@192.168.0.200:3306/testsp'

engine = create_engine(connection_string)

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base(cls=DeferredReflection)

Base.query = db_session.query_property()
