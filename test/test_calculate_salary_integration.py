import sys
sys.path.append("src/")
from pytest import mark
from src import calculate_salary
from src import User
from src import RepositorySalary
from google.cloud import firestore


def get_user_salary(user_id: str):
    collection_name = "users_salary"
    db = firestore.Client(project="emulator")
    try:
        doc_ref = db.collection(
            collection_name).document(user_id)
        doc = doc_ref.get()
        print(doc.to_dict())
        if doc.exists:
            return doc.to_dict()["salary"]
        else:
            return None
    except Exception as e:
        print(f"An error occurred while retrieving user salary: {e}")
        return None


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
        self.repository_salary = RepositorySalary(
            firestore_client=firestore.Client(project="emulator")
        )

    def when(self):
        self.salary = self.calculate_salary(self.user, self.repository_salary)

    def then(self):
        assert self.salary == self.salary_expected
        salary_db = get_user_salary(self.user.id)
        assert salary_db == self.salary_expected


@mark.parametrize(
    argnames="""
        name, age, salary, id, salary_expected
        """,
    argvalues=[
        ("John", 20, 300, "1", 240),
        ("Jane", 19, 250, "2", 200),
        ("Bob", 10, 400, "3", 320),
        ("Bob", 28, 200, "4", 180),
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
