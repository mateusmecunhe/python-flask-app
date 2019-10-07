from flask import Flask, render_template, url_for, request, Response, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from bmi import calculate_bmi

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task: %r>' % self.id 

class Pacient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    weight = db.Column(db.Integer, default=0)
    height = db.Column(db.Integer, default=0)
    bmi = db.Column(db.Float, default=0)

    def __repr__(self):
        return '<Pacient: %r>' % self.id 


# @app.route('/', methods=['POST', 'GET'])
# def index():
#     if request.method == 'POST':
#         task_content = request.form['content']
#         new_task = Todo(content=task_content)

#         try:
#             db.session.add(new_task)
#             db.session.commit()
#             return redirect('/')
#         except:
#             return 'error adding your task'

#     else:
#         #tasks = Todo.query.order_by(Todo.date_created).all()
#         return render_template('index.html', tasks=tasks)

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

# controlling bmi calculation traffic

@app.route('/bmi', methods=['POST', 'GET'])
def bmi_calc():
    if request.method == "GET":
        pacients = Pacient.query.all()
        for p in pacients:
            print(p.name)
            print(p.bmi)
        print(len(pacients))
        return render_template('bmi-calc/bmi-calculation.html', pacients=pacients)
    elif request.method == "POST":
        pacient_name = request.form['name']
        pacient_weight = int(request.form['weight'])
        pacient_height = int(request.form['height'])
        pacient_bmi = calculate_bmi(height=pacient_height, weight=pacient_weight)
        pacient = Pacient(name=pacient_name, height=pacient_height, weight=pacient_weight, bmi=pacient_bmi)

        try:
            db.session.add(pacient)
            db.session.commit()
            return redirect('/bmi')
        except:
            return 'error calculating your bmi'
        pass


@app.route('/bmi/delete/<int:id>')
def delete_pacient(id):
    pacient_to_delete = Pacient.query.get_or_404(id)
    
    try:
        db.session.delete(pacient_to_delete)
        db.session.commit()
        return redirect('/bmi')
    except:
        return 'error trying to delete'
    

if __name__ == '__main__':
    app.run(debug=True)

