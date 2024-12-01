from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class VehicleForm(FlaskForm):
    brand = StringField('Brand', validators=[DataRequired()])
    model = StringField('Model', validators=[DataRequired()])
    vehicle_type = SelectField('Type', choices=[('car', 'Car'), ('motorcycle', 'Motorcycle')],
                               validators=[DataRequired()])
    num_doors = IntegerField('Number of Doors')
    has_sidecar = BooleanField('Has Sidecar')
    create = SubmitField('Create')

