import os
import smtplib
from email.header import Header
from email.mime.text import MIMEText

from flask import Flask, render_template, url_for, session, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Супер секретный мод на майнкрафт'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tetropentada.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    mail = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    name = db.Column(db.String(80), unique=False, nullable=False)
    surname = db.Column(db.String(80), unique=False, nullable=False)
    avatar = db.Column(db.String(80), unique=False, nullable=False)

    def __repr__(self):
        return '<User {} {} {} {} {} {} {}>'.format(
            self.id, self.username, self.mail, self.password, self.name,
            self.surname, self.avatar)


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=False, nullable=False)
    content = db.Column(db.String(80), unique=False, nullable=False)
    tag = db.Column(db.String(80), unique=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('Questions', lazy=True))

    def __repr__(self):
        return '<Question {} {} {} {} {}>'.format(
            self.id, self.title, self.tag, self.content, self.user_id)


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(80), unique=False, nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'),
                            nullable=False)
    question = db.relationship('Question',
                               backref=db.backref('Answers', lazy=True))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('Answers', lazy=True))

    def __repr__(self):
        return '<Answer {} {} {} {}>'.format(
            self.id, self.content, self.user_id, self.question_id)


db.create_all()


class SingInForm(FlaskForm):
    username = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])
    submit = SubmitField('Войти')


class RegistrationForm(FlaskForm):
    name = StringField(validators=[DataRequired()])
    surname = StringField(validators=[DataRequired()])
    username = StringField(validators=[DataRequired()])
    mail = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')


class ProfileAddPhotoForm(FlaskForm):
    photo = FileField(validators=[FileRequired(),
                                  FileAllowed(['jpg', 'png'], 'Images only!')])
    submit = SubmitField('Загрузить фото')


class AddQuestionForm(FlaskForm):
    title = StringField(validators=[DataRequired()])
    content = TextAreaField(validators=[DataRequired()])
    tags = SelectField(choices=[('#Авто, Мото', 'Авто, Мото'),
                                ('#Бизнес, Финансы', 'Бизнес, Финансы'),
                                ('#Города и Страны', 'Города и Страны'),
                                ('#Гороскопы, Магия, Гадания',
                                 'Гороскопы, Магия, Гадания'),
                                ('#Домашние задания', 'Домашние задания'),
                                ('#Досуг, Развлечения', 'Досуг, Развлечения'),
                                ('#Еда, Кулинария', 'Еда, Кулинария'),
                                ('#Животные, Растения', 'Животные, Растения'),
                                ('#Знакомства, Любовь, Отношения',
                                 'Знакомства, Любовь, Отношения'),
                                ('#Искусство и Культура',
                                 'Искусство и Культура'),
                                ('#Компьютерные и Видео игры',
                                 'Компьютерные и Видео игры'),
                                ('#Компьютеры, Связь', 'Компьютеры, Связь'),
                                ('#Красота и Здоровье', 'Красота и Здоровье'),
                                ('#Наука, Техника, Языки',
                                 'Наука, Техника, Языки'),
                                ('#Образование', 'Образование'),
                                ('#Общество, Политика, СМИ',
                                 'Общество, Политика, СМИ'),
                                ('#Программирование', 'Программирование'),
                                ('#Путешествия, Туризм', 'Путешествия, Туризм'),
                                ('#Работа, Карьера', 'Работа, Карьера'),
                                ('#Семья, Дом, Дети', 'Семья, Дом, Дети'),
                                ('#Спорт', 'Спорт'),
                                ('#Стиль, Мода, Звезды', 'Стиль, Мода, Звезды'),
                                ('#Товары и Услуги', 'Товары и Услуги'),
                                ('#Философия, Непознанное',
                                 'Философия, Непознанное'),
                                ('#Юмор', 'Юмор')])
    submit = SubmitField('Добавить вопрос')


class AnswerQuestionForm(FlaskForm):
    content = TextAreaField(validators=[DataRequired()])
    submit = SubmitField('Ответить')


def send_notification(question, user, answer, email):
    # Настройки
    mail_sender = 'tetropentada@mail.ru'
    mail_receiver = email
    username = user
    password = 'minecraft3301'
    server = smtplib.SMTP('smtp.mail.ru:587')

    print(question)
    print(user)
    print(answer)
    print(email)

    # Формируем тело письма
    subject = 'Вы получили ответ на свой вопрос!'
    body = str(user) + ' ответил на ваш вопрос "' + str(question) + '"!'
    body += '"' + str(answer) + '"'
    msg = MIMEText(body, 'plain', 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')

    print(body)

    # Отпавляем письмо
    server.starttls()
    server.ehlo()
    server.login(username, password)
    server.sendmail(mail_sender, mail_receiver, msg.as_string())
    server.quit()


@app.route("/")
@app.route("/main")
def main():
    if session.get('username'):
        return render_template("main.html", title='Tetropentada',
                               style=url_for('static', filename='cover.css'),
                               bootstrap=url_for('static',
                                                 filename='bootstrap.min.css'),
                               icon=url_for('static',
                                            filename='images/icon.png'))
    return render_template("main.html", title='Tetropentada',
                           style=url_for('static', filename='cover.css'),
                           bootstrap=url_for('static',
                                             filename='bootstrap.min.css'),
                           icon=url_for('static', filename='images/icon.png'))


@app.route("/sign_in", methods=['POST', 'GET'])
def sign_in():
    form = SingInForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).filter_by(
            password=password).first()
        if user:
            session['username'] = username
            session['user_id'] = user.id
            return redirect("/main")
        return render_template("wrong_sign_in.html", title='Tetropentada',
                               form=form,
                               style=url_for('static', filename='cover.css'),
                               bootstrap=url_for('static',
                                                 filename='bootstrap.min.css'),
                               icon=url_for('static',
                                            filename='images/icon.png'))
    return render_template("sign_in.html", title='Tetropentada', form=form,
                           style=url_for('static', filename='cover.css'),
                           bootstrap=url_for('static',
                                             filename='bootstrap.min.css'),
                           icon=url_for('static', filename='images/icon.png'))


