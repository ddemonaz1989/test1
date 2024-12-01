from dao.db_conf import db


class CarDB(db.Model):
    __TYPE = "car"
    __tablename__ = 'cars_attribute'
    id = db.Column(db.Integer, primary_key=True)
    id_vehicle = db.Column(db.Integer, db.ForeignKey('vehicles.id'))
    num_doors = db.Column(db.Integer, nullable=False)
