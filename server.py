import os
import sys

import dateutil.parser as date_parser
from datetime import date

sys.path.append(os.getcwd())

from flask import Flask, render_template, request, jsonify, json, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from services.authentication import OAuthSignIn
import services.graph_api as graph
import engines.post_metrics_engine as post_metrics_engine
import engines.performance_inference_engine as post_performance
from models.user_model import UserModel
from models.base_model import DBSingleton
from werkzeug.security import generate_password_hash, check_password_hash

# from flask_security import login_required

app = Flask(__name__)
login_manager = LoginManager(app)
login_manager.init_app(app)

# This will redirect users to the login view whenever they are required to be logged in.
login_manager.login_view = 'login'


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


# user signup
@app.route('/signup', methods=['GET', 'POST'])
def signup():
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
        return redirect(url_for('dashboard_accounts'))
    if request.method == 'POST':
        try:
            user = UserModel.get(UserModel.email == request.form['email'])
            if check_password_hash(user.password_hash, request.form['password']):
                login_user(user, True)
                return redirect(url_for('dashboard_accounts'))
            else:
                flash('Authentication failed.')
        except Exception as ex:
            flash('Account does not exist. Please click on signup to signup')

    return render_template('login.html')


# logout user from session
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


# dashboard home page
@app.route('/')
@app.route('/dashboard/accounts')
@login_required
def dashboard_accounts():
    return render_template('dashboard_accounts.html')


@app.route('/dashboard/posts')
@login_required
def dashboard_posts():
    post_dict = {}
    page = graph.PageOrPost(current_user.page_id, current_user.page_token)
    performance = post_performance.PerformanceInferenceEngine()

    try:
        fan_base = page.get_node_properties("fan_count")["fan_count"]
        # print("fan_base: {}".format(fan_base))

        posts_list = \
            page.get_node_properties("posts.limit(5).fields(id,message,created_time)")["posts"][
                "data"]
    except:
        import traceback
        traceback.print_exc()
        flash('We cannot connect to facebook. Please check your network connection and try again')
        return redirect(url_for('dashboard_accounts'))

    for post_val in posts_list:
        date_time = date_parser.parse(post_val["created_time"])
        created_date = str(date_time.date())
        created_time = str(date_time.time())
        post_title = post_val.get('message')

        post = graph.PageOrPost(post_val['id'], current_user.page_token)
        try:
            post_statistics = post.get_node_properties(
                "insights.metric(post_impressions_unique,post_engaged_users,post_consumptions_unique,post_negative_feedback_unique).period(lifetime).fields(id,name,values,title)")[
                "insights"]["data"]
        except:
            import traceback
            traceback.print_exc()
            flash('We cannot connect to facebook. Please check your network connection and try again')
            return redirect(url_for('dashboard_accounts'))

        try:
            lifetime_post_reach = post_statistics[0]["values"][0]["value"]
        except KeyError:
            lifetime_post_reach = 0

        try:
            lifetime_engaged_users = post_statistics[1]["values"][0]["value"]
        except KeyError:
            lifetime_engaged_users = 0

        try:
            lifetime_negative_feedback = post_statistics[3]["values"][0]["value"]
        except KeyError:
            lifetime_negative_feedback = 0

        lifetime_post_reach_score = post_metrics_engine.pct_of_total_post_reach(int(lifetime_post_reach), int(fan_base))
        lifetime_engaged_users_score = post_metrics_engine.pct_of_post_engagement(int(lifetime_engaged_users),
                                                                                  int(lifetime_post_reach))
        lifetime_negative_feedback_score = post_metrics_engine.pct_of_post_negative_feedback(
            int(lifetime_negative_feedback),
            int(lifetime_engaged_users))

        post_dict[post_val['id']] = {"post_title": post_title,
                                     "created_date": created_date,
                                     "created_time": created_time,
                                     "lifetime_post_reach_score": performance.performance_score(
                                         lifetime_post_reach_score),
                                     "lifetime_engaged_users_score": performance.performance_score(
                                         lifetime_engaged_users_score),
                                     "lifetime_negative_feedback_score": performance.performance_score(
                                         lifetime_negative_feedback_score),
                                     }

    print("user_post: {}".format(post_dict))
    return render_template('dashboard_posts.html', user_posts=post_dict)


