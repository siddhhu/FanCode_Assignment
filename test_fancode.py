import requests
import unittest

# API Base URL
BASE_URL = "http://jsonplaceholder.typicode.com"

class FancodeTest(unittest.TestCase):
    def setUp(self):
        self.users_url = f"{BASE_URL}/users"
        self.todos_url = f"{BASE_URL}/todos"

    def get_fancode_users(self):
        # Fetch users from the API
        response = requests.get(self.users_url)
        if response.status_code == 200:
            users = response.json()
            # Filtering users based on FanCode's lat-long boundaries
            fancode_users = [
                user for user in users 
                if -40 <= float(user['address']['geo']['lat']) <= 5 
                and 5 <= float(user['address']['geo']['lng']) <= 100
            ]
            return fancode_users
        else:
            raise Exception(f"Failed to fetch users: {response.status_code}")

    def get_user_todos(self, user_id):
        # Fetch todos for a given user by their user_id
        response = requests.get(self.todos_url, params={'userId': user_id})
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to fetch todos for user {user_id}: {response.status_code}")

    def test_fancode_users_completion(self):
        # Test to ensure that more than 50% of tasks for each FanCode user are completed
        fancode_users = self.get_fancode_users()

        for user in fancode_users:
            todos = self.get_user_todos(user['id'])
            total_tasks = len(todos)
            completed_tasks = len([todo for todo in todos if todo['completed']])

            # Print user details for more information
            print(f"Testing user: {user['name']} (ID: {user['id']})")
            print(f"Total tasks: {total_tasks}, Completed tasks: {completed_tasks}")

            # Edge Case 1: User has no todos
            if total_tasks == 0:
                print(f"User {user['name']} (ID: {user['id']}) has no todo tasks.")
                continue

            # Checking if the user has more than 50% tasks completed
            self.assertGreater(completed_tasks, total_tasks / 2,
                f"User {user['name']} (ID: {user['id']}) has not completed more than 50% of their tasks")

if __name__ == "__main__":
    unittest.main()