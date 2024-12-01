from dao.db_conf import db


class MotorcycleDB(db.Model):
    __TYPE = "motorcycle"
    __tablename__ = 'motorcycles_attribute'
    id = db.Column(db.Integer, primary_key=True)
    id_vehicle = db.Column(db.Integer, db.ForeignKey('vehicles.id'))
    has_sidecar = db.Column(db.Boolean, nullable=False)