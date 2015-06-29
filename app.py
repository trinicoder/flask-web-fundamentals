#!/usr/bin/env python

from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask.ext.wtf import Form
from wtforms.fields import StringField, SubmitField, PasswordField
from wtforms.validators import Required
from flask.ext.sqlalchemy import SQLAlchemy
#import sqlalchemy
#from sqlalchemy.sql import select
from flask.ext.script import Manager
import os

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess'
app.config['SQLALCHEMY_DATABASE_URI']=\
    'sqlite:///' + os.path.join(basedir, 'hotspot.db')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
manager = Manager(app)
db = SQLAlchemy(app)

user = ['varoon', 'jon']
password = ['pass', '123', 'qwerty']
secret='Flashpointparadox'


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), unique=True, index=True)


    def __repr__(self):
        return '<User %r>' % self.username

@app.route('/')
def index(username=None):
    #jack_user = User(username='jack')
    #our_user = db.session.query(User).filter_by(username='jack').first()
    #db.session.delete(our_user)
    user_db = User.query.all()



    if session.get('username') !=  None:
        return render_template('index.html', username= session.get('username'), user=user_db)

    return render_template('index.html', username= 'Your not Logged in!', user=user_db)

@app.route('/logged')
def logged(username=None):
    username = session['username']
    if username != None:

        return render_template('loggedin.html', username= username)
    return render_template('loggedin.html', username= 'Your not Logged in!')

@app.route('/logout')
def logout(username=None):
    session['username'] = None
    return render_template('loggedin.html', username= 'Your not Logged in!')

class LoginForm(Form):
    username = StringField('Enter your Username', validators = [Required()])
    password = PasswordField('Enter your Password', validators = [Required()])
    submit = SubmitField('Submit')


@app.route('/login', methods = ['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit() :
        # get user name
        username=form.username.data

        #result = db.session.query(User).filter(User.username == username)
        #query db for matching record

        result = db.session.query(User).filter_by(username=username)

        #check for query result( Must be a easier way to do this)
        try:
            our_user=result[0].username
        except:
            return render_template('login.html', form=form, username='<User does not exist on database>')


        if our_user==username and form.password.data in password:
            session['username'] = form.username.data
            session['password'] = form.password.data
            return redirect(url_for('logged'))

        form.username.data = ''

    return render_template('login.html', form=form, username=session.get('username'))



if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
    #manager.run()
