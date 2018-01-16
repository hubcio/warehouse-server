# -*- encoding: utf-8 -*-

from WarehouseServer import app, db, auth, com, auto, servo, logic
from functools import wraps
from flask import abort, request, jsonify, g, url_for

from models import User, Drawer
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


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
@auto.doc()
def get_position():
    state = com.state
    data = {"x": com.x_pos_fdb,
            "y": com.y_pos_fdb,
            "z": com.z_pos_fdb,
            "cx": com.x_current,
            "cy": com.y_current,
            "cz": com.z_current,
            "servo": servo.get_position(),
            "state": state}
    return jsonify(data)


@app.route('/api/warehouse/rfid')
@auto.doc()
def read_rfid():
    card_data = 'NaN'
    print(card_data)
    return jsonify({'rfid_id': card_data})


@app.route('/api/warehouse/move/absolute/x/<int:value>', methods=['GET'])
@auto.doc()
def move_x_absolute(value):
    com.move_x_absolute(value)
    return get_position()


@app.route('/api/warehouse/move/absolute/y/<int:value>', methods=['GET'])
@auto.doc()
def move_y_absolute(value):
    com.move_y_absolute(value)
    return get_position()


@app.route('/api/warehouse/move/absolute/z/<int:value>', methods=['GET'])
@auto.doc()
def move_z_absolute(value):
    com.move_z_absolute(value)
    return get_position()


@app.route('/api/warehouse/move/relative/x/<int:value>', methods=['GET'])
@auto.doc()
def move_x_relative(value):
    com.move_x_relative(value)
    return get_position()

@app.route('/api/warehouse/move/relative/x/-<int:value>', methods=['GET'])
def move_x_relative_decrement(value):
    com.move_x_relative(-value)
    return get_position()

@app.route('/api/warehouse/move/relative/y/<int:value>', methods=['GET'])
@auto.doc()
def move_y_relative(value):
    com.move_y_relative(value)
    return jsonify({'success': True})


@app.route('/api/warehouse/move/relative/y/-<int:value>', methods=['GET'])
def move_y_relative_decrement(value):
    com.move_y_relative(-value)
    return get_position()


@app.route('/api/warehouse/move/relative/z/<int:value>', methods=['GET'])
@auto.doc()
def move_z_relative(value):
    com.move_z_relative(value)
    return get_position()

@app.route('/api/warehouse/move/relative/z/-<int:value>', methods=['GET'])
def move_z_relative_decrement(value):
    com.move_z_relative(-value)
    return get_position()


@app.route('/api/warehouse/home/x', methods=['GET'])
@auto.doc()
def home_x():
    com.home_x()
    return get_position()


@app.route('/api/warehouse/home/y', methods=['GET'])
@auto.doc()
def home_y():
    com.home_y()
    return get_position()


@app.route('/api/warehouse/home/z', methods=['GET'])
@auto.doc()
def home_z():
    com.home_z()
    return get_position()

@app.route('/api/warehouse/move/absolute/servo/<int:value>', methods=['GET'])
@auto.doc()
def move_servo(value):
    """Set servo position to absolute percent value"""
    servo.move_percent(value)
    return get_position()

@app.route('/api/warehouse/move/test1', methods=['GET'])
@auto.doc()
def move_test():
    com.move_x_relative(3000, True)
    com.move_z_relative(3000, True)
    com.move_x_relative(-2800)
    com.move_z_relative(-2800)

    return get_position()


@app.route('/api/drawers/mine', methods=['GET'])
@auto.doc()
@auth.login_required
@requires_roles('admin', 'user')
def show_current_user_drawers():
    """Show drawers that belong to requesting user"""
    cols = ['drawer_id', 'description_short', 'description_long', 'rfid_id']
    data = Drawer.query.filter(Drawer.users.any(user_id=g.user.user_id)).all()
    drawers = [{col: getattr(d, col) for col in cols} for d in data]
    return jsonify(drawers=drawers)


@app.route('/api/drawers/all', methods=['GET'])
@auto.doc()
@auth.login_required
@requires_roles('admin')
def show_all_drawers():
    """Return all drawers"""
    cols = ['drawer_id', 'description_short', 'description_long', 'rfid_id']
    data = Drawer.query.all()
    drawers = [{col: getattr(d, col) for col in cols} for d in data]
    return jsonify(drawers=drawers)


@app.route('/api/drawers/<int:drawer_id>', methods=['PUT', 'POST', 'DELETE'])
@auto.doc()
@auth.login_required
@requires_roles('admin', 'user')
def drawer_handler(drawer_id):
    if request.method == 'PUT':
        # TODO putting handler
        return
    if request.method == 'POST':
        # TODO going for existing drawer scenario

        return
    if request.method == 'DELETE':
        # TODO going for drawer and making it empty
        return


@app.route('/api/drawers/new', methods=['POST'])
@auto.doc()
@auth.login_required
@requires_roles('admin', 'user')
def new_drawer():
    description_short = request.json.get('description_short')
    if description_short is None:
        return error_response()

    drawer = Drawer()
    drawer.description_short = description_short
    drawer.date_modified = datetime.utcnow()
    drawer.is_empty = 0

    current_user = User.query.get(g.user.user_id)  # get current user
    current_user.drawers.append(drawer)  # and assign that drawer to him

    db.session.add(current_user)
    db.session.commit()

    cols = ['drawer_id', 'description_short', 'description_long', 'rfid_id']
    data = Drawer.query.filter(Drawer.users.any(user_id=g.user.user_id)).all()
    drawers = [{col: getattr(d, col) for col in cols} for d in data]
    return jsonify(drawers=drawers)


@app.route('/api/users/new', methods=['POST'])
@auto.doc()
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    role = 'user'
    if username is None or password is None:
        return error_response()
    if User.query.filter_by(username=username).first() is not None:
        abort(400)  # existing user
    user = User(username=username, role=role)
    user.hash_password(password)
    user.date = datetime.utcnow()
    db.session.add(user)
    db.session.commit()
    return (jsonify({'username': user.username}), 201,
            {'location': url_for('get_user', user_id=user.user_id, _external=True)})


@app.route('/api/users/all', methods=['GET'])
@auto.doc()
@auth.login_required
@requires_roles('admin')
def get_all_users():
    cols = ['user_id', 'username', 'role', 'date']
    data = User.query.all()
    users = [{col: getattr(d, col) for col in cols} for d in data]
    return jsonify(users=users)


@app.route('/api/users/<int:user_id>', methods=['GET', 'DELETE'])
@auto.doc()
@auth.login_required
@requires_roles('admin')
def get_user(user_id):
    """GET info about user or DELETE user"""
    if request.method == 'GET':
        user = User.query.get(user_id)
        if not user:
            abort(400)
        return jsonify({'username': user.username})
    elif request.method == 'DELETE':
        user = User.query.get(user_id)
        if not user or user_id == 1:
            abort(400)
        User.query.filter(User.user_id == user_id).delete()
        db.session.commit()
        return jsonify({'username': user.username})


@app.route('/api/users/token')
@auto.doc()
@auth.login_required
@requires_roles('admin', 'user')
def get_auth_token():
    """Returns valid token."""
    token = g.user.generate_auth_token(600)
    return jsonify({'token': token.decode('ascii'), 'duration': 600})


@app.route('/api/doc', methods=['GET'])
def documentation():
    return auto.html()
