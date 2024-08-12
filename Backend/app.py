from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from neo4j_database import get_db, create_user
from routes.auth import auth_route
from routes.story import story_route
from routes.blog import blog_route
from routes.translation import translation_route

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
app.config['JWT_SECRET_KEY'] = 'super-secret'
app.config['GOOGLE_CLIENT_ID'] = '637746679388-lhhr7e2mc59u9iqp8mdvajthqko3gfdc.apps.googleusercontent.com'
jwt = JWTManager(app)

if __name__ == "__main__":
    # with app.app_context():
    #     db = get_db()
    #     results = db.write_transaction(create_user, "Milica", "Petkovic", "milica@elfak.rs", "123")
    
    app.register_blueprint(auth_route)
    app.register_blueprint(story_route)
    app.register_blueprint(blog_route, url_prefix="/blog")
    app.register_blueprint(translation_route, url_prefix="/translate")
    app.run(debug=True, port="5001")