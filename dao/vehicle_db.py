from dao.db_conf import db


class VehicleDB(db.Model):
    __tablename__ = 'vehicles'
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String, nullable=False)
    model = db.Column(db.String, nullable=False)
    vehicle_type = db.Column(db.String, nullable=False)

    def to_json(self, attr):
        return {
            'id': self.id,
            'brand': self.brand,
            'model': self.model,
            'num_doors' if self.vehicle_type == "car" else 'has sidecar': attr,
            'type': self.vehicle_type
        }