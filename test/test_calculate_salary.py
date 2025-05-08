import sys
sys.path.append("src/")
from unittest.mock import Mock
from src import User
from src import calculate_salary
from pytest import mark
from src import RepositorySalary


class calculate_salary_age_less_21:

    def given(
        self,
        name,
        age,
        salary,
        id,
        salary_expected,
        calculate_salary,
    ):
        self.name = name
        self.age = age
        self.salary = salary
        self.id = id
        self.calculate_salary = calculate_salary
        self.user = User(
            name=self.name,
            age=self.age,
            salary=self.salary,
            id=self.id,
        )
        self.salary_expected = salary_expected
        self.repository_salary: RepositorySalary = Mock()
        self.repository_salary.save_user_salary = Mock(
            return_value=None
        )


    def when(self):
        self.salary = self.calculate_salary(self.user, self.repository_salary)

    def then(self):
        assert self.salary == self.salary_expected
        self.repository_salary.save_user_salary.assert_called_once_with(
            self.user, self.salary_expected
        )


@mark.parametrize(
    argnames="""
        name, age, salary, id, salary_expected
        """,
    argvalues=[
        ("John", 20, 300, "1", 240),
        ("Jane", 19, 250, "2", 200),
        ("Bob", 10, 400, "3", 320),
        ("Bob", 28, 200, "3", 180),
    ],
)
def test_calculate_salary(
    name: str,
    age: int,
    salary: int,
    id: str,
    salary_expected: int,
):
    test = calculate_salary_age_less_21()
    test.given(
        name=name,
        age=age,
        salary=salary,
        id=id,
        salary_expected=salary_expected,
        calculate_salary=calculate_salary,
    )
    test.when()
    test.then()
