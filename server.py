import os
import sys

sys.path.append(os.getcwd())

from flask import Flask, render_template, request, jsonify, json, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, current_user
from services.authentication import OAuthSignIn
from models.user_model import UserModel
from models.base_model import DBSingleton

app = Flask(__name__)

login_manager = LoginManager(app)
login_manager.login_view = 'index'


@app.before_first_request
def initialize_tables():
    connect_db()
    if not UserModel.table_exists():
        UserModel.create_table()
    disconnect_db()


@app.before_request
def connect_db():
    DBSingleton.getInstance().connect()


@app.teardown_request
def disconnect_db(err=None):
    DBSingleton.getInstance().close()


@login_manager.user_loader
def load_user(id):
    return UserModel.get(UserModel.id == int(id))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()


@app.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    social_id, username, email = oauth.callback()
    if social_id is None:
        flash('Authentication failed.')
        return redirect(url_for('index'))
    user = UserModel.get(UserModel.social_id == social_id)
    if not user:
        user = UserModel.create(social_id=social_id, username=username, email=email, password="test_sikriit",
                                is_active=True)
    login_user(user, True)
    return redirect(url_for('index'))


@app.route('/users/', methods=['POST'])
def add_user():
    encoded_json = jsonify(request.form)
    decoded_json = json.loads(encoded_json.data)

    if 'is_active' in decoded_json:
        decoded_json['is_active'] = (decoded_json['is_active'].lower() == 'true')
    print('decoded_json is: {}'.format(decoded_json))
    # print('decoded_json[is_true]: {}, type: {}'.format(decoded_json['is_true'],
    #                                                    type(decoded_json['is_true'])))  # for debugging
    new_user = UserModel(**decoded_json)
    if new_user.save() != 1:
        return jsonify({'response': {'status_code': 400,
                                     'status_text': 'error',
                                     'message': 'creating new record',
                                     'data': decoded_json}})
    decoded_json['id'] = new_user.id
    return jsonify({'response': {'status_code': 200,
                                 'status_text': 'success',
                                 'message': 'creating new record',
                                 'data': decoded_json}})


@app.route('/users/<int:_id>', methods=['GET'])
def get_fact(_id):
    query = UserModel.select().where(UserModel.id == _id)
    if query.count() != 1:
        return jsonify({'response': {'status_code': 400,
                                     'status_text': 'error',
                                     'message': 'fetching record',
                                     'data': {'id': _id}}})
    else:
        user_record = query.get()
        return jsonify({'response': {'status_code': 200,
                                     'status_text': 'success',
                                     'message': 'fetching record',
                                     'data': {'id': user_record.id,
                                              'username': user_record.username,
                                              'usersecret': user_record.usersecret,
                                              'is_active': user_record.is_active,
                                              'created_on': user_record.timestamp}}})


@app.route('/users/', methods=['GET'])
def get_users():
    query = UserModel.select()
    if query.count() >= 1:
        all_users = {}
        for user_record in query.iterator():
            all_users[user_record.id] = {'username': user_record.username,
                                         'usersecret': user_record.usersecret,
                                         'is_active': user_record.is_active,
                                         'created_on': user_record.timestamp}

        return jsonify({'response': {'status_code': 200,
                                     'status_text': 'success',
                                     'message': 'fetching all records',
                                     'data': all_users}})
    return jsonify({'response': {'status_code': 400,
                                 'status_text': 'error',
                                 'message': 'fetching all records',
                                 'data': 'No Record Found'}})


@app.route('/users/<int:_id>', methods=['PUT'])
def update_user(_id):
    encoded_json = jsonify(request.form)
    decoded_json = json.loads(encoded_json.data)

    if 'is_active' in decoded_json:
        decoded_json['is_active'] = (decoded_json['is_active'].lower() == 'true')
    print('decoded_json is: {}'.format(decoded_json))
    # print('decoded_json[is_true]: {}, type: {}'.format(decoded_json['is_true'],
    #                                                    type(decoded_json['is_true'])))  # for debugging

    query = UserModel.update(**decoded_json).where(UserModel.id == _id)
    if query.execute() < 1:
        decoded_json['id'] = _id
        return jsonify({'response': {'status_code': 400,
                                     'status_text': 'error',
                                     'message': 'updating record',
                                     'data': decoded_json}})
    decoded_json['id'] = _id
    return jsonify({'response': {'status_code': 200,
                                 'status_text': 'success',
                                 'message': 'updating record',
                                 'data': decoded_json}})


@app.route('/users/<int:_id>', methods=['DELETE'])
def delete_fact(_id):
    query = UserModel.select().where(UserModel.id == _id)
    if query.count() != 1:
        return jsonify({'response': {'status_code': 400,
                                     'status_text': 'error',
                                     'message': 'deleting record: record not found',
                                     'data': {'id': _id}}})
    user_record = query.get()
    if user_record.delete_instance() != 1:
        return jsonify({'response': {'status_code': 400,
                                     'status_text': 'error',
                                     'message': 'deleting record',
                                     'data': {'id': _id}}})
    return jsonify({'response': {'status_code': 200,
                                 'status_text': 'success',
                                 'message': 'deleting record',
                                 'data': {'id': user_record.id,
                                          'username': user_record.username,
                                          'usersecret': user_record.usersecret,
                                          'is_active': user_record.is_active,
                                          'created_on': user_record.timestamp}}})


app.secret_key = os.environ.get("FLASK_SECRET_KEY")
