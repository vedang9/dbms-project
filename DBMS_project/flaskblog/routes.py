import os
import secrets
from PIL import Image
from flask import  render_template,url_for,flash,redirect,request
from flaskblog import app,db,bcrypt
from flaskblog.forms import SignupForm,LoginForm,UpdateAccountForm
from flaskblog.models import User
from flask_login import login_user,current_user,logout_user,login_required


@app.route("/")
@app.route("/home")
@login_required
def home():
    return render_template("home_page.html")

@app.route("/signup",methods=['GET','POST'])
def signup():
    form=SignupForm()
    if form.validate_on_submit():
        hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user=User(firstname=form.firstname.data, lastname=form.lastname.data, phone_number=form.phone_number.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created successfully for {form.firstname.data}!','success')
        return redirect(url_for('home'))
    return render_template('sign up.html',title='Sign Up', form=form)

@app.route("/signin",methods=['GET','POST'])
def signin():
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash("Login unsuccessful. Please check email and password","danger")
    return render_template('sign in.html',title='Sign In', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('signin'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _ , f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    
    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account",methods=['GET','POST'])
@login_required
def account():
    form=UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.phone_number = form.phone_number.data
        current_user.email = form.email.data
        db.session.commit()
        flash(" Your Account has been updated successfully","success")
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.phone_number.data = current_user.phone_number
        form.email.data = current_user.email
    image_file= url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html',title='Account', image_file=image_file, form=form)