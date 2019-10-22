from flask import Flask, render_template, url_for, request, Response, redirect, Blueprint, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
import json
bmi_bp = Blueprint('bmi_bp', __name__, url_prefix='/bmi')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Pacient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    weight = db.Column(db.Float, default=0)
    height = db.Column(db.Float, default=0)
    bmi = db.Column(db.Float, default=0)

    def __repr__(self):
        return '<Pacient: %r>' % self.id 

def calculate_bmi(height, weight):
    height_in_m = height/100
    height_in_m_squared = height_in_m * height_in_m
    bmi = (weight/height_in_m_squared)
    return round(bmi, 2)

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
        pacient_weight = float(request.form['weight'])
        pacient_height = float(request.form['height'])
        
        pacient_bmi = calculate_bmi(height=pacient_height, weight=pacient_weight)
        print(pacient_bmi)
        pacient = Pacient(name=pacient_name, height=pacient_height, weight=pacient_weight, bmi=pacient_bmi)
       
        error = validate_pacient(pacient)
        # flash(error)
        if len(error) is 0:
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
    
@bmi_bp.route('/rest', methods=['POST', 'GET'])
def json_data():
    if request.method == 'POST':
        pacient_posted = request.get_json()
        pacient_posted_name = pacient_posted['name']
        pacient_posted_height = float(pacient_posted['height'])
        pacient_posted_weight = float(pacient_posted['weight'])
        pacient_posted_bmi = calculate_bmi(height=pacient_posted_height, weight=pacient_posted_weight)

        pacient = Pacient(name=pacient_posted_name, height=pacient_posted_height, weight=pacient_posted_weight, bmi=pacient_posted_bmi)
        print(type(pacient))

        pacient_dict = {}
        pacient_dict["name"] = str(pacient.name)
        pacient_dict["weight"] = str(pacient.weight)
        pacient_dict["height"] = str(pacient.height)
        pacient_dict["bmi"] = str(pacient.bmi)
        print(pacient.id)
    
        print(type(pacient_dict))
        print(pacient_dict)
            
        try:
            db.session.add(pacient)
            db.session.commit()
            return json.dumps(pacient_dict)
        except:
            return 'error calculating your bmi'
        return 'hey'
    else:
        pacients = Pacient.query.all()
        pacients_list = []
        for pacient in pacients:
            pacient_dict = {}
            pacient_dict["name"] = str(pacient.name)
            pacient_dict["weight"] = str(pacient.weight)
            pacient_dict["height"] = str(pacient.height)
            pacient_dict["bmi"] = str(pacient.bmi)
            pacients_list.append(pacient_dict)
        pacients_json = json.dumps(pacients_list, sort_keys=True)
        print(type(pacients_json))
        print(json.loads(pacients_json))
        return pacients_json


@bmi_bp.route('/rest/<int:id>', methods=['PUT', 'DELETE'])
def json_update_or_delete(id):
    if request.method == 'PUT':
        pacient = Pacient.query.get_or_404(id)
        pacient_put = request.get_json()

        pacient.name = pacient_put['name']
        pacient.height = pacient_put['height']
        pacient.weight = pacient_put['weight']
        pacient.bmi = calculate_bmi(height=float(pacient.height), weight=float(pacient.weight))
        try:
            db.session.commit()
        except:
            "error trying to update"
        return f'pacient {pacient.name} updated successfully'

    elif request.method == "DELETE":
        pacient_to_delete = Pacient.query.get_or_404(id)
        try:
            db.session.delete(pacient_to_delete)
            db.session.commit()
        except:
            "error trying to delete"
        return 'pacient deleted'