@app.route('/dashboard/post_analysis/<string:post_id>')
@login_required
def dashboard_post_analysis(post_id):
    page_post = graph.PageOrPost(post_id, current_user.page_token)

    try:
        post_stats_reach = page_post.get_node_properties(
            "insights.metric(post_impressions_unique,post_engaged_users,post_consumptions_unique,post_negative_feedback_unique).period(lifetime).fields(id,name,values,title)")[
            "insights"]["data"]

        post_stats_engagement = page_post.get_node_properties(
            "id,message,created_time,shares,likes.summary(true).limit(0),comments.summary(true).limit(0)")
    except:
        import traceback
        traceback.print_exc()
        flash('We cannot connect to facebook. Please check your network connection and try again')
        return redirect(url_for('dashboard_accounts'))

    try:
        lifetime_post_reach = post_stats_reach[0]["values"][0]["value"]
    except KeyError:
        lifetime_post_reach = 0

    try:
        lifetime_engaged_users = post_stats_reach[1]["values"][0]["value"]
    except KeyError:
        lifetime_engaged_users = 0

    try:
        clicks = post_stats_reach[2]["values"][0]["value"]
    except KeyError:
        clicks = 0

    try:
        lifetime_negative_feedback = post_stats_reach[3]["values"][0]["value"]
    except KeyError:
        lifetime_negative_feedback = 0

    post_id = post_stats_engagement["id"]

    date_time = date_parser.parse(post_stats_engagement["created_time"])
    created_date = str(date_time.date())
    created_time = str(date_time.time())

    post_title = post_stats_engagement.get('message')

    try:
        shares = post_stats_engagement["shares"]["count"]
    except KeyError:
        shares = 0

    try:
        likes = post_stats_engagement["likes"]["summary"]["total_count"]
    except KeyError:
        likes = 0

    try:
        comments = post_stats_engagement["comments"]["summary"]["total_count"]
    except KeyError:
        comments = 0

    post_metrics = {"post_id": post_id,
                    "post_title": post_title,
                    "created_date": created_date,
                    "created_time": created_time,
                    "shares": shares,
                    "likes": likes,
                    "comments": comments,
                    "lifetime_post_reach": lifetime_post_reach,
                    "lifetime_engaged_users": lifetime_engaged_users,
                    "clicks": clicks,
                    "lifetime_negative_feedback": lifetime_negative_feedback}

    print("post_metrics: {}".format(post_metrics))
    return render_template('dashboard_post_analysis.html', post_metrics=post_metrics)


@app.route('/dashboard/analytics')
@login_required
def dashboard_analytics():
    return render_template('dashboard_analytics.html')


@app.route('/dashboard/analytics_daily_report')
@login_required
def dashboard_analytics_daily_report():
    return render_template('dashboard_daily_report.html')


@app.route('/dashboard/analytics_weekly_report')
@login_required
def dashboard_analytics_weekly_report():
    return render_template('dashboard_weekly.html')


@app.route('/dashboard/reports')
@login_required
def dashboard_reports():
    return render_template('dashboard_advice.html')


@app.route('/dashboard/reports_advice')
@login_required
def dashboard_reports_advice():
    return render_template('dashboard_advice.html')


@app.route('/dashboard/user')
@login_required
def dashboard_user():
    return render_template('user.html')


