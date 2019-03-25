from flask import Flask, render_template, url_for, session, redirect
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Супер секретный мод на майнкрафт'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tetropentada.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    name = db.Column(db.String(80), unique=False, nullable=False)
    surname = db.Column(db.String(80), unique=False, nullable=False)

    def __repr__(self):
        return '<User {} {} {} {} {}>'.format(
            self.id, self.username, self.password, self.name, self.surname)


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=False, nullable=False)
    content = db.Column(db.String(80), unique=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('Questions', lazy=True))

    def __repr__(self):
        return '<Question {} {} {} {}>'.format(
            self.id, self.title, self.content, self.user_id)


db.create_all()


class SingInForm(FlaskForm):
    username = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])
    submit = SubmitField('Войти')


class RegistrationForm(FlaskForm):
    name = StringField(validators=[DataRequired()])
    surname = StringField(validators=[DataRequired()])
    username = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')


class AddQuestionForm(FlaskForm):
    title = StringField(validators=[DataRequired()])
    content = TextAreaField(validators=[DataRequired()])
    submit = SubmitField('Добавить вопрос')


@app.route("/")
@app.route("/main")
def main():
    return render_template("main.html", title='Tetropentada main page',
                           style=url_for('static', filename='cover.css'),
                           bootstrap=url_for('static', filename='Bootstrap v3.1.1/dist/css/bootstrap.min.css'),
                           icon=url_for('static', filename='images/icon.png'))


@app.route("/sign_in", methods=['POST', 'GET'])
def sign_in():
    form = SingInForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).filter_by(password=password).first()
        if user:
            session['username'] = username
            session['user_id'] = user.id
            return redirect("/main")
        return render_template("wrong_sign_in.html", title='Tetropentada sign in', form=form,
                               style=url_for('static', filename='sign_in.css'),
                               bootstrap=url_for('static', filename='Bootstrap v3.1.1/dist/css/bootstrap.min.css'))
    return render_template("sign_in.html", title='Tetropentada sign in', form=form,
                           style=url_for('static', filename='sign_in.css'),
                           bootstrap=url_for('static', filename='Bootstrap v3.1.1/dist/css/bootstrap.min.css'))


@app.route("/registration", methods=['POST', 'GET'])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        if not User.query.filter_by(username=username).first():
            user = User(username=username, password=form.password.data,
                        name=form.name.data, surname=form.surname.data)
            db.session.add(user)
            db.session.commit()
            session['username'] = username
            session['user_id'] = user.id
            return redirect("/index")
        return render_template("wrong_registration.html", title='Tetropentada registration', form=form,
                               style=url_for('static', filename='sign_in.css'),
                               bootstrap=url_for('static', filename='Bootstrap v3.1.1/dist/css/bootstrap.min.css'))
    return render_template("registration.html", title='Tetropentada registration', form=form,
                           style=url_for('static', filename='sign_in.css'),
                           bootstrap=url_for('static', filename='Bootstrap v3.1.1/dist/css/bootstrap.min.css'))


@app.route("/index/<int:my_quests>")
def index(my_quests):
    if my_quests:
        if session.get('username'):
            return render_template("index.html", title='Tetropentada my_questions', my_quests=True,
                                   questions=Question.query.filter_by(user_id=session['user_id']),
                                   style=url_for('static', filename='cover.css'),
                                   bootstrap=url_for('static', filename='Bootstrap v3.1.1/dist/css/bootstrap.min.css'))
        return redirect("/sign_in")
    return render_template("index.html", title='Tetropentada index', my_quests=False,
                           questions=Question.query.all(), style=url_for('static', filename='cover.css'),
                           bootstrap=url_for('static', filename='Bootstrap v3.1.1/dist/css/bootstrap.min.css'))


@app.route("/add_question", methods=['POST', 'GET'])
def add_question():
    if session.get('username'):
        form = AddQuestionForm()
        if form.validate_on_submit():
            user = User.query.filter_by(id=session['user_id']).first()
            user.Questions.append(Question(title=form.title.data, content=form.content.data,
                                           user_id=session['user_id']))
            db.session.commit()
            return redirect("/index/1")
        return render_template("add_news.html", title='Tetropentada add_news', form=form,
                               style=url_for('static', filename='sign_in.css'),
                               bootstrap=url_for('static', filename='Bootstrap v3.1.1/dist/css/bootstrap.min.css'))
    return redirect("/sign_in")


@app.route("/delete_question/<int:id>")
def delete_question(id):
    db.session.delete(Question.query.filter_by(id=id).first())
    db.session.commit()
    return redirect("/index/1")


@app.route("/sign_out")
def sign_out():
    session.pop('username')
    session.pop('user_id')
    return redirect("/main")


app.run(port=8080, host='127.0.0.1')
