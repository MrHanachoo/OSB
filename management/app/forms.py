__author__ = 'med'

from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FileField
from wtforms.validators import DataRequired, Email
from api import User, AddUser


class LoginForm(Form):
    """

    """
    user_name = StringField('Username:', validators=[DataRequired()])
    user_pass = PasswordField('Password:', validators=[DataRequired()])
    submit = SubmitField('Login')
    remember_me = BooleanField('remember_me', default=False)

    def validate(self):
        if not Form.validate(self):
            return False
        user_name = self.user_name.data.lower()
        user_pass = self.user_pass.data.lower()
        if User.exists(user_name, user_pass):
            if AddUser.gen_temp_url_key(user_name, user_pass):
                print 'DEBUG: forms.validate.LoginForm :: gen_temp_url_key : True'
                return User.get_info(user_name, user_pass)
        else:
            self.submit.errors.append("Invalid user name or password !!!")
            return False


class RegisterForm(Form):
    """

    """
    user_name = StringField('Username:', validators=[DataRequired()])
    user_pass = PasswordField('Password:', validators=[DataRequired()])
    confirm_user_pass = PasswordField('Confirm Password:', validators=[DataRequired()])
    user_email = StringField('Email:', validators=[DataRequired(), Email()])
    submit = SubmitField('Sign up for Rosafi Cloud Storage')

    def validate(self):
        if not Form.validate(self):
            return False
        name = self.user_name.data.lower()
        passwd = self.user_pass.data.lower()
        if self.user_pass.data != self.confirm_user_pass.data:
            self.confirm_user_pass.errors.append("Passwords do not match !")
            return False
        if User.exists(name, passwd):
            self.user_name.errors.append("This Username is already taken !")
            return False
        email = self.user_email.data.lower()
        if AddUser.add_user(name, passwd, email):
            if AddUser.gen_temp_url_key(name, passwd):
                print 'DEBUG: forms.validate.add_user :: gen_temp_url_key : True'
                return True
        else:
            self.user_email.errors.append("This email is already taken !")
            return False


class UploadObjectForm(Form):
    """

    """
    object_to_upload = FileField('')



