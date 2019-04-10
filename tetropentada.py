from LSA import LSA
from flask import Flask, render_template, url_for, session, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, \
    SelectField, BooleanField
from wtforms.validators import DataRequired, Email
from wtforms.fields.html5 import EmailField
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Супер секретный мод на майнкрафт'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tetropentada.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

TAGS = [('Все вопросы', 'Все вопросы'),
        ('Авто, Мото', 'Авто, Мото'),
        ('Бизнес, Финансы', 'Бизнес, Финансы'),
        ('Города и Страны', 'Города и Страны'),
        ('Гороскопы, Магия, Гадания', 'Гороскопы, Магия, Гадания'),
        ('Домашние задания', 'Домашние задания'),
        ('Досуг, Развлечения', 'Досуг, Развлечения'),
        ('Еда, Кулинария', 'Еда, Кулинария'),
        ('Животные, Растения', 'Животные, Растения'),
        ('Знакомства, Любовь, Отношения', 'Знакомства, Любовь, Отношения'),
        ('Искусство и Культура', 'Искусство и Культура'),
        ('Компьютерные и Видео игры', 'Компьютерные и Видео игры'),
        ('Компьютеры, Связь', 'Компьютеры, Связь'),
        ('Красота и Здоровье', 'Красота и Здоровье'),
        ('Наука, Техника, Языки', 'Наука, Техника, Языки'),
        ('Образование', 'Образование'),
        ('Общество, Политика, СМИ', 'Общество, Политика, СМИ'),
        ('Программирование', 'Программирование'),
        ('Путешествия, Туризм', 'Путешествия, Туризм'),
        ('Работа, Карьера', 'Работа, Карьера'),
        ('Семья, Дом, Дети', 'Семья, Дом, Дети'),
        ('Спорт', 'Спорт'),
        ('Стиль, Мода, Звезды', 'Стиль, Мода, Звезды'),
        ('Товары и Услуги', 'Товары и Услуги'),
        ('Философия, Непознанное', 'Философия, Непознанное'),
        ('Юмор', 'Юмор'),
        ('Другое', 'Другое')]


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    mail = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))
    name = db.Column(db.String(80))
    surname = db.Column(db.String(80))
    avatar = db.Column(db.String(80))
    rating = db.Column(db.Integer)
    pos = db.Column(db.Integer)

    def __repr__(self):
        return '<User {} {} {} {} {} {} {} {} {}>'.format(
            self.id, self.username, self.mail, self.password, self.name,
            self.surname, self.avatar, self.pos, self.rating)


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    content = db.Column(db.String(80))
    tag = db.Column(db.String(80))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('Questions', lazy=True))

    def __repr__(self):
        return '<Question {} {} {} {} {}>'.format(
            self.id, self.title, self.tag, self.content, self.user_id)


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(80))
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    best = db.Column(db.Integer, unique=False, nullable=False)
    question = db.relationship('Question', backref=db.backref('Answers', lazy=True))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('Answers', lazy=True))

    def __repr__(self):
        return '<Answer {} {} {} {} {}>'.format(
            self.id, self.content, self.best, self.user_id, self.question_id)


db.create_all()


class SingInForm(FlaskForm):
    username = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])
    submit = SubmitField('Войти')


class SearchAndSort(FlaskForm):
    search = StringField()
    submit = SubmitField('Найти')
    sort = SelectField(choices=TAGS)
    checkbox = BooleanField('Умная сортировка')
    submit_for_sort = SubmitField('Отсортировать по категории')


class RegistrationForm(FlaskForm):
    name = StringField(validators=[DataRequired()])
    surname = StringField(validators=[DataRequired()])
    username = StringField(validators=[DataRequired()])
    mail = EmailField(validators=[DataRequired(), Email()])
    password = PasswordField(validators=[DataRequired()])
    pos = SelectField(choices=[('Я - участник', 'Я - участник'),
                               ('Я - модератор', 'Я - модератор')])
    submit = SubmitField('Зарегистрироваться')


class ProfileAddPhotoForm(FlaskForm):
    photo = FileField(validators=[FileRequired(), FileAllowed(['jpg', 'png'], 'Images only!')])
    submit = SubmitField('Загрузить фото')


