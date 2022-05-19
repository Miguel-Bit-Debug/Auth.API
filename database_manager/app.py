from flask import Flask, render_template, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, template_folder='template')

app.config["SECRET_KEY"] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///app.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True, index=True)
    password = db.Column(db.String(200), nullable=False)
    profile = db.relationship('Profile', backref='user', uselist=False)

    def __str__(self):
        return self.name


class Profile(db.Model):
    __tablename__ = "profiles"

    id = db.Column(db.Integer, primary_key=True)
    photo = db.Column(db.Unicode(124), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __str__(self):
        return self.name


@app.route('/')
def index():
    users = User.query.all()
    return render_template('users.html', users=users)


@login_manager.user_loader
def current_user(user_id):
    return User.query.get(user_id)


@app.route('/user/delete/<int:id>')
def delete(id):
    user = User.query.filter_by(id=id).first()
    db.session.delete(user)
    db.session.commit()

    return redirect('/')


@app.route('/user/<int:id>')
@login_required
def info(id):
    user = User.query.get(id)
    return render_template('user.html', user=user)


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user = User()
        user.name = request.form['name']
        user.email = request.form['email']
        user.password = generate_password_hash(request.form['password'])

        db.session.add(user)
        db.session.commit()

        return redirect(url_for("index"))

    return render_template('register.html')


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if not user:
            return redirect(url_for('login'))

        if not check_password_hash(user.password, password):
            return redirect(url_for('login'))

        login_user(user)
        return redirect(url_for('index'))


    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
