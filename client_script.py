import requests

# Base URL of the Flask application
BASE_URL = 'http://localhost:5000'

def get_total_spending(user_id):
    response = requests.get(f'{BASE_URL}/total_spent/{user_id}')
    if response.status_code == 200:
        return response.json()
    else:
        print(f'Failed to retrieve total spending for user {user_id}')
        return None

def write_to_mongodb(user_data):
    response = requests.post(f'{BASE_URL}/write_to_mongodb', json=user_data)
    if response.status_code == 201:
        print('User data added to MongoDB successfully!')
    else:
        print(f'Failed to add user data to MongoDB: {response.text}')

def get_avg_spending_by_age():
    response = requests.get(f'{BASE_URL}/average_spending_by_age')
    if response.status_code == 200:
        return response.json()
    else:
        print('Failed to retrieve average spending by age')
        return None

def main():
    while True:
        try:
            user_id = int(input('Enter user ID: '))
            if 0 < user_id <= 3000:
                break
            else:
                print('User ID must be between 1 and 3000')
        except ValueError:
            print('User ID must be a number')

    total_spending = get_total_spending(user_id)
    print('Total spending:', total_spending['total_spent'])
    if total_spending and total_spending['total_spent'] > 1000:
        user_data = {
            'user_id': user_id,
            'total_spent': total_spending['total_spent']
        }
        write_to_mongodb(user_data)

    avg_spending_by_age = get_avg_spending_by_age()
    if avg_spending_by_age:
        print('Average spending by age:')
        for age_range, avg_spending in avg_spending_by_age.items():
            print(f'{age_range}: {avg_spending}')

if __name__ == '__main__':
    main()