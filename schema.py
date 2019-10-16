import graphene
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType
from models import *
from database import db_session

class Person(SQLAlchemyObjectType):

    class Meta:
        model = PersonModel
        interfaces = (graphene.relay.Node, )


class Article(SQLAlchemyObjectType):
  
    class Meta:
        model = ArticleModel
        interfaces = (graphene.relay.Node, )


class UpdatePerson(graphene.Mutation):
    class Arguments:
        uuid = graphene.Int()
        name = graphene.String()

    person = graphene.Field(Person)
    ok = graphene.Boolean()    

    def mutate(self, info, uuid, name):

        person = Person.get_query(info).get(uuid)
        person.name = name
        
        db_session.commit()

        ok = True
        return UpdatePerson(person=person, ok=ok)


class Query(graphene.ObjectType):
    
    node = graphene.relay.Node.Field()
    person = graphene.Field(Person, uuid = graphene.Int())
    people = graphene.List(Person)
    person_by_name = graphene.Field(Person, name = graphene.String(required=True))
    artical = graphene.Field(Article, uuid = graphene.Int())
    articals = graphene.List(Article, uuid = graphene.Int())
    
    def resolve_people(self, info):
        query = Person.get_query(info)

        return query.all()

    def resolve_person(self, info, uuid):
        query = Person.get_query(info)

        return query.get(uuid)

    def resolve_person_by_name(self, info, name):
        query = Person.get_query(info)        

        return query.filter_by(name=name).first()


    def resolve_artical(self, info, uuid):
        query = Article.get_query(info)

        return query.get(uuid)

    def resolve_articals(self, info, uuid):
        query = Article.get_query(info)

        return query.filter_by(person_id = uuid)


class Mutations(graphene.ObjectType):
    update_person_name = UpdatePerson.Field()


class MyMiddleWare(graphene.ObjectType):
    def resolve(next, root, info, **args):
        app.logger.info('ok')
        return next(root, info, **args)


schema = graphene.Schema(query=Query, mutation=Mutations)
