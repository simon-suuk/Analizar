import os
import sys

sys.path.append(os.getcwd())

from flask import Flask, render_template, request, jsonify, json, flash, redirect, url_for
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from models.user_model import UserModel
from models.base_model import DBSingleton
from werkzeug.security import generate_password_hash, check_password_hash

# from flask_security import login_required

app = Flask(__name__)
login_manager = LoginManager(app)
login_manager.init_app(app)

# This will redirect users to the login view whenever they are required to be logged in.
login_manager.login_view = 'signin'


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


# user signup
@app.route('/signup', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        company_name = request.form['company_name']
        industry = request.form['industry']
        company_size = request.form['company_size']

        # Email Validation
        try:
            user = UserModel.get(UserModel.email == email)
        except Exception as ex:
            user = UserModel.create(
                name=name,
                email=email,
                password_hash=generate_password_hash(password),
                company_name=company_name,
                industry=industry,
                company_size=company_size
            )

            return redirect(url_for('login'))
        else:
            flash('sorry email supplied has already been taken ')

    return render_template('signup.html')


# user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('user_dashboard'))
    if request.method == 'POST':
        try:
            user = UserModel.get(UserModel.email == request.form['email'])
            if check_password_hash(user.password_hash, request.form['password']):
                login_user(user, True)
                return redirect(url_for('user_dashboard'))
            else:
                flash('Authentication failed.')
        except Exception as ex:
            flash('Account does not exist. Please click on signup to register')

    return render_template('signin.html')


# logout user from session
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


# dashboard home page
@app.route('/dashboard')
@login_required
def user_dashboard():
    pass
    return render_template('dashboard.html')


@app.route('/dashboard/marketing')
@login_required
def user_marketing_obj_dashboard():
    return render_template('dashboard_marketing.html')


@app.route('/dashboard/user_guide')
@login_required
def user_guide_dashboard():
    return render_template('dashboard_userguide.html')


@app.route('/dashboard/report')
@login_required
def user_report_dashboard():
    return render_template('dashboard_report.html')


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