class AddQuestionForm(FlaskForm):
    title = StringField(validators=[DataRequired()])
    content = TextAreaField(validators=[DataRequired()])
    tags = SelectField(choices=TAGS[2:])
    submit = SubmitField('Добавить вопрос')


class AnswerQuestionForm(FlaskForm):
    content = TextAreaField(validators=[DataRequired()])
    submit = SubmitField('Ответить')


@app.route("/")
@app.route("/main")
def main():
    if session.get('username'):
        pos = User.query.filter_by(id=session.get('user_id')).first().pos
        return render_template("main.html", title='Tetropentada',
                               style=url_for('static', filename='cover.css'),
                               bootstrap=url_for('static', filename='bootstrap.min.css'), User=User,
                               icon=url_for('static', filename='images/icon.png'),
                               status=get_status(pos))
    return render_template("main.html", title='Tetropentada',
                           style=url_for('static', filename='cover.css'),
                           bootstrap=url_for('static', filename='bootstrap.min.css'),
                           icon=url_for('static', filename='images/icon.png'), User=User)


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
        return render_template("wrong_sign_in.html", title='Tetropentada', form=form,
                               style=url_for('static', filename='cover.css'),
                               bootstrap=url_for('static', filename='bootstrap.min.css'),
                               icon=url_for('static', filename='images/icon.png'), User=User)
    return render_template("sign_in.html", title='Tetropentada', form=form,
                           style=url_for('static', filename='cover.css'),
                           bootstrap=url_for('static', filename='bootstrap.min.css'),
                           icon=url_for('static', filename='images/icon.png'), User=User)


@app.route("/requests", methods=['POST', 'GET'])
def requests():
    users = User.query.filter_by(pos=1).all()
    return render_template('requests.html', title='Tetropentada', User=User, users=users,
                           style=url_for('static', filename='cover.css'),
                           bootstrap=url_for('static', filename='bootstrap.min.css'),
                           icon=url_for('static', filename='images/icon.png'))


@app.route("/registration", methods=['POST', 'GET'])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        mail = form.mail.data
        if User.query.filter_by(mail=mail).first():
            return render_template("wrong_registration.html", title='Tetropentada', form=form,
                                   message='Такой e-mail уже занят',
                                   style=url_for('static', filename='cover.css'),
                                   bootstrap=url_for('static', filename='bootstrap.min.css'),
                                   icon=url_for('static', filename='images/icon.png'))
        if User.query.filter_by(username=username).first():
            return render_template("wrong_registration.html", title='Tetropentada', form=form,
                                   message='Такое имя пользователя уже занято',
                                   style=url_for('static', filename='cover.css'),
                                   bootstrap=url_for('static', filename='bootstrap.min.css'),
                                   icon=url_for('static', filename='images/icon.png'))
        pos = 1
        if form.pos == 'Я - участник':
            pos = 0
        user = User(username=username, mail=mail,
                    password=form.password.data,
                    name=form.name.data, surname=form.surname.data,
                    avatar='guest.png', rating=0, pos=pos)
        db.session.add(user)
        db.session.commit()
        session['username'] = username
        session['user_id'] = user.id
        return redirect("/index/0/none")
    return render_template("registration.html", title='Tetropentada', form=form, User=User,
                           style=url_for('static', filename='cover.css'),
                           bootstrap=url_for('static', filename='bootstrap.min.css'),
                           icon=url_for('static', filename='images/icon.png'))


