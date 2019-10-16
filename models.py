from sqlalchemy import Column, Integer, ForeignKey, String, Text
from sqlalchemy.orm import relationship
from database import Base, engine


class PersonModel(Base):
    __tablename__ = 'person'
    uuid = Column(Integer, primary_key=True)
    name = Column(String(50))
    age = Column(Integer)
    Articles = relationship("ArticleModel")
    
    
class ArticleModel(Base):
    __tablename__ = 'article'
    uuid = Column(Integer, primary_key=True)
    person_id = Column(ForeignKey("person.uuid"))
    title = Column(String(100))
    content = Column(Text)


# Base.metadata.drop_all(engine)
# Base.metadata.create_all(engine)

Base.prepare(engine)