@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    if current_user.page_id is not None:
        return redirect(url_for('dashboard_posts'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()


@app.route('/callback/<provider>')
def oauth_callback(provider):
    if current_user.page_id is not None:
        return redirect(url_for('dashboard_posts'))

    oauth = OAuthSignIn.get_provider(provider)
    social_id, social_username, social_email, account_data = oauth.callback()
    # print('My Account Data: {}'.format(account_data))

    page_id = account_data[0].get('id')
    page_name = account_data[0].get('name')
    page_category = account_data[0].get('category')
    page_token = account_data[0].get('access_token')

    if social_id is None:
        flash('Authentication failed.')
        return redirect(url_for('dashboard_accounts'))

    try:
        query = UserModel.update(
            social_id=social_id,
            social_username=social_username,
            social_email=social_email,
            page_id=page_id,
            page_name=page_name,
            page_category=page_category,
            page_token=page_token
        ).where(UserModel.email == current_user.email)

        if query.execute() < 1:
            flash('adding account failed.')
            return redirect(url_for('dashboard_accounts'))

    except Exception as ex:
        print(ex.args)
    return redirect(url_for('dashboard_posts'))


# @app.route('/set_properties')
@login_required
def set_properties():
    post_metrics_properties = {}
    page = None
    try:
        page = graph.PageOrPost(current_user.page_id, current_user.page_token)
    except Exception as ex:
        print(ex.args)

    post_metrics_properties["fan_base"] = page.get_node_properties("fan_count")["fan_count"]

    today = date.today().strftime('%Y-%m-%d')
    fan_adds = page.get_node_properties("insights.since({today}).metric(page_fan_adds)"
                                        ".fields(title, values)".format(today=today))["insights"]["data"][0]["values"][
        0]["value"]

    post_metrics_properties["fan_adds"] = fan_adds

    # posts_stats = page.get_node_properties(
    #     "posts.since(2014-06-08).until(2014-06-09).fields(id,message,created_time,shares,likes.summary(true).limit(0),comments.summary(true).limit(0))")[
    #     "posts"]["data"]

    posts_stats = page.get_node_properties("posts.until(2017-12-25).limit(5).fields(id,message,created_time,shares,"
                                           "likes.summary(true).limit(0),comments.summary(true).limit(0))")["posts"][
        "data"]

    # new_dict = dict((item["id"], item) for item in posts_stats)
    # print("newdict: {}".format(new_dict))
    page_post = None
    for val in posts_stats:
        # print("post data: {}".format(val))
        page_post = graph.PageOrPost(val['id'], current_user.page_token)

        date_time = date_parser.parse(val["created_time"])
        created_date = str(date_time.date())
        created_time = str(date_time.time())

        post_title = val.get('message')

        try:
            shares = val["shares"]["count"]
        except KeyError:
            shares = 0

        try:
            likes = val["likes"]["summary"]["total_count"]
        except KeyError:
            likes = 0

        try:
            comments = val["comments"]["summary"]["total_count"]
        except KeyError:
            comments = 0

        stats = page_post.get_node_properties(
            'insights.metric(post_impressions_unique,post_engaged_users,post_consumptions_unique,'
            'post_negative_feedback_unique).period(lifetime).fields(id,name,values,title)')["insights"]["data"]

        try:
            lifetime_post_reach = stats[0]["values"][0]["value"]
        except KeyError:
            lifetime_post_reach = 0

        try:
            lifetime_engaged_users = stats[1]["values"][0]["value"]
        except KeyError:
            lifetime_engaged_users = 0

        try:
            clicks = stats[2]["values"][0]["value"]
        except KeyError:
            clicks = 0

        try:
            lifetime_negative_feedback = stats[3]["values"][0]["value"]
        except KeyError:
            lifetime_negative_feedback = 0

        post_metrics_properties[val['id']] = {"post_title": post_title,
                                              "created_date": created_date,
                                              "created_time": created_time,
                                              "shares": shares,
                                              "likes": likes,
                                              "comments": comments,
                                              "lifetime_post_reach": lifetime_post_reach,
                                              "lifetime_engaged_users": lifetime_engaged_users,
                                              "clicks": clicks,
                                              "lifetime_negative_feedback": lifetime_negative_feedback}

    # print("post_metrics_properties: {}".format(post_metrics_properties))
    return post_metrics_properties


@app.route('/fetch_page_edge/<edge_name>')
@login_required
def fetch_page_edge(edge_name):
    page = None
    try:
        page = graph.PageOrPost(current_user.page_id, current_user.page_token)
        # print("All Post nodes Page: {}".format(page.get_edge("feed")))

    except Exception as ex:
        print(ex.args)
        return None
    return jsonify(page.get_edge(edge_name))


@app.route('/fetch_page_properties/<fields>')
@login_required
def fetch_page_properties(fields):
    page = None
    try:
        page = graph.PageOrPost(current_user.page_id, current_user.page_token)
    except Exception as ex:
        print(ex.args)
        return None
    return jsonify(page.get_node_properties(fields))


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
