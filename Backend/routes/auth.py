from flask import Blueprint, request, jsonify, current_app
from neo4j_database import check_password, create_user, get_db, get_user_by_email, get_user_by_id, serialize_user
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, decode_token
from google.oauth2 import id_token

auth_route = Blueprint("auth", __name__)

@auth_route.route("/auth/login", methods=["POST"])
def login():
    req = request.get_json()
    email = str(req["email"])
    password_candidate = str(req["password"])
    if not email:
        return {"email": "This field is required."}, 400

    if not password_candidate:
        return {"password": "This field is required."}, 400
    
    db = get_db()

    result = db.read_transaction(get_user_by_email, email)

    if not result:
        return jsonify({"message":"The email you entered isn't connected to an account."}), 422
    existing_user = result["user"]

    if check_password(existing_user, password_candidate):
        access_token = create_access_token(identity=existing_user["id"])
        resp = jsonify({'message': 'Uspešno prijavljivanje', 'user': serialize_user(existing_user), 'access_token' : access_token})
        resp.set_cookie('accessToken', access_token, httponly=True, max_age=1000*60*60*24)
        return resp, 200
    else:
        return jsonify({"message":"Wrong data"}), 422


@auth_route.route("/auth/register", methods=["GET", "POST"])
def register():
    req = request.get_json()
    current_app.logger.info(req)
    name = str(req["name"])
    lastname = str(req["lastname"])
    email = str(req["email"])
    password = str(req["password"])

    # Check if fields are empty

    if not name:
        return {"name": "This field is required."}, 400

    if not lastname:
        return {"lastname": "This field is required."}, 400

    if not email:
        return {"email": "This field is required."}, 400

    if not password:
        return {"password": "This field is required."}, 400

    # Check if email already exists

    db = get_db()

    result = db.read_transaction(get_user_by_email, email)
    if result:
        return jsonify({"message": "Email is already in use."}), 422

    # Create user

    results = db.write_transaction(create_user, name, lastname, email, password, "staff", "local")
    user = results["user"]
    current_app.logger.info(user)
    return serialize_user(user), 201

@auth_route.route('/auth/google', methods=['POST'])
def google_login():
    req = request.get_json()
    current_app.logger.info(req)
    token = str(req["token"])
    try:
        id_info = id_token.verify_token(
            token, request, current_app.config['GOOGLE_CLIENT_ID']
        )
    except Exception as e:
        current_app.logger.info(e)
        return jsonify({ 'message':"Google user not authenticated" })
    current_app.logger.info(id_info)
    return jsonify({ 'message':"Google user authenticated" })


@auth_route.route('/auth/current-user', methods=['GET'])
@jwt_required()
def current_user():
    user_id = get_jwt_identity()
    db = get_db()
    results = db.read_transaction(get_user_by_id, user_id)
    user = results["user"]
    if user is None:
        return 404
    else:
        return jsonify(serialize_user(user)), 200

