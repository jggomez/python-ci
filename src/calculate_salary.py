from . import User


def calculate_salary(user: User, repository_salary) -> int:
    """Calculates the salary of a user.

    Args:
        user (User): The user to calculate the salary for.

    Returns:
        int: The calculated salary.
    """
    new_salary = user.salary
    if user.age < 21:
        new_salary = user.salary * 0.8
    elif user.age < 30:
        new_salary = user.salary * 0.9

    repository_salary.save_user_salary(user, new_salary)
    return new_salary
