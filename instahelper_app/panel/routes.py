import os
from flask import (Blueprint, url_for, redirect, 
                    render_template, request, flash)
from flask_login import login_required, current_user, logout_user, login_user
from instahelper_app.panel.forms import (RegistrationForm, LoginForm, AccountForm,
                                         HashtagForm)
from instahelper_app import bcrypt
from instahelper_app.models import User, db, Account, Hashtag
from cryptography.fernet import Fernet

import redis, time



panel = Blueprint('panel', __name__, static_folder='static', template_folder='templates')

@panel.route("/", methods=("GET", "POST"))
@login_required
def home():
    r = redis.Redis()
    form = AccountForm()
    if request.method == "POST":
        if form.validate_on_submit():
            if kopyala(form.username.data, form.password.data):
                key = os.environ.get("INSTA_KEY").encode()
                
                hashed_password= Fernet(key).encrypt(form.password.data.encode('utf-8')).decode('utf-8')
                
                acc = Account(username=form.username.data, password=hashed_password, owner=int(current_user.id))
                db.session.add(acc)
                db.session.commit()
                flash(f"You have successfully added {form.username.data} as your instagram account.", 'success')
            else:
                flash(r.get(form.username.data+"message").decode('utf-8'), 'danger')
                r.delete(form.username.data+"message")
    accounts = Account.query.filter_by(owner=current_user.id).all()
    return render_template("dashboard.html", form=form, accounts=accounts)


@panel.route("<int:accid>/hashtag", methods=["GET", "POST"])
@login_required
def hashtag(accid):
    accounts = Account.query.filter_by(owner=current_user.id).all()
    acc = Account.query.filter_by(id=accid).first()
    form = HashtagForm()
    r = redis.Redis()
    if request.method == "POST":
        hashtags = (form.hashtags.data).split("\r\n")
        command = Hashtag(owner=accid, tags=str(hashtags), like=form.like.data, comment=form.comment.data, follow=form.follow.data)
        db.session.add(command)
        db.session.commit()
  
        r.lpush(acc.username, "hashtag")
        r.lpush(acc.username+"tags", *hashtags)
        if form.like.data: r.set(acc.username+"like", str(form.like.data)) 
        if form.comment.data: r.set(acc.username+"comment", str(form.comment.data)) 
        if form.follow.data: r.set(acc.username+"follow", str(form.follow.data)) 
        flash(f"Hashtag bot started successfully.", "success")
    if "hashtag".encode() in r.lrange(acc.username,0, r.llen(acc.username)):
        tags = []
        [tags.append(tag.decode('utf-8')) for tag in r.lrange(acc.username+"tags",0, r.llen(acc.username+"tags"))]
        return render_template("hashtag.html", form=form, accounts=accounts, started=True, accid=accid, tags=tags)
    return render_template("hashtag.html", form=form, accounts=accounts, started=False, accid=accid)

@panel.route("<int:accid>/stop_hashtag", methods=["GET", "STOP"])
@login_required
def stop_hashtag(accid):
    acc = Account.query.filter_by(id=accid).first()
    r = redis.Redis()
    r.delete(acc.username)
    r.delete(acc.username+"tags")
    r.delete(acc.username+"like")
    r.delete(acc.username+"comment")
    r.delete(acc.username+"follow")
    r.delete(acc.username+"pool")
    return redirect(url_for('panel.hashtag', accid=accid))








@panel.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f"You have successfully logged in as {form.email.data}", 'success')
            #next_page = request.args.get('next')  # args is a dict. .get doesnt return error if it is empty
            #return redirect(url_for(next_page)) if next_page else redirect(url_for('main.home'))
            return redirect(url_for('panel.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')

        
    return render_template('login.html', title='Login', form=form)

@panel.route("/register", methods = ['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("panel.home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=hashed_password, email=form.email.data)
        db.session.add(user)
        db.session.commit()

        flash(f"You have registered as {form.username.data}! Now you can login.", 'success')
        return redirect(url_for('panel.login'))
    return render_template("register.html", form=form, title="Register")









@panel.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))







@panel.route('/delete/<string:username>', methods=['GET', 'POST'])
def delete_account(username):
    acc = Account.query.filter_by(username=username).first()
    if acc.owner == current_user.id:
        Hashtag.query.filter_by(owner=acc.id).delete()
        
        db.session.commit()
        db.session.delete(acc)
        db.session.commit()
    return redirect(url_for('panel.home'))






def kopyala(username, password):
    listname = "tocopylist"
    r = redis.Redis()
    acclist = r.lrange(listname, 0, r.llen(listname))
    for acc in acclist:
        if acc.decode('utf-8') == username:
            acclist.index(acc)
            r.lrem(listname, 1, username)
            r.delete(username)
    
    r.rpush(listname, username)
    r.set(username, password, 500)
    while r.get(username):
        if r.get(username+"message"):
            return False
        time.sleep(1)
    return True
    

