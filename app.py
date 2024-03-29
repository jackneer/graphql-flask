from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
from database import db_session, engine
from flask_graphql import GraphQLView
from schema import schema

app = Flask(__name__)
# db = SQLAlchemy(app)
app.debug = True

app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True, context={'session': db_session}))

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == '__main__':
    app.run()
