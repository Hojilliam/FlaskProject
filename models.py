from extensions import db

class User(db.Model):
    __tablename__ = 'user_info'
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
    user_id = db.Column(db.Integer, db.ForeignKey('user_info.user_id'), primary_key=True)
    money_spent = db.Column(db.Float)
    year = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'money_spent': self.money_spent,
            'year': self.year
        }