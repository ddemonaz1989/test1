from flask import Flask, jsonify, request
from flask import render_template

from dao.db_conf import db
import dao.vehicle_db as vehicle_dao
import dao.motorcycle_db as moto_dao
import dao.car_db as car_dao
from forms.new_vehicle import VehicleForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vehicles.db'
app.config['SECRET_KEY'] = 'secret-key'
db.init_app(app)

# Наполнение БД данными
with app.app_context():
    db.drop_all()
    db.create_all()

    vehicle1 = vehicle_dao.VehicleDB(brand='Porsche', model='911', vehicle_type='car')
    vehicle2 = vehicle_dao.VehicleDB(brand='BMW', model='X6', vehicle_type='car')
    vehicle3 = vehicle_dao.VehicleDB(brand='Honda', model='Civic', vehicle_type='car')
    vehicle4 = vehicle_dao.VehicleDB(brand='Harley Davidson', model='Road King', vehicle_type='motorcycle')
    vehicle5 = vehicle_dao.VehicleDB(brand='Harley Davidson', model='Fat Boy', vehicle_type='motorcycle')
    vehicle6 = vehicle_dao.VehicleDB(brand='Harley Davidson', model='Softail', vehicle_type='motorcycle')

    db.session.add_all([
        vehicle1, vehicle2, vehicle3, vehicle4, vehicle5, vehicle6
    ])

    db.session.commit()

    db.session.add_all([
        car_dao.CarDB(num_doors=2, id_vehicle=vehicle1.id),
        car_dao.CarDB(num_doors=4, id_vehicle=vehicle2.id),
        car_dao.CarDB(num_doors=4, id_vehicle=vehicle3.id)
    ])

    db.session.add_all([
        moto_dao.MotorcycleDB(has_sidecar=False, id_vehicle=vehicle4.id),
        moto_dao.MotorcycleDB(has_sidecar=False, id_vehicle=vehicle5.id),
        moto_dao.MotorcycleDB(has_sidecar=False, id_vehicle=vehicle6.id)
    ])

    db.session.commit()


@app.route('/')
@app.route('/vehicles')
def get_vehicles():
    """
    **Эндпоинт:** `GET /vehicles`

         **Пример ответа:**
         ```json
         {
           "vehicles": [
             {"id": 1, "brand": "Toyota", "model": "Camry", "num_doors": 4, "type": "car"},
             {"id": 2, "brand": "Harley-Davidson", "model": "Sportster", "has_sidecar": true, "type": "motorcycle"}
           ]
         }
         ```
    """
    query = db.session.query(vehicle_dao.VehicleDB, car_dao.CarDB, moto_dao.MotorcycleDB). \
        outerjoin(car_dao.CarDB, vehicle_dao.VehicleDB.id == car_dao.CarDB.id_vehicle). \
        outerjoin(moto_dao.MotorcycleDB, vehicle_dao.VehicleDB.id == moto_dao.MotorcycleDB.id_vehicle)

    vehicles = []

    for record in query.all():
        vehicle, car_attr, moto_attr = record
        vehicle_data = {
            "id": vehicle.id,
            "brand": vehicle.brand,
            "model": vehicle.model,
            "type": vehicle.vehicle_type,
        }
        if vehicle.vehicle_type == "car":
            vehicle_data["num_doors"] = car_attr.num_doors
        else:
            vehicle_data["has_sidecar"] = moto_attr.has_sidecar

        vehicles.append(vehicle_data)

    return render_template("home.html", vehicles=vehicles), 200


