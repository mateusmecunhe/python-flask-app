from flask import Flask, render_template, url_for, request, Response, redirect, Blueprint, flash
from flask_sqlalchemy import SQLAlchemy
bmi_bp = Blueprint('bmi_bp', __name__, url_prefix='/bmi')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Pacient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    weight = db.Column(db.Integer, default=0)
    height = db.Column(db.Integer, default=0)
    bmi = db.Column(db.Float, default=0)

    def __repr__(self):
        return '<Pacient: %r>' % self.id 

def calculate_bmi(height, weight):
    return round(weight/((height/100) * (height/100)), 2)

def validate_pacient(pacient):
    error = ()
    if not pacient.name:
        error = 'name is needed'
    if pacient.weight < 1:
        error = '{} kg is an invalid weight. Try again!'.format(pacient.weight)
    if pacient.height < 1:
        error = '{} cm is invalid. Try again! '.format(pacient.height)

    return error

@bmi_bp.route('/', methods=['POST', 'GET'])
def bmi_calc():
    if request.method == "GET":
        pacients = Pacient.query.all()
        return render_template('bmi-calc/bmi-calculation.html', pacients=pacients)
    elif request.method == "POST":
        pacient_name = request.form['name']
        pacient_weight = int(request.form['weight'])
        pacient_height = int(request.form['height'])
        pacient_bmi = calculate_bmi(height=pacient_height, weight=pacient_weight)
        pacient = Pacient(name=pacient_name, height=pacient_height, weight=pacient_weight, bmi=pacient_bmi)
       
        error = validate_pacient(pacient)
        # flash(error)
        if error is None:
            try:
                db.session.add(pacient)
                db.session.commit()
                return redirect('/bmi')
            except:
                return 'error calculating your bmi'
            pass
        print('********')
        flash(error)
        return redirect('/bmi')


        #flash(error) 


@bmi_bp.route('/delete/<int:id>')
def delete_pacient(id):
    pacient_to_delete = Pacient.query.get_or_404(id)
  
    try:
        db.session.delete(pacient_to_delete)
        db.session.commit()
        return redirect('/bmi')
    except:
        return 'error trying to delete'

@bmi_bp.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    pacient = Pacient.query.get_or_404(id)
    if request.method == 'POST':
        pacient.name = request.form['name']
        pacient.weight = request.form['weight']
        pacient.height = request.form['height']

        try:
            db.session.commit()
            return redirect('/bmi')
        except:
            return 'error trying to update your pacient'
    else:

        return render_template('bmi-calc/update.html', pacient=pacient)
    