@app.route("/index/<int:my_quests>/<tag>", methods=['POST', 'GET'])
def index(my_quests, tag):
    form = SearchAndSort()
    questions = Question.query.all()

    if form.validate_on_submit():
        if form.checkbox.data:
            tag = form.sort.data
            if tag != 'Все вопросы':
                sorted_questions = []
                for quest in questions:
                    if quest.tag == tag:
                        sorted_questions.append(quest)
            else:
                sorted_questions = questions.copy()
            try:
                sorted_titles = LSA(form.search.data,
                                    [question.title for question in sorted_questions]).main()
                sorted_questions = sorted(sorted_questions,
                                          key=lambda question: sorted_titles.index(question.title))
            except:
                pass
        else:
            search = form.search.data
            tag = form.sort.data
            if tag != 'Все вопросы':
                sorted_questions = []
                for quest in questions:
                    if quest.tag == tag:
                        sorted_questions.append(quest)
            else:
                sorted_questions = []
                print(questions)
                for quest in questions:
                    if str(search).upper() in str(quest.title).upper() or str(search).upper() in str(
                            quest.content).upper():
                        sorted_questions.append(quest)
            try:
                sorted_titles = LSA(form.search.data,
                                    [question.title for question in sorted_questions]).main()
                sorted_questions = sorted(sorted_questions,
                                          key=lambda question: sorted_titles.index(question.title))
            except:
                pass
    elif tag != 'none':
        form.sort.data = tag
        if tag != 'Все вопросы':
            sorted_questions = []
            for quest in questions:
                if quest.tag == tag:
                    sorted_questions.append(quest)
        else:
            sorted_questions = questions.copy()
    else:
        sorted_questions = questions.copy()
        tag = 'none'
    current_user = User.query.filter_by(id=session.get('user_id')).first()
    if my_quests:
        if session.get('user_id'):
            return render_template("index.html", title='Tetropentada',
                                   my_quests=True, form=form, len=len, tag=tag,
                                   questions=[quest for quest in sorted_questions if
                                              quest.user_id == session['user_id']],
                                   style=url_for('static', filename='cover.css'),
                                   bootstrap=url_for('static', filename='bootstrap.min.css'),
                                   icon=url_for('static', filename='images/icon.png'),
                                   User=User, current_user=current_user)
        return redirect("/sign_in")
    return render_template("index.html", title='Tetropentada', my_quests=False,
                           len=len, tag=tag,
                           questions=sorted_questions, form=form,
                           style=url_for('static', filename='cover.css'),
                           bootstrap=url_for('static', filename='bootstrap.min.css'),
                           icon=url_for('static', filename='images/icon.png'),
                           User=User, current_user=current_user)


@app.route("/add_question", methods=['POST', 'GET'])
def add_question():
    if session.get('username'):
        form = AddQuestionForm()
        if form.validate_on_submit():
            user = User.query.filter_by(id=session['user_id']).first()
            user.Questions.append(Question(title=form.title.data, content=form.content.data,
                                           user_id=session['user_id'], tag=form.tags.data))
            db.session.commit()
            return redirect("/index/1/none")
        return render_template("add_question.html", title='Tetropentada',
                               form=form,
                               style=url_for('static', filename='cover.css'),
                               bootstrap=url_for('static', filename='bootstrap.min.css'),
                               icon=url_for('static', filename='images/icon.png'), User=User)
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
                os.remove('{}/static/avatars/{}'.format(os.getcwd(), user.avatar))
                avatar_name = "{}{}.{}".format(user.username,
                                               int(user.avatar[len(user.username):-4]) + 1, exp)
            form.photo.data.save("{}/static/avatars/{}".format(os.getcwd(), avatar_name))
            user.avatar = avatar_name
            db.session.commit()
            return redirect("/profile/{}".format(id))
        avatar_name = user.avatar
        pos = User.query.filter_by(id=id).first().pos
        session_user = User.query.filter_by(id=session['user_id']).first()
        return render_template("profile.html", title='Tetropentada', User=User, session_user=session_user,
                               style=url_for('static', filename='cover.css'),
                               bootstrap=url_for('static', filename='bootstrap.min.css'),
                               form=form, user=user, status=get_status(pos),
                               icon=url_for('static', filename='images/icon.png'),
                               avatar=url_for('static', filename='avatars/{}'.format(avatar_name)))
    return redirect("/sign_in")


