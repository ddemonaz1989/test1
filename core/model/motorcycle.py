from core.model.vehicle import Vehicle


class Motorcycle(Vehicle):

    def __init__(self, brand, model, has_sidecar):
        super().__init__(brand, model)
        self.__has_sidecar = has_sidecar

    @property
    def has_sidecar(self):
        return self.__has_sidecar

    @has_sidecar.setter
    def has_sidecar(self, has_sidecar):
        self.__has_sidecar = has_sidecar

    def display_info(self):
        super().display_info()
        sidecar_status = "Yes" if self.__has_sidecar else "No"
        print(f"Has sidecar: {sidecar_status}")