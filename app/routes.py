from datetime import datetime
from sqlalchemy import desc
from app import app, db
from app.models import User, Post, History
from app.forms import LoginForm, RegistrasiForm, PostForm
from flask import render_template, url_for, redirect, flash, request, jsonify
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/')
@app.route('/home')
def home():
    user = User.query.all()
    post = Post.query.order_by(desc(Post.id))

    if current_user.is_authenticated :
        aksi = "home"
        Addlog = History(aksi=aksi, user_id=current_user.username, user_ip=request.remote_addr)
        db.session.add(Addlog)
        db.session.commit()
    else  :
        aksi = "home"
        username = "GUEST"
        Addlog = History(aksi=aksi, user_id=username, user_ip=request.remote_addr)
        db.session.add(Addlog)
        db.session.commit()
    return render_template('home.html', user=user, posts=post)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated :
        return redirect(url_for('home'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user.password == form.password.data :  
            login_user(user)
            flash(f'berhasil login', 'success')
            return redirect(url_for('home'))
        else :
            flash('Login gagal', 'danger')

    if current_user.is_authenticated :
        aksi = "login"
        Addlog = History(aksi=aksi, user_id=current_user.username, user_ip=request.remote_addr)
        db.session.add(Addlog)
        db.session.commit()
    else  :
        aksi = "login"
        username = "GUEST"
        Addlog = History(aksi=aksi, user_id=username, user_ip=request.remote_addr)
        db.session.add(Addlog)
        db.session.commit()
    return render_template('login.html', title='Login', form=form)


@app.route('/regis', methods=['GET', 'POST'])
def regis():
    if current_user.is_authenticated :
        return redirect(url_for('home'))
    
    form = RegistrasiForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, password=form.password.data, email=form.email.data)
        db.session.add(user)
        db.session.commit()

        aksi = "registrasi"
        Addlog = History(aksi=aksi, user_id=form.username.data, user_ip=request.remote_addr)
        db.session.add(Addlog)
        db.session.commit()

        flash(f'Registrasi {form.username.data} Berhasi', 'success')
        return redirect(url_for('login'))

    return render_template('regis.html', form=form)

@app.route('/logout')
def logout():
    aksi = "/logout"
    Addlog = History(aksi=aksi, user_id=current_user.username, user_ip=request.remote_addr)
    db.session.add(Addlog)
    db.session.commit()
    logout_user()
    return redirect(url_for('home'))

@app.route('/new_post', methods=['GET', 'POST'])
@login_required
def new_post(): 
    form = PostForm()
    if form.validate_on_submit():
        post = Post(isi = form.isi.data, author=current_user)
        db.session.add(post)
        db.session.commit()

        
        Addlog = History(aksi=form.isi.data, user_id=current_user.username, user_ip=request.remote_addr)
        db.session.add(Addlog)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('isi_konten.html', title='isi konten', form=form)

@app.route('/log', methods=['GET', 'POST'])
@login_required
def log():
    his = History.query.order_by(desc(History.id))
    return render_template('history.html', his=his)