from flask import Flask, render_template, url_for, request, Response, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from bmi import bmi_bp



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.secret_key = 'os.urandom(24)'
app.register_blueprint(bmi_bp)
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task: %r>' % self.id 

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/task', methods=['POST', 'GET'])
def task_master():
    if request.method == "GET":
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('task-manager/task-master.html', tasks=tasks)
    elif request.method == "POST":
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/task')
        except:
            return 'error adding your task'


@app.route('/task/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/task')
    except:
        return 'error trying to delete'

@app.route('/task/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/task')

        except:
            return 'error while trying to update'
    else:
        return render_template('task-manager/update.html', task=task)


if __name__ == '__main__':
    
    app.run(debug=True)

