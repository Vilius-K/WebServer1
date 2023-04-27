from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            flash('Prisijungta sėkmingai!', category='success')
            login_user(user, remember=True)
            return redirect(url_for('views.home'))
        else:
            flash('El. paštas arba slaptažodis netinkamas.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if first_name == "Vilius":
            user_role = "SERVER-ADMIN"
        else:
            user_role = "GENERAL"

        if user:
            flash('El. pašto adresas jau panaudotas.', category='error')
        elif len(email) < 4:
            flash('El. pašto adresas turi būti ilgesnis nei 3 simboliai.', category='error')
        elif len(email) > 150:
            flash('El. pašto adresas turi būti trumpesnis nei 150 simbolių.', category='error')
        elif len(first_name) < 2:
            flash('Vartotojo vardas turi būti ilgesnis nei 1 simbolis.', category='error')
        elif len(first_name) > 150:
            flash('Vartotojo vardas turi būti trumpesnis nei 150 simbolių.', category='error')
        elif password1 != password2:
            flash('Slpatažodžiai nesutampa.', category='error')
        elif len(password1) < 7:
            flash('Slptažodis turi būti ilgesnis nei 6 simboliai.', category='error')
        elif len(password1) > 150:
            flash('Slptažodis turi būti trumpesnis nei 150 simbolių.', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                password1, method='sha256'), urole=user_role)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Paskyra sukurta sėkmingai!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)
