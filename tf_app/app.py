from flask import Flask, render_template, request, redirect, url_for, session
from models import db, User, QuizRecord
import uuid

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

questions = [
    {"id": 1, "text": "Is Python dynamically typed?", "answer": True},
    {"id": 2, "text": "Does Python support multiple inheritance?", "answer": True},
    # 他8問追加
]


@ app.before_first_request
def create_tables():
    db.create_all()


@app.route('/')
def qr_landing():
    return redirect(url_for('signup'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        unique_name = f"{username}_{str(uuid.uuid4())[:8]}"
        user = User(username=username, unique_name=unique_name)
        db.session.add(user)
        db.session.commit()
        session['user_id'] = user.id
        return redirect(url_for('main_menu'))
    return render_template('signup.html')


@app.route('/main_menu')
def main_menu():
    return render_template('main_menu.html')


@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if request.method == 'POST':
        user_id = session.get('user_id')
        user_answers = request.form.to_dict()
        correct_answers = sum(
            1 for q_id, ans in user_answers.items() 
            if questions[int(q_id) - 1]['answer'] == (ans == 'true')
        )
        record = QuizRecord(user_id=user_id, score=correct_answers)
        db.session.add(record)
        db.session.commit()
        return redirect(url_for('ranking'))
    return render_template('quiz.html', questions=questions)


@app.route('/ranking')
def ranking():
    results = (
        db.session.query(User.username, db.func.sum(QuizRecord.score).label('score'))
        .join(QuizRecord, User.id == QuizRecord.user_id)
        .group_by(User.username)
        .order_by(db.desc('score'))
        .all()
    )
    return render_template('ranking.html', results=results)


if __name__ == '__main__':
    app.run(debug=True)
