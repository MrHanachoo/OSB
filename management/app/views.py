__author__ = 'med'

from flask import request, render_template, flash, redirect, session, url_for, jsonify
import flask.ext.uploads
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app
from forms import LoginForm, RegisterForm, UploadObjectForm
from api import User, Containers, Objects
from werkzeug.utils import secure_filename
import os
from swiftclient import client

@app.route('/')
def home():
    return render_template('home.html', title='Home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if not form.validate():
            return render_template('login.html',
                                   title='Login',
                                   form=form)
        else:
            if User.exists(form.user_name.data.lower(), form.user_pass.data.lower()):
                ses = User.get_info(form.user_name.data.lower(), form.user_pass.data.lower())
                print 'DEBUG: views.login :: ' + ses['StorageURL'], ses['Token']
                session['user_name'] = form.user_name.data.lower()
                session['url'] = ses['StorageURL']
                session['token'] = ses['Token']
                session['temp_url_key'] = ses['Temp_Url_Key']
                session['account'] = ses['Account']
                return redirect(url_for('account'))
    elif request.method == 'GET':
        if 'url' in session and 'token' in session:
            return redirect(url_for('account'))
        else:
            return render_template('login.html',
                                   title='Login',
                                   form=form)


@app.route('/logout')
def logout():
    if 'url' in session and 'token' in session:
        session.pop('user_name', None)
        session.pop('url', None)
        session.pop('token', None)
        session.pop('temp_url_key', None)
        return redirect(url_for('home'))
    else:
        return redirect(url_for('login'))


@app.route('/signup', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if request.method == 'POST':
        if not form.validate():
            return render_template('signup.html',
                                   title='Sign up',
                                   form=form)
        else:
            return redirect(url_for('account'))
    elif request.method == 'GET':
        if 'url' in session and 'token' in session:
            return redirect(url_for('account'))
        else:
            return render_template('signup.html',
                                   title='Sign up',
                                   form=form)


@app.route('/account')
def account():
    if 'url' in session and 'token' in session:
        cont_list = Containers().list(session['url'], session['token'])
        print cont_list
        print type(cont_list)
        if cont_list == '<html><h1>Unauthorized</h1><p>This server could not verify that you are authorized to access ' \
                        'the document you requested.</p></html>':
           return redirect(url_for('logout'))
        return render_template('account.html',
                               title='Account',
                               cont_list=cont_list)
    else:
        return redirect(url_for('login'))


@app.route('/account/<container_name>', methods=['GET', 'POST'])
def container(container_name):
    if 'url' in session and 'token' in session:
        session['container'] = container_name
        cont_list = Containers().list(session['url'], session['token'])

        objs_list = Objects().list(session['url'], session['token'], container_name)
        if not objs_list:
            return render_template('account.html',
                               title='Account',
                               cont_list=cont_list)
        return render_template('account.html',
                               title='container',
                               objs_list=objs_list,
                               cont_list=cont_list)
    else:
        return redirect(url_for('login'))


@app.route('/account/create/<container_name>', methods=['GET', 'POST'])
def create_container(container_name):
    if 'url' in session and 'token' in session:
        cont_create = Containers().create(session['url'], session['token'], container_name)
        print 'DEBUG: views./account/create/' + str(container_name) + ": " + str(cont_create)
        result = {'status': cont_create}
        return jsonify(**result)

@app.route('/account/delete/<container_name>', methods=['GET', 'POST', 'DELETE'])
def delete_container(container_name):
    if 'url' in session and 'token' in session:
        cont_delete = Containers().delete(session['url'], session['token'], container_name)
        print 'DEBUG: views./account/delete/' + str(container_name) + ": " + str(cont_delete)
        result = {'status': cont_delete}
        print 'DEBUG: views./account/delete/json'+str(jsonify(**result))
        #return redirect(url_for('account'))
        return jsonify(**result)





@app.route('/account/<container_name>/upload', methods=['GET', 'POST'])
def upload_object(container_name):
    if 'url' in session and 'token' in session:
        form = UploadObjectForm()
        print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'+container_name
        if request.method == 'POST':
            obj = request.files['object_to_upload']
            filename = secure_filename(obj.filename)
            print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'+filename
            directory = os.path.join(app.config['UPLOAD_FOLDER'], session['user_name'])
            print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'+directory
            if not os.path.exists(directory):
                os.makedirs(directory)
            path = os.path.join(directory, filename)
            obj.save(path)
            '''if form.validate():
                file = request.files('up')
                if file:
                    filename = secure_filename(file.filename)
                    print filename
                    directory = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    print directory
                    if not os.path.exists(directory):
                        os.makedirs(directory)
                    path = os.path.join(directory, filename)
                    print path
                    file.save(path)'''
            '''
            up_obj = Objects.upload(session['url'], session['token'], container_name, obj)
            print 'DEBUG: views./account/' + container_name + '/upload/' + obj > +': ' + str(up_obj)
            result = {'status': up_obj}
            return jsonify(**result)'''



@app.route('/account/<container_name>/<object_name>/delete', methods=['GET', 'POST'])
def delete_object(container_name, object_name):
    if 'url' in session and 'token' in session:
        del_obj = Objects.delete(session['url'], session['token'], container_name, object_name)
        print 'DEBUG: views./account/' + container_name + '/delete/' + object_name  +': ' + str(del_obj)
        result = {'status': del_obj}
        print '================================'+str(result)
        return jsonify(**result)

@app.route('/account/<container_name>/<object_name>/share', methods=['GET', 'POST'])
def share_object(container_name, object_name):
    if 'url' in session and 'token' in session:
        sh_obj = Objects.share(app.config['HOST'], 'GET','300', session['account'], container_name, object_name, session['temp_url_key'])
        print 'DEBUG: views./account/' + container_name + '/upload/' + object_name  +': ' + str(sh_obj)
        result = {'status': sh_obj}
        return jsonify(**result)

@app.route('/account/<container_name>/<object_name>/download', methods=['GET', 'POST'])
def download_object(container_name, object_name):
    if 'url' in session and 'token' in session:
        down_obj = Objects.download(app.config['HOST'], 'GET','10', session['account'], container_name, object_name, session['temp_url_key'])
        print 'DEBUG: views./account/' + container_name + '/download/' + object_name  +': ' + str(down_obj)
        result = {'status': down_obj}
        return jsonify(**result)
    '''
    if 'url' in session and 'token' in session:
        down_obj = Objects.download(session['url'], session['token'], container_name, object_name)
        print 'DEBUG: views./account/' + container_name + '/download/' + object_name > +': ' + str(down_obj)
        result = {'status': down_obj}
        return jsonify(**result)
'''

@app.route('/about')
def about():
    return render_template('about.html',
                           title='About')


@app.route('/contact')
def contact():
    return render_template('contact.html',
                           title='Contact')


@app.route('/index')
def index():
    user = {'nickname': 'MrHanach'}
    posts = [
        {
            'author': {'nickname': 'med'},
            'body': 'Beautiful  day in Tunis ! '
        },
        {
            'author': {'nickname': 'mido'},
            'body': 'the film was cool ! '
        }
    ]
    return render_template('index.html',
                           title='Home',
                           user=user,
                           posts=posts)





@app.route('/agent')
def agent():
    user_agent = request.headers.get('User-Agent')
    return '<p>Your browser is %s</p>' % user_agent

