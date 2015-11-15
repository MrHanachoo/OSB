__author__ = 'med'

from flask import request, render_template, flash, redirect, session, url_for, jsonify
import flask.ext.uploads
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app
from forms import LoginForm, RegisterForm, UploadObjectForm, ContConfigForm
from api import User, Containers, Objects
from werkzeug.utils import secure_filename
import os, datetime
import swiftclient



@app.route('/')
def home():
    return render_template('home.html', title='Home')


@app.route('/account/<container_name>/<object_name>/tempurl/<ttl>', methods=['GET', 'POST'])
def share_object(container_name, object_name, ttl):
    if 'url' in session and 'token' in session:
        temp_url_gen = Objects.temp_url_gen(session['url'], app.config['HOST'], 'GET',str(int(ttl)*3600), session['account'], container_name, object_name, session['temp_url_key'], session['token'])
        print 'DEBUG: views./account/' + container_name + '/' + object_name  +'/tempurl'+': ' + str(temp_url_gen)
        result = {'status': temp_url_gen}
        return jsonify(**result)

@app.route('/account/<container_name>/publish/<status>', methods=['POST'])
def publish_container(container_name, status):
    if 'url' in session and 'token' in session:
        form = ContConfigForm()
        print status
        cg = Containers.config(url=session['url'], token=session['token'], container_name=container_name, status=status)
        result = {'status': cg}
        return jsonify(**result)



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
        try:
            output = swiftclient.get_account(url=session['url'], token=session['token'])
        except swiftclient.ClientException:
            return redirect(url_for('logout'))
        print 'DEBUG: views.account().swiftclient.get_account: '+str(output)
        account_info = output[0]
        account_info['x-account-bytes-used'] = float(account_info['x-account-bytes-used']) /(1024**3)
        cont_list = output[1]
        acl_dic = {}
        for i in cont_list:
            acl_dic[i['name']] = Containers.check_read_acl(url=session['url'], token=session['token'], container_name=i['name'])

        return render_template('account.html',
                               title='Account',
                               account_info=account_info,
                               cont_list=cont_list,
                               acl_dic=acl_dic)
    else:
        return redirect(url_for('login'))


@app.route('/account1')
def search():
    if 'url' in session and 'token' in session:
        val = request.args.get('val')
        print "#########################################", val
        try:
            output = swiftclient.get_account(url=session['url'], token=session['token'])
        except swiftclient.ClientException:
            return redirect(url_for('logout'))
        print 'DEBUG: views.account().swiftclient.get_account: '+str(output)
        account_info = output[0]
        account_info['x-account-bytes-used'] = float(account_info['x-account-bytes-used']) /(1024**3)
        cont_list = output[1]
        cont_list_1 = []
        for i in cont_list:
            if val in i['name']:
                cont_list_1.append(i)

        acl_dic = {}
        for i in cont_list_1:
            acl_dic[i['name']] = Containers.check_read_acl(url=session['url'], token=session['token'], container_name=i['name'])

        return render_template('account.html',
                               title='Account',
                               account_info=account_info,
                               cont_list=cont_list_1,
                               acl_dic=acl_dic)
    else:
        return redirect(url_for('login'))


@app.route('/account/<container_name>', methods=['GET', 'POST'])
def container(container_name):
    if 'url' in session and 'token' in session:
        session['container'] = container_name
        try:
            output = swiftclient.get_container(url=session['url'], token=session['token'], container=container_name)
        except swiftclient.ClientException:
            return redirect(url_for('logout'))

        print 'DEBUG: views.container().swiftclient.get_container: '+str(output)
        container_info = output[0]
        container_info['x-container-bytes-used'] = float(container_info['x-container-bytes-used']) /(1024**3)

        for i in output[1]:
            i['last_modified'] = i['last_modified'][:10]+" "+i['last_modified'][11:16]
            i['content_type'] = i['content_type'].split('/')[1]

            temp_meta = Objects.read_temp_url(url=session['url'], token=session['token'], container=container_name, object=i['name'])
            i['temp_url'] = temp_meta[0]
            timestamp = temp_meta[1]
            if timestamp == False:
                i['temp_url_exp'] = '- '
            else:
                i['temp_url_exp'] = datetime.datetime.fromtimestamp(float(timestamp))

            print '###############################################################'
        obj_list = output[1]
        print type(output)
        print output[0]
        print output[1]
        cont_acl = Containers.check_read_acl(url=session['url'], token=session['token'], container_name=container_name)
        return render_template('container.html',
                               title='Container',
                               container_info=container_info,
                               obj_list=obj_list,
                               cont_acl=cont_acl)
        '''
        result = {'status': output}
        return jsonify(**result)
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
        '''

    else:
        return redirect(url_for('login'))





@app.route('/account/<container_name>/create', methods=['GET', 'POST'])
def create_container(container_name):
    if 'url' in session and 'token' in session:
        cont_create = Containers().create(session['url'], session['token'], container_name)
        print 'DEBUG: views./account/create/' + str(container_name) + ": " + str(cont_create)
        result = {'status': cont_create}
        return jsonify(**result)





@app.route('/account/<container_name>/delete', methods=['GET', 'POST', 'DELETE'])
def delete_container(container_name):
    if 'url' in session and 'token' in session:
        cont_delete = Containers().delete(session['url'], session['token'], container_name)
        print 'DEBUG: views./account/delete/' + str(container_name) + ": " + str(cont_delete)
        result = {'status': cont_delete}
        print 'DEBUG: views./account/delete/json'+str(jsonify(**result))
        #return redirect(url_for('account'))
        return jsonify(**result)





@app.route('/account/<container_name>/upload/<file_path>', methods=['GET', 'POST'])
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

@app.route('/account/<container_name>/<object_name>/view', methods=['GET', 'POST'])
def view_object(container_name, object_name):
    if 'url' in session and 'token' in session:
        down_obj = Objects.download(app.config['HOST'], 'GET','10', session['account'], container_name, object_name, session['temp_url_key'])
        down_obj = down_obj+'&inline'
        print 'DEBUG: views./account/' + container_name + '/download/' + object_name  +': ' + str(down_obj)
        result = {'status': down_obj}
        return jsonify(**result)


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

# TODO: config Buttons cont/obj
# TODO: redesign upload

#
