import uuid #This package create ids uniques

class Client:


    def __init__(self, name, company, email, position, uid=None) -> None:
        self.name = name
        self.company = company
        self.email = email
        self.position = position
        self.uid = uid or uuid.uuid4()

    
    def to_dict(self):
        return vars(self)


    #  ---> @staticmethod nos permite declarar métodos estáticos en nuestra clase. Es un método que se puede ejecutar sin necesidad de una instancia de una clase. No hace falta que reciba self como parámetro. <----

    @staticmethod
    def schema():
        return ['name', 'company', 'email', 'position', 'uid']
