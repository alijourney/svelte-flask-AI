import datetime
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from neo4j_database import get_db, get_categories, serialize_category, db_get_blogs, db_create_blog, db_add_category_to_blog, db_add_blog_to_user, serialize_blog, db_get_blogs_by_category

blog_route = Blueprint("blog", __name__)

@blog_route.route('/get-categories', methods=["GET"])
def get_all_categories():
    db = get_db()
    categories_record = db.read_transaction(get_categories)
    all_categories = []
    for cat in categories_record:
        all_categories.append(cat['category'])
    return jsonify({'categories': [serialize_category(x) for x in all_categories]}), 201

@blog_route.route("/", methods=["GET"])
def get_blogs():
    db = get_db()
    blogs_record = db.read_transaction(db_get_blogs)
    current_app.logger.info(blogs_record)
    all_blogs = []
    for blog in blogs_record:
        obj = {
            'blog': blog['blog'],
            'user': blog['user'],
            'category': blog['category'],
        }
        all_blogs.append(obj)
    
    return jsonify({'blogs': [serialize_blog(x) for x in all_blogs]}), 201

@blog_route.route("/category/<string:id>", methods=["GET"])
def get_blogs_by_category(id):
    db = get_db()
    blogs_record = db.read_transaction(db_get_blogs_by_category, id)
    current_app.logger.info(blogs_record)
    all_blogs = []
    for blog in blogs_record:
        obj = {
            'blog': blog['blog'],
            'user': blog['user'],
            'category': blog['category'],
        }
        all_blogs.append(obj)
    
    return jsonify({'blogs': [serialize_blog(x) for x in all_blogs]}), 201

@blog_route.route("/create-blog", methods=["POST"])
@jwt_required()
def create_blog():
    req = request.get_json()
    db = get_db()
    title = str(req['title'])
    text = str(req['text'])
    category_id = str(req['category_id'])
    new_blog = db.write_transaction(db_create_blog, title, text, datetime.datetime.now())
    db.write_transaction(db_add_category_to_blog, new_blog[0]['id'], category_id)
    db.write_transaction(db_add_blog_to_user, get_jwt_identity(), new_blog[0]['id'])

    return jsonify({'message': 'Blog created'}), 201

@blog_route.route("/", methods=["DELETE"])
def delete_blog():
    db = get_db()