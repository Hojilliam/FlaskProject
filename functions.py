from models import Spending, User

def get_avg(user_list):
    users25_30_spending = 0
    counter = 0
    for user_id in user_list:
        iterator = Spending.query.filter_by(user_id=user_id).all()
        for value in iterator:
            users25_30_spending += value.money_spent
            counter += 1
    return users25_30_spending / counter