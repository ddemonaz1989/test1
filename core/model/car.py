from core.model.vehicle import Vehicle


class Car(Vehicle):

    def __init__(self, brand, model, num_doors):
        super().__init__(brand, model)
        self.__num_doors = num_doors

    @property
    def num_doors(self):
        return self.__num_doors

    @num_doors.setter
    def num_doors(self, num_doors):
        self.__num_doors = num_doors

    def display_info(self):
        super().display_info()
        print(f"Number of doors: {self.__num_doors}")
