from . import User


class RepositorySalary:

    def __init__(self, firestore_client):
        self.db = firestore_client
        self.collection_name = "users_salary"

    def save_user_salary(self, user: User, new_salary: int):
        """Saves a user's salary to Firestore.

        Args:
            user: The User object.
            new_salary: The new salary to be saved.
        """
        try:
            doc_ref = self.db.collection(
                self.collection_name).document(user.id)
            doc_ref.set(
                {
                    "name": user.name,
                    "age": user.age,
                    "salary": new_salary,
                    "id": user.id,
                }
            )
            print(
                f"User {user.name} with ID {user.id} salary updated to {new_salary} in Firestore.")
        except Exception as e:
            print(f"An error occurred while saving user salary: {e}")
                