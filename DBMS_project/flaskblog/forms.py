from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField,PasswordField,SubmitField,BooleanField, IntegerField
from wtforms.validators import DataRequired,Length,Email,EqualTo, ValidationError
from flaskblog.models import User


class SignupForm(FlaskForm):
    firstname=StringField('First Name',validators=[DataRequired(),Length(min=2,max=20)])
    lastname=StringField('Last Name',validators=[DataRequired(),Length(min=2,max=20)])
    phone_number = IntegerField('Phone Number',validators=[DataRequired(message='Field is required and should consist digits only.')])
    username=StringField('Username',validators=[DataRequired(),Length(min=2,max=20)])
    email=StringField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('Password',validators=[DataRequired()])
    confirm_password=PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
    submit=SubmitField('Sign Up')

    def validate_email(self,email):
        user=User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Account already exists")
        

class LoginForm(FlaskForm):
    email=StringField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('Password',validators=[DataRequired()])
    remember=BooleanField('Remember Me')
    submit=SubmitField('Sign In')


class UpdateAccountForm(FlaskForm):
    phone_number = IntegerField('Phone Number',validators=[DataRequired(message='Field is required and should consist digits only.')])
    email=StringField('Email',validators=[DataRequired(),Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit=SubmitField('Update')

    def validate_phone_number(self,phone_number):
        if phone_number.data != current_user.phone_number:
            user=User.query.filter_by(phone_number=phone_number.data).first()
            if user:
                raise ValidationError("This Phone Number already exists")

    def validate_email(self,email):
        if email.data != current_user.email:
            user=User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("This Email already exists")