@app.route('/vehicles/new', methods=['GET', 'POST'])
def create_vehicles():
    """
    **Эндпоинт:** `POST /vehicles`

         **Пример запроса:**
         ```json
         {
           "brand": "Tesla",
           "model": "Model 3",
           "num_doors": 4,
           "type": "car"
         }
         ```

         **Пример ответа:**
         ```json
         {
           "message": "Vehicle added successfully",
           "vehicle": {"id": 3, "brand": "Tesla", "model": "Model 3", "num_doors": 4, "type": "car"}
         }
         ```
    """
    form = VehicleForm()
    if form.validate_on_submit():
        vehicle_type = form.vehicle_type.data

        new_vehicles = vehicle_dao.VehicleDB(
            brand=form.brand.data,
            model=form.model.data,
            vehicle_type=form.vehicle_type.data
        )
        db.session.add(new_vehicles)
        db.session.commit()

        match vehicle_type:
            case "car":
                new_car = car_dao.CarDB(
                    num_doors=form.num_doors.data,
                    id_vehicle=new_vehicles.id
                )
                db.session.add(new_car)
                db.session.commit()

                return jsonify({
                    'message': 'Vehicle added successfully',
                    'vehicle': new_vehicles.to_json(new_car.num_doors)
                }), 201
            case "motorcycle":
                new_moto = moto_dao.MotorcycleDB(
                    id_vehicle=new_vehicles.id,
                    has_sidecar=form.has_sidecar.data
                )
                db.session.add(new_moto)
                db.session.commit()

                return jsonify({
                    'message': 'Vehicle added successfully',
                    'vehicle': new_vehicles.to_json(new_moto.has_sidecar)
                }), 201
            case _:
                raise TypeError("Expected type car or motorcycle")
    return render_template("newVehicles.html", form=form)


@app.route('/vehicles/<int:vehicle_id>/edit', methods=['GET', 'POST'])
def update_vehicles(vehicle_id):
    """
    **Эндпоинт:** `PUT /vehicles/<int:vehicle_id>`

     **Пример запроса:**
     ```json
     {
       "brand": "Tesla",
       "model": "Model X",
       "num_doors": 6,
       "type": "car"
     }
     ```

     **Пример ответа:**
     ```json
     {
       "message": "Vehicle updated successfully",
       "vehicle": {"id": 3, "brand": "Tesla", "model": "Model X", "num_doors": 6, "type": "car"}
     }
     ```
    """
    vehicle = vehicle_dao.VehicleDB.query.get_or_404(vehicle_id, description='Vehicle not found')
    form = VehicleForm(obj=vehicle)

    if form.validate_on_submit():
        vehicle.brand = form.brand.data
        vehicle.model = form.model.data

        match vehicle.vehicle_type:
            case "car":
                car = car_dao.CarDB.query.filter_by(id_vehicle=vehicle_id).first()
                car.num_doors = form.num_doors.data
            case "motorcycle":
                motorcycle = moto_dao.MotorcycleDB.query.filter_by(id_vehicle=vehicle_id).first()
                motorcycle.has_sidecar = form.has_sidecar.data

        db.session.commit()

        return jsonify({
            'message': 'Vehicle updated successfully',
            'vehicle': {
                "id": vehicle.id,
                "brand": vehicle.brand,
                "model": vehicle.model,
                "type": vehicle.vehicle_type,
                "num_doors": car.num_doors if vehicle.vehicle_type == "car" else None,
                "has_sidecar": motorcycle.has_sidecar if vehicle.vehicle_type == "motorcycle" else None
            }
        }), 200

    attr = None
    match vehicle.vehicle_type:
        case "car":
            car = car_dao.CarDB.query.filter_by(id_vehicle=vehicle_id).first()
            attr = car.num_doors
        case "motorcycle":
            motorcycle = moto_dao.MotorcycleDB.query.filter_by(id_vehicle=vehicle_id).first()
            attr = motorcycle.has_sidecar

    return render_template("editVehicles.html", form=form, vehicle=vehicle, attr=attr)


@app.route('/vehicles/<int:vehicle_id>/delete', methods=['POST'])
def delete_vehicles(vehicle_id):
    """
    **Эндпоинт:** `DELETE /vehicles/<int:vehicle_id>`

     **Пример ответа:**
     ```json
     {
       "message": "Vehicle deleted successfully"
     }
     ```
    """
    vehicle = vehicle_dao.VehicleDB.query.get(vehicle_id)
    db.session.delete(vehicle)
    db.session.commit()

    attr = None

    if vehicle.vehicle_type == "car":
        attr = car_dao.CarDB.query.filter_by(id_vehicle=vehicle_id).first()
    else:
        attr = moto_dao.MotorcycleDB.query.filter_by(id_vehicle=vehicle_id).first()

    db.session.delete(attr)
    db.session.commit()

    return jsonify({"message": "Vehicle deleted successfully"})


if __name__ == '__main__':
    app.run(debug=True)
