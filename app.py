from flask import Flask, request, jsonify
from extensions import db, client
from models import User, Spending
from sqlalchemy import inspect, and_

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users_vouchers.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database with the app
db.init_app(app)

# Create tables at startup
with app.app_context():
    db.create_all()

def get_user_spent(user_id):
    spending = Spending.query.filter_by(user_id=user_id).all()
    total_spent = 0
    for value in spending:
        total_spent += value.money_spent
    return total_spent

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())

@app.route("/users", methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

# Unfinished - returns single value instead of list of all values
@app.route("/total_spent/<int:user_id>", methods=['GET'])
def get_total_spent(user_id):

    spending = Spending.query.filter_by(user_id=user_id).all()

    total_spent = 0
    for value in spending:
        total_spent += value.money_spent

    data = {
        'user_id': user_id,
        'total_spent': total_spent
    }

    return jsonify(data)

# To be checked for accuracy
@app.route('/average_spending_by_age', methods=['GET'])
def get_avg_by_age():

    def get_avg(users):
        users_spending = 0
        counter = 0
        for user_id in users:
            base = Spending.query.filter_by(user_id=user_id).all()
            for value in base:
                users_spending += value.money_spent
                counter += 1
        return users_spending / counter

    def get_users_by_age_range(min_age, max_age=None):
        if max_age:
            return User.query.filter(and_(User.age >= min_age, User.age <= max_age)).all()
        else:
            return User.query.filter(User.age >= min_age).all()

    def calculate_avg_spending(users):
        user_ids = [user.user_id for user in users]
        return get_avg(user_ids)

    age_ranges = [
        (18, 24),
        (25, 30),
        (31, 36),
        (37, 47),
        (47, None)
    ]

    avg_spending_by_age = {}

    for min_age, max_age in age_ranges:
        users = get_users_by_age_range(min_age, max_age)
        avg_spending = calculate_avg_spending(users)
        age_key = f'{min_age} - {max_age}' if max_age else f'{min_age}+'
        avg_spending_by_age[age_key] = round(avg_spending, 2)

    return jsonify(avg_spending_by_age)

@app.route('/write_to_mongodb', methods=['POST'])
def write_to_mongodb():

    users = User.query.all()

    db = client['test']
    collection = db['vouchers']

    try:
        for user in users:
            data = {
                'user': user.to_dict(),
                'total_spent': get_user_spent(user.user_id)
            }
            if get_user_spent(user.user_id) > 1000:
                collection.insert_one(data)
    except Exception as e:
        return f'Failed to add data to MongoDB! {e}', 500

    return 'Added user data to MongoDB!', 201

@app.route('/update_mongodb', methods=['PUT'])
def update_mongodb():

    users = User.query.all()

    db = client['test']
    collection = db['vouchers']

    try:
        for user in users:
            data = {
                'user': user.to_dict(),
                'total_spent': get_user_spent(user.user_id)
            }
            if get_user_spent(user.user_id) > 1000:
                collection.update_one(
                    {'user_id': user.to_dict()},
                    {'$set': data},
                    # upsert=True
                )
    except Exception as e:
        return f'Failed to update data in MongoDB! {e}', 500

    return 'Updated user data in MongoDB!', 201

if __name__ == '__main__':
    app.run(debug=True)
