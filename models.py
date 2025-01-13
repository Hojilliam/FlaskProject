from extensions import db

class User(db.Model):
    __tablename__ = 'user_info'

    def __str__(self):
        return f'{self.name} is {self.age} years old and has the email {self.email}'

    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'name': self.name,
            'email': self.email,
            'age': self.age
        }

class Spending(db.Model):
    __tablename__ = 'user_spending'

    def __str__(self):
        return f'{self.user_id} spent {self.money_spent} in {self.year}'

    user_id = db.Column(db.Integer, db.ForeignKey('user_info.user_id'), primary_key=True, nullable=False)
    money_spent = db.Column(db.Float)
    year = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'money_spent': self.money_spent,
            'year': self.year
        }