@app.route("/registration", methods=['POST', 'GET'])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        if not User.query.filter_by(username=username).first():
            user = User(username=username, mail=form.mail.data,
                        password=form.password.data,
                        name=form.name.data, surname=form.surname.data,
                        avatar='guest.png')
            db.session.add(user)
            db.session.commit()
            session['username'] = username
            session['user_id'] = user.id
            return redirect("/index/0")
        return render_template("wrong_registration.html", title='Tetropentada',
                               form=form,
                               style=url_for('static', filename='cover.css'),
                               bootstrap=url_for('static',
                                                 filename='bootstrap.min.css'),
                               icon=url_for('static',
                                            filename='images/icon.png'))
    return render_template("registration.html", title='Tetropentada', form=form,
                           style=url_for('static', filename='cover.css'),
                           bootstrap=url_for('static',
                                             filename='bootstrap.min.css'),
                           icon=url_for('static', filename='images/icon.png'))


@app.route("/index/<int:my_quests>")
def index(my_quests):
    if my_quests:
        if session.get('username'):
            return render_template("index.html", title='Tetropentada',
                                   my_quests=True,
                                   questions=Question.query.filter_by(
                                       user_id=session['user_id']),
                                   style=url_for('static',
                                                 filename='cover.css'),
                                   bootstrap=url_for('static',
                                                     filename='bootstrap.min.css'),
                                   icon=url_for('static',
                                                filename='images/icon.png'))
        return redirect("/sign_in")
    return render_template("index.html", title='Tetropentada', my_quests=False,
                           questions=Question.query.all(),
                           style=url_for('static', filename='cover.css'),
                           bootstrap=url_for('static',
                                             filename='bootstrap.min.css'),
                           icon=url_for('static', filename='images/icon.png'))


@app.route("/add_question", methods=['POST', 'GET'])
def add_question():
    if session.get('username'):
        form = AddQuestionForm()
        if form.validate_on_submit():
            user = User.query.filter_by(id=session['user_id']).first()
            user.Questions.append(
                Question(title=form.title.data, content=form.content.data,
                         tag=form.tags.data,
                         user_id=session['user_id']))
            db.session.commit()
            return redirect("/index/1")
        return render_template("add_question.html", title='Tetropentada',
                               form=form,
                               style=url_for('static', filename='cover.css'),
                               bootstrap=url_for('static',
                                                 filename='bootstrap.min.css'),
                               icon=url_for('static',
                                            filename='images/icon.png'))
    return redirect("/sign_in")


@app.route("/profile/<int:id>", methods=['POST', 'GET'])
def profile(id):
    if session.get('username'):
        form = ProfileAddPhotoForm()
        user = User.query.filter_by(id=id).first()
        if form.validate_on_submit():
            exp = secure_filename(form.photo.data.filename)[-3:]
            if user.avatar == 'guest.png':
                avatar_name = "{}1.{}".format(user.username, exp)
            else:
                os.remove(
                    '{}/static/avatars/{}'.format(os.getcwd(), user.avatar))
                avatar_name = "{}{}.{}".format(user.username, int(
                    user.avatar[len(user.username):-4]) + 1, exp)
            form.photo.data.save(
                "{}/static/avatars/{}".format(os.getcwd(), avatar_name))
            user.avatar = avatar_name
            db.session.commit()
            return redirect("/profile/{}".format(id))
        avatar_name = user.avatar
        return render_template("profile.html", title='Tetropentada',
                               style=url_for('static', filename='cover.css'),
                               bootstrap=url_for('static',
                                                 filename='bootstrap.min.css'),
                               form=form,
                               icon=url_for('static',
                                            filename='images/icon.png'),
                               avatar=url_for('static',
                                              filename='avatars/{}'.format(
                                                  avatar_name)),
                               username=User.query.filter_by(
                                   id=id).first().username)
    return redirect("/sign_in")


@app.route("/single_question/<int:id>", methods=['POST', 'GET'])
def single_question(id):
    form = AnswerQuestionForm()
    if form.validate_on_submit():
        if session.get('username'):
            user = User.query.filter_by(id=session['user_id']).first()
            question = Question.query.filter_by(id=id).first()
            answer = Answer(content=form.content.data,
                            user_id=session['user_id'], question_id=id)
            user.Answers.append(answer)
            question.Answers.append(answer)
            db.session.commit()
            # send_notification(question, user, answer,
            #                  User.query.filter_by(id=session['user_id']).first().mail)
            return redirect("/single_question/{}".format(id))
        return redirect("/sign_in")
    question = Question.query.filter_by(id=id).first()
    return render_template("single_question.html", title='Tetropentada',
                           question=question,
                           author=User.query.filter_by(
                               id=question.user_id).first(),
                           form=form,
                           answers=Answer.query.filter_by(question_id=id),
                           User=User,
                           style=url_for('static', filename='cover.css'),
                           bootstrap=url_for('static',
                                             filename='bootstrap.min.css'),
                           icon=url_for('static', filename='images/icon.png'))


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


app.run(port=8080, host='127.0.0.1', debug=True)
