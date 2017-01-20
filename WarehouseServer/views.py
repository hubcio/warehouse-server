# -*- encoding: utf-8 -*-

from WarehouseServer import app, db, auth
from functools import wraps
from flask import abort, request, jsonify, g, url_for
from random import randint
from models import User


def requires_roles(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if get_current_user_role() not in roles:
                return error_response()
            return f(*args, **kwargs)

        return wrapped

    return wrapper


def get_current_user_role():
    return g.user.role


def error_response():
    return "You've got no permission to access this page.", 403


@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


@app.route('/api/warehouse/state', methods=['GET'])
def get_position():
    x = randint(0, 10000)
    y = randint(0, 10000)
    z = randint(0, 10000)
    cx = randint(0, 1000)
    cy = randint(0, 1000)
    cz = randint(0, 1000)
    state = "idle"
    data = {"x": x, "y": y, "z": z, "cx": cx, "cy": cy, "cz": cz, "state": state}

    return jsonify(data)


@app.route('/api/users/new', methods=['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    role = 'user'
    if username is None or password is None:
        abort(400)  # missing arguments
    if User.query.filter_by(username=username).first() is not None:
        abort(400)  # existing user
    user = User(username=username, role=role)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return (jsonify({'username': user.username}), 201,
            {'location': url_for('get_user', id=user.id, _external=True)})


@app.route('/api/users/all', methods=['GET'])
@auth.login_required
@requires_roles('admin')
def get_all_users():
    cols = ['id', 'username', 'role']
    data = User.query.all()
    users = [{col: getattr(d, col) for col in cols} for d in data]
    return jsonify(users=users)


@app.route('/api/users/<int:id>', methods=['GET', 'DELETE'])
@auth.login_required
@requires_roles('admin')
def get_user(id):
    if request.method == 'GET':
        user = User.query.get(id)
        if not user:
            abort(400)
        return jsonify({'username': user.username})
    elif request.method == 'DELETE':
        user = User.query.get(id)
        if not user or id == 1:
            abort(400)
        User.query.filter(User.id == id).delete()
        db.session.commit()
        return jsonify({'username': user.username})


@app.route('/api/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token(600)
    return jsonify({'token': token.decode('ascii'), 'duration': 600})


@app.route('/api/resource')
@auth.login_required
def get_resource():
    return jsonify({'data': 'Hello, %s!' % g.user.username})
