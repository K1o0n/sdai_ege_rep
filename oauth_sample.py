import os
from dotenv import load_dotenv
# from flask import Flask, render_template, redirect, url_for, request, flash
from flask_dance.contrib.google import make_google_blueprint, google
from flask import Flask, render_template, session, request, redirect, url_for
import db_functions as db
# import logging
# from urllib.parse import quote as url_quote
# from werkzeug.security import generate_password_hash
load_dotenv()
app = Flask(__name__)
client_id = os.getenv('GOOGLE_CLIENT_ID')
client_secret = os.getenv('GOOGLE_CLIENT_SECRET')
app.secret_key = os.getenv('secret_key')
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'
blueprint = make_google_blueprint(
    client_id=client_id,
    client_secret=client_secret,
    reprompt_consent=True,
    scope=["profile", "email"]
)
app.register_blueprint(blueprint, url_prefix="/login")

@app.route('/login')
def login():
    return redirect(url_for('google.login'))

@app.route('/sign-in/', methods=['GET', 'POST'])
def sign_in():
    google_data = None
    user_info_endpoint = '/oauth2/v2/userinfo'
    if google.authorized:
        google_data = google.get(user_info_endpoint).json()
        print(google_data)
        return redirect('/dashboard/')
    if request.method == 'GET':
        return render_template('sign-in.html',google_data=google_data,
                           fetch_url=google.base_url + user_info_endpoint)
    """
    #TODO Сделать нормальную авторизацию через гугл. 
    
    Кто это читает и понимает в бд, пожалуйста, помогите
    Все данные которые приходят с гугла лежат в google_data. По идее, если пользователь уже есть в бд, то его нужно авторизовать
    Но там есть еще одна проблема, что если пользователь зареган через гугл, то у него нет пароля, и как его авторизовать?
    Я вживил в sign-in.html кнопку для авторизации через гугл, на этом мои полномочия все.
    (эти мольбы о помощи, кстати, написал ИИ)
    
    А, и да, в render_template всегда передается google_data и fetch_url. Также нужно чистить google_data при неудачной авторизации
    Ибо кнопочка пропадет, а данные останутся
    А еще я не имею понятия почему после логина перенаправляется на localhost:5000, а не на /dashboard/, но думаю пофиксится
    
    """
    # print(google_data)
    data = dict(request.form)
    uid = db.get_user_id(data['email'], 1)
    user = db.get_user(uid, 1)
    # orms were invented in 1995... People before 1995:
    if user and user[0][4] == data['password']:
        session['email'] = data['email']
        return redirect('/dashboard/')
    else:
        return render_template('sign-in.html', error='MEOW!', google_data=None, fetch_url=google.base_url + user_info_endpoint)

if __name__ == "__main__":
    app.run(debug=1)