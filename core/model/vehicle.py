class Vehicle:

    def __init__(self, brand, model):
        self.__brand = brand
        self.__model = model

    @property
    def brand(self):
        return self.__brand

    @brand.setter
    def brand(self, brand):
        self.__brand = brand

    @property
    def model(self):
        return self.__model

    @model.setter
    def model(self, model):
        self.__model = model

    def display_info(self):
        print(f"Brand: {self.__brand}, Model: {self.__model}")