@app.route("/single_question/<int:id>", methods=['POST', 'GET'])
def single_question(id):
    form = AnswerQuestionForm()
    if form.validate_on_submit():
        if session.get('username'):
            pos = User.query.filter_by(id=session['user_id']).first().pos
            if pos != 3:
                user = User.query.filter_by(id=session['user_id']).first()
                question = Question.query.filter_by(id=id).first()
                answer = Answer(content=form.content.data,
                                user_id=session['user_id'], best=0, question_id=id)
                user.Answers.append(answer)
                question.Answers.append(answer)
                db.session.commit()
                question = Question.query.filter_by(id=answer.question_id).first()
                user1 = User.query.filter_by(id=question.user_id).first()
                send_notification(user1.mail,
                                  "Пользователь {} дал ответ на ваш вопрос \"{}\"\n\n{}".format(user1.username,
                                                                                                question.title,
                                                                                                answer.content))
                return redirect("/single_question/{}".format(id))
            return redirect("/single_question/{}".format(id))
        return redirect("/sign_in")
    question = Question.query.filter_by(id=id).first()
    answers = Answer.query.filter_by(question_id=id)
    return render_template("single_question.html", title='Tetropentada',
                           question=question,
                           author=User.query.filter_by(id=question.user_id).first(),
                           form=form, User=User, answers=answers,
                           answers_list=sorted(answers, key=lambda x: x.best, reverse=True),
                           style=url_for('static', filename='cover.css'),
                           bootstrap=url_for('static', filename='bootstrap.min.css'),
                           icon=url_for('static', filename='images/icon.png'))


@app.route("/delete_question/<int:id>")
def delete_question(id):
    db.session.delete(Question.query.filter_by(id=id).first())
    db.session.commit()
    return redirect("/index/0/none")


@app.route("/sign_out")
def sign_out():
    session.pop('username')
    session.pop('user_id')
    return redirect("/main")


@app.route("/best_answer/<int:user_id>/<int:quest_id>/<int:answer_id>/<int:set>")
def best_answer(user_id, quest_id, answer_id, set):
    if set:
        User.query.filter_by(id=user_id).first().rating += 10
        Answer.query.filter_by(id=answer_id).first().best = 1
    else:
        User.query.filter_by(id=user_id).first().rating -= 10
        Answer.query.filter_by(id=answer_id).first().best = 0
    db.session.commit()
    return redirect("/single_question/{}".format(quest_id))


@app.route("/bad_answer/<int:user_id>/<int:quest_id>/<int:answer_id>/<int:set>")
def bad_answer(user_id, quest_id, answer_id, set):
    if set:
        User.query.filter_by(id=user_id).first().rating -= 4
        Answer.query.filter_by(id=answer_id).first().best = -1
    else:
        User.query.filter_by(id=user_id).first().rating += 4
        Answer.query.filter_by(id=answer_id).first().best = 0
    db.session.commit()
    return redirect("/single_question/{}".format(quest_id))


@app.route("/set_user_position/<int:user_id>/<int:pos>")
def set_user_position(user_id, pos):
    User.query.filter_by(id=user_id).first().pos = pos
    db.session.commit()
    if session['user_id'] == 0:
        return redirect("/requests")
    return redirect("/index/0/none")


@app.route("/set_ban_status/<int:user_id>/<int:pos>")
def set_ban_status(user_id, pos):
    user = User.query.filter_by(id=user_id).first()
    user.pos = pos
    if pos == 0:
        for quest in user.Questions:
            db.session.delete(quest)
    db.session.commit()
    return redirect("/profile/{}".format(user_id))


def get_status(pos):
    if pos == 0:
        return 'Участник'
    elif pos == 1:
        return 'Участник (отправен запрос на модерацию)'
    elif pos == 2:
        return 'Модератор'
    elif pos == 3:
        return 'Забанен'
    return 'Супер админ'


def send_notification(to, msg):
    smtpObj = smtplib.SMTP('smtp.yandex.ru', 587)
    smtpObj.ehlo()
    smtpObj.starttls()

    from_ = "mark.2406@yandex.ru"
    smtpObj.login(from_, 'Mark.240607777777sssssss')

    msg = MIMEText(msg, 'plain', 'utf-8')
    msg['Subject'] = Header('Вы получили ответ на свой вопрос', 'utf-8')
    msg['From'] = from_
    msg['To'] = to

    smtpObj.sendmail(from_, to, msg.as_string())
    smtpObj.quit()


app.run(port=8080, host='127.0.0.1')
