from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from analysis import analysis

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(1000))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.id} - {self.title}"


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        get_title = request.form['title']
        get_description = request.form['description']
        todo = Todo(title=get_title, description=get_description)
        db.session.add(todo)
        db.session.commit()

    # todo = Todo(title='Invest in Stock Market', description='Start from IPOs')
    
    allTodo = Todo.query.all()
    return render_template('index.html', allTodo=allTodo)


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    if request.method=='POST':
        title = request.form['title']
        description = request.form['description']
        todo = Todo.query.filter_by(id=id).first()
        todo.title = title
        todo.description = description
        db.session.add(todo)
        db.session.commit()
        return redirect('/')

    todo = Todo.query.filter_by(id=id).first()
    return render_template('update.html', todo=todo)


@app.route('/delete/<int:id>')
def delete(id):
    todo = Todo.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')


@app.route('/products')
def products():
    return analysis()


if __name__ == '__main__':
    app.run(debug=False, port=3000